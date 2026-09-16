"""FastAPI server for the local Job Hunt web application."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import random
import shutil
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from ..config import (
    PROJECT_ROOT,
    RESUMES_DIR,
    get_settings,
)
from ..gmail import GmailClient
from ..jobs import build_job, fetch_from_url, load_profession_vocabulary
from ..llm import LLMConfig, get_llm_client
from ..pdf import render_resume_pdf
from ..resume import ResumeBuilder
from ..sheet import SheetClient
from ..utils import slugify
from ..services.public_apis import verify_email_deliverability
from ..services.jobspy_service import scraper_service
from ..services.first_reader import audit_outreach_pitch
from ..email_finder import discover_and_score_emails
from ..scraper.sources.rss_adapter import RSSFeedAdapter, DEFAULT_RSS_FEEDS
from ..services.autopilot_service import autopilot_service
from ..services.autopsy_service import run_applications_autopsy
from .db import (
    ingest_scraped_batch, get_ingestion_history, update_lead_email_verification,
    list_applications, record_application, update_status, init_db,
    delete_application, clear_all_applications,
    get_profile, save_profile, get_dashboard_analytics, record_inbound_reply,
    list_inbound_replies, record_lead, list_leads, get_lead,
    update_lead_status, bulk_insert_leads, get_leads_stats, DB_PATH,
    ingest_rss_leads, get_user_quota, update_user_quota, consume_unmask_credit,
    grant_unmask_credits, is_lead_unmasked
)

app = FastAPI(title="AOE - Autonomous Outreach Engine API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = PROJECT_ROOT / "frontend"


# --- Models ---

class ScraperTriggerRequest(BaseModel):
    role: str = "Product Designer"
    seniority: str = "Any"
    geography: str = "All"
    freshness_hours: int = 72
    mode: str = "Express"

class EmailVerifyRequest(BaseModel):
    lead_id: int
    email: Optional[str] = None

class PitchAuditRequest(BaseModel):
    subject: str = ""
    body: str = ""

class FindEmailRequest(BaseModel):
    company: str = ""
    contact_name: str = ""
    domain: Optional[str] = None
    lead_id: Optional[int] = None

class VerifyProRequest(BaseModel):
    passkey: str = ""

class ConfigPayload(BaseModel):
    candidate_name: str = ""
    candidate_email: str = ""
    candidate_phone: str = ""
    candidate_location: str = ""
    candidate_portfolio: str = ""
    candidate_linkedin: str = ""
    sender_email: str = ""
    dry_run: bool = True
    llm_provider: str = "gemini"
    llm_api_key: str = ""
    llm_model: str = ""
    llm_base_url: Optional[str] = None
    default_profession: str = "product-designer"
    tracker_spreadsheet_id: str = ""


class ParseJobRequest(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = None
    profession: Optional[str] = None


class AnalyzeJobRequest(BaseModel):
    company: str
    role: str
    text: str
    keywords: List[str] = Field(default_factory=list)
    profession: Optional[str] = None
    llm_provider: Optional[str] = None
    llm_api_key: Optional[str] = None


class TailorResumeRequest(BaseModel):
    company: str = "Target Company"
    role: str = "Product Designer"
    text: Optional[str] = ""
    job_text: Optional[str] = ""
    contact_email: Optional[str] = None
    profession: Optional[str] = None
    custom_summary: Optional[str] = None
    mode: str = "branded"  # branded or ats
    accent_color: str = "#2563eb"
    font_pairing: str = "grotesque"
    country: Optional[str] = "us"
    page_budget: Optional[str] = "1"
    visa_status: Optional[str] = None
    nationality: Optional[str] = None
    photo_path: Optional[str] = None


class RenderCustomPdfRequest(BaseModel):
    company: str
    role: str
    text: str
    profession: Optional[str] = None
    accent_color: str = "#0ea5e9"
    mode: str = "branded"


class DraftEmailRequest(BaseModel):
    company: str = "Target Company"
    role: str = "Product Designer"
    job_text: Optional[str] = ""
    contact_email: Optional[str] = None
    to: Optional[str] = None
    llm_provider: Optional[str] = None
    llm_api_key: Optional[str] = None


class SendEmailRequest(BaseModel):
    to: str
    subject: str
    body: str
    company: str
    role: str
    url: Optional[str] = ""
    resume_path: Optional[str] = ""


class UpdateStatusRequest(BaseModel):
    app_id: int
    status: str
    notes: Optional[str] = None


class DeleteAppRequest(BaseModel):
    app_id: int

class ProfilePayload(BaseModel):
    full_name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    target_role: str = ""
    experience_years: str = ""
    salary_min: int = 45000
    salary_max: int = 75000
    currency: str = "GBP (£)"
    work_mode: str = "Hybrid"
    portfolio_links: Dict[str, str] = Field(default_factory=dict)
    resume_markdown: str = ""
    extracted_skills: List[str] = Field(default_factory=list)
    llm_provider: str = "gemini"
    llm_api_key: str = ""
    llm_model: str = "gemini-1.5-flash"
    gmail_account: str = ""
    google_sheet_id: str = ""
    dry_run: bool = True
    activation_passkey: str = ""


class LeadCreateRequest(BaseModel):
    company: str
    role: str = "Product Designer"
    country: str = ""
    category: str = "Direct"
    contact_email: str = ""
    contact_person: str = ""
    website: str = ""
    job_url: str = ""
    status: str = "To Contact"
    notes: str = ""


class LeadStatusUpdateRequest(BaseModel):
    lead_id: int
    status: str
    notes: Optional[str] = None


class CsvImportRequest(BaseModel):
    csv_text: Optional[str] = None
    leads: Optional[List[Dict[str, Any]]] = None


class IngestRSSRequest(BaseModel):
    channels: Optional[List[str]] = Field(default_factory=lambda: ["wwr_design", "remoteok_all"])
    custom_rss_url: Optional[str] = None
    max_per_feed: int = 25



class AutoPilotRunRequest(BaseModel):
    lead_id: Optional[int] = None
    company: Optional[str] = None
    role: Optional[str] = None
    job_url: Optional[str] = None
    jd_text: Optional[str] = None
    contact_email: Optional[str] = None
    contact_person: Optional[str] = None
    profession: Optional[str] = "product-designer"
    llm_provider: Optional[str] = None
    llm_api_key: Optional[str] = None


class BillingCheckoutRequest(BaseModel):
    tier: str = "pro"
    email: Optional[str] = None
    payment_method: Optional[str] = "simulated_card"


class UnmaskLeadRequest(BaseModel):
    lead_id: int


class BatchRunRequest(BaseModel):
    lead_ids: List[int]
    mode: str = "draft"  # "draft", "dry_run", "live_send"
    passkey: Optional[str] = None


class FollowUpRequest(BaseModel):
    target_type: str = "application"  # "application" or "lead"
    target_id: int
    custom_note: Optional[str] = None


class DeleteApplicationRequest(BaseModel):
    app_id: int


class SaveCredentialsRequest(BaseModel):
    credentials_json: str


class ToggleDryRunRequest(BaseModel):
    dry_run: bool


class ScanInboundRequest(BaseModel):
    query: Optional[str] = "-from:me newer_than:30d"
    max_results: Optional[int] = 30


class CopilotChatRequest(BaseModel):
    message: str
    action_topic: Optional[str] = None
    history: List[Dict[str, str]] = Field(default_factory=list)


class ExtractCvRequest(BaseModel):
    cv_text: str


class RegisterCandidateRequest(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = ""
    target_role: Optional[str] = "Senior Product Designer"
    location: Optional[str] = ""
    experience_years: Optional[str] = "5+ Years"
    cv_text: Optional[str] = ""
    portfolio_links: Optional[Dict[str, str]] = Field(default_factory=dict)
    projects_summary: Optional[str] = ""
    achievements_summary: Optional[str] = ""
    is_onboarded: bool = True


# --- Endpoints ---

@app.get("/api/config")
def get_config_endpoint():
    settings = get_settings()
    env_path = PROJECT_ROOT / ".env"
    llm_provider = os.getenv("LLM_PROVIDER", "gemini")
    llm_api_key = (
        os.getenv(f"{llm_provider.upper()}_API_KEY")
        or os.getenv("LLM_API_KEY")
        or ""
    )
    return {
        "candidate_name": settings.candidate_name,
        "candidate_email": settings.candidate_email,
        "candidate_phone": settings.candidate_phone,
        "candidate_location": settings.candidate_location,
        "candidate_portfolio": settings.candidate_portfolio,
        "candidate_linkedin": settings.candidate_linkedin,
        "sender_email": settings.sender_email,
        "dry_run": settings.dry_run,
        "llm_provider": llm_provider,
        "llm_api_key": llm_api_key,
        "llm_model": os.getenv("LLM_MODEL", ""),
        "llm_base_url": os.getenv("LLM_BASE_URL", ""),
        "default_profession": os.getenv("DEFAULT_PROFESSION", "product-designer"),
        "app_env": os.getenv("APP_ENV", settings.app_env),
        "port": settings.port,
        "tracker_spreadsheet_id": settings.tracker_spreadsheet_id,
        "env_file_exists": env_path.exists(),
        "credentials_exist": (PROJECT_ROOT / "credentials.json").exists(),
        "token_exists": (PROJECT_ROOT / "token.json").exists(),
        "master_resume_exists": (PROJECT_ROOT / "master_resume.docx").exists(),
    }


@app.post("/api/config")
def save_config_endpoint(payload: ConfigPayload):
    env_path = PROJECT_ROOT / ".env"
    
    os.environ["CANDIDATE_NAME"] = payload.candidate_name
    os.environ["CANDIDATE_EMAIL"] = payload.candidate_email
    os.environ["CANDIDATE_PHONE"] = payload.candidate_phone
    os.environ["CANDIDATE_LOCATION"] = payload.candidate_location
    os.environ["CANDIDATE_PORTFOLIO"] = payload.candidate_portfolio
    os.environ["CANDIDATE_LINKEDIN"] = payload.candidate_linkedin
    os.environ["SENDER_EMAIL"] = payload.sender_email
    os.environ["DRY_RUN"] = str(payload.dry_run).lower()
    os.environ["LLM_PROVIDER"] = payload.llm_provider
    os.environ[f"{payload.llm_provider.upper()}_API_KEY"] = payload.llm_api_key
    os.environ["LLM_API_KEY"] = payload.llm_api_key
    if payload.llm_model:
        os.environ["LLM_MODEL"] = payload.llm_model
    if payload.llm_base_url:
        os.environ["LLM_BASE_URL"] = payload.llm_base_url
    os.environ["DEFAULT_PROFESSION"] = payload.default_profession
    os.environ["TRACKER_SPREADSHEET_ID"] = payload.tracker_spreadsheet_id

    content = [
        f"CANDIDATE_NAME={payload.candidate_name}",
        f"CANDIDATE_EMAIL={payload.candidate_email}",
        f"CANDIDATE_PHONE={payload.candidate_phone}",
        f"CANDIDATE_LOCATION={payload.candidate_location}",
        f"CANDIDATE_PORTFOLIO={payload.candidate_portfolio}",
        f"CANDIDATE_LINKEDIN={payload.candidate_linkedin}",
        f"SENDER_EMAIL={payload.sender_email}",
        f"DRY_RUN={'true' if payload.dry_run else 'false'}",
        f"LLM_PROVIDER={payload.llm_provider}",
        f"LLM_API_KEY={payload.llm_api_key}",
        f"{payload.llm_provider.upper()}_API_KEY={payload.llm_api_key}",
        f"LLM_MODEL={payload.llm_model}",
        f"LLM_BASE_URL={payload.llm_base_url or ''}",
        f"DEFAULT_PROFESSION={payload.default_profession}",
        f"TRACKER_SPREADSHEET_ID={payload.tracker_spreadsheet_id}",
    ]
    env_path.write_text("\n".join(content) + "\n", encoding="utf-8")
    
    get_settings.cache_clear()
    return {"status": "saved", "message": "Configuration saved successfully"}


@app.get("/api/professions")
def list_professions_endpoint():
    prof_dir = PROJECT_ROOT / "professions"
    if not prof_dir.exists():
        return []
    
    results = []
    for f in sorted(prof_dir.glob("*.yaml")):
        slug = f.stem
        skills, roles = load_profession_vocabulary(slug)
        desc = ""
        name = slug.replace("-", " ").title()
        try:
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip()
                elif line.startswith("description:"):
                    desc = line.split(":", 1)[1].strip()
        except Exception:
            pass
        results.append({
            "slug": slug,
            "name": name,
            "description": desc,
            "skills_count": len(skills),
            "roles_count": len(roles),
        })
    return results


@app.post("/api/test/llm")
def test_llm_endpoint(payload: Dict[str, Any]):
    provider = (payload.get("provider") or "gemini").strip().lower()
    api_key = (payload.get("api_key") or os.getenv(f"{provider.upper()}_API_KEY") or os.getenv("LLM_API_KEY") or "").strip()
    if api_key.startswith("Bearer "):
        api_key = api_key[7:].strip()
    model = (payload.get("model") or "").strip()
    base_url = (payload.get("base_url") or "").strip() or None

    config = LLMConfig(provider=provider, api_key=api_key, model=model, base_url=base_url)
    client = get_llm_client(config)
    
    start_time = time.perf_counter()
    try:
        reply = client.generate("Please reply with: 'Connection successful!' in 5 words or less.")
        duration_ms = round((time.perf_counter() - start_time) * 1000)
        return {
            "status": "ok",
            "provider": provider,
            "latency_ms": duration_ms,
            "response": reply.strip()
        }
    except Exception as exc:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(exc)})


@app.post("/api/test/gmail")
def test_gmail_endpoint():
    try:
        client = GmailClient()
        profile = client.get_profile()
        return {"status": "ok", "email": profile.get("emailAddress"), "messagesTotal": profile.get("messagesTotal")}
    except Exception as exc:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(exc)})


@app.post("/api/jobs/parse")
def parse_job_endpoint(req: ParseJobRequest):
    text = req.text or ""
    if req.url and not text:
        try:
            text = fetch_from_url(req.url)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Failed to fetch job URL: {exc}")

    if not text:
        raise HTTPException(status_code=400, detail="Either a job URL or job text must be provided.")

    job = build_job(
        text=text,
        url=req.url,
        company=req.company,
        role=req.role,
        profession=req.profession,
    )
    return {
        "company": job.company,
        "role": job.role,
        "url": job.url,
        "contact_email": job.contact_email,
        "keywords": job.keywords,
        "text": job.text[:4000],
    }


@app.post("/api/jobs/analyze")
def analyze_job_endpoint(req: AnalyzeJobRequest):
    skills, _ = load_profession_vocabulary(req.profession)
    text_lower = req.text.lower()
    
    matched = [s for s in skills if s in text_lower]
    score = min(96.0, max(38.0, round(len(matched) * 7.2 + 22.0, 1)))
    gaps = [s for s in skills[:25] if s not in matched][:6]

    strategy = f"Position your background around {', '.join(matched[:3]) if matched else 'core product engineering'}. Explicitly highlight your ownership of requirements matching {req.role} at {req.company}."

    try:
        provider = req.llm_provider or os.getenv("LLM_PROVIDER", "gemini")
        api_key = req.llm_api_key or os.getenv(f"{provider.upper()}_API_KEY") or os.getenv("LLM_API_KEY")
        if api_key:
            client = get_llm_client(LLMConfig(provider=provider, api_key=api_key))
            prompt = (
                f"Analyze this job for {req.role} at {req.company}.\n"
                f"Job description: {req.text[:2000]}\n\n"
                "Return a punchy 2-sentence positioning strategy for the candidate: sentence 1 highlights their angle, sentence 2 explains how to address any gap."
            )
            llm_strategy = client.generate(prompt)
            if llm_strategy:
                strategy = llm_strategy.strip()
    except Exception:
        pass

    fit_level = "High Alignment" if score >= 75.0 else ("Strong Match" if score >= 60.0 else "Moderate Fit")

    return {
        "match_score": score,
        "matched_skills": matched,
        "gap_skills": gaps,
        "strategy": strategy,
        "positioning_angle": strategy,
        "fit_level": fit_level,
        "matched_count": len(matched),
        "gap_count": len(gaps),
    }


@app.post("/api/resume/tailor")
def tailor_resume_endpoint(req: TailorResumeRequest):
    job_text = req.text or req.job_text or ""
    job = build_job(
        text=job_text,
        company=req.company,
        role=req.role,
        profession=req.profession,
    )
    builder = ResumeBuilder()
    data, docx_path = builder.build(job)

    slug = slugify(job.company)
    out_pdf = RESUMES_DIR / f"{slug}_resume.pdf"
    render_resume_pdf(data, out_pdf)

    # Load candidate profile evidence
    profile = get_profile()
    name = profile.get("full_name") or "Candidate Name"
    email = profile.get("email") or "user@example.com"
    phone = profile.get("phone") or "+1-555-019-2834"
    loc = profile.get("location") or "San Francisco, CA"
    links = profile.get("portfolio_links") or {}
    figma = links.get("figma") or "https://figma.com/@portfolio"
    behance = links.get("behance") or "https://behance.net/portfolio"
    notion = links.get("notion") or "https://notion.site/portfolio"
    github = links.get("github") or "https://github.com/portfolio"
    showreel = links.get("showreel") or "https://youtube.com/portfolio"

    is_middle_east = (req.country or "").lower() in ["ae", "sa", "om", "qa", "dubai", "uae"]
    is_one_page = (req.page_budget or "1") == "1"

    # Middle East metadata line
    middle_east_header = ""
    if is_middle_east:
        visa = req.visa_status or "Employment Visa (Transferable)"
        nat = req.nationality or "Indian"
        middle_east_header = f"\nVisa Status: {visa} | Nationality: {nat}"
        if req.photo_path:
            middle_east_header += f" | Photo: {req.photo_path}"

    summary_text = (
        f"Senior Product Designer with 5+ years of end-to-end UX ownership, high-conversion web/mobile interfaces, "
        f"and design systems governance. Targeting the {job.role} role at {job.company} with immediate capability in user research, "
        f"systematic design tokens, and rapid interactive prototyping."
    )

    matched = job.matched_skills or ["Design Systems", "Figma", "User Research", "Interaction Design", "Prototyping", "Information Architecture"]
    skills_formatted = " · ".join(matched[:8])

    if is_one_page:
        # Strict 1-Page Layout: 3-4 bullets per role, compact spacing, ~320 words total
        experience_section = f"""## Professional Experience

**Senior Product Designer** | Enterprise SaaS & Digital Labs
*2022 – Present | Delhi NCR, India*
- Designed and scaled centralized Figma design system adopted across 4 engineering squads, reducing design-to-production turnaround by 40%.
- Spearheaded end-to-end redesign of core analytics workflows, boosting 30-day user retention by 28% and driving a 1.8x CSAT increase.
- Conducted weekly moderated usability testing sessions and translated qualitative research into high-fidelity interactive motion prototypes.

**Product / UI-UX Designer** | Creative Digital Studio
*2020 – 2022 | Remote*
- Shipped 8 responsive web and mobile products across fintech, logistics, and creator platforms with strict accessibility standards (WCAG AA).
- Built component libraries and micro-interactions in code (Tailwind CSS, HTML/JS) accelerating engineering handoffs."""
    else:
        # 2-Page Executive / C-Level Layout: full historical coverage
        experience_section = f"""## Professional Experience

**Lead Product Designer & Design Architect** | Enterprise Labs
*2022 – Present | Delhi NCR, India*
- Direct design systems governance, UI-UX roadmap, and user research strategy across 4 cross-functional squads and 25+ engineers.
- Architected modular design tokens and component libraries, cutting UI defect rates by 45% and unifying multi-brand design language.
- Spearheaded end-to-end redesign of flagship B2B dashboard, increasing 30-day user retention by 28% and annual expansion ARR.
- Partnered directly with executive leadership on quarterly product vision prototypes and investor pitch demos.

**Senior UI-UX Designer** | Creative Agency
*2020 – 2022 | Remote*
- Led product design engagements for 12 enterprise and startup clients in fintech, consumer tech, and SaaS.
- Facilitated design thinking workshops, stakeholder alignment, and comprehensive usability studies with 60+ global users.
- Mentored junior designers and established standard operating procedures for Figma auto-layout and prototyping handoff.

**UI Designer & Visual Specialist** | Digital Studio
*2018 – 2020 | Delhi NCR, India*
- Designed responsive interfaces, brand style guides, and design collateral for early-stage venture-backed products."""

    tailored_markdown = f"""# {name}
### {job.role} | {loc}
{email} | {phone}{middle_east_header}

## Professional Summary
{summary_text}

## Core Capabilities & Technical Skills
{skills_formatted}

{experience_section}

## Selected Live Work & Evidence Hub
- **Interactive Figma Prototypes:** [{figma}]({figma})
- **Product Case Studies:** [{notion}]({notion})
- **Visual Design & Behance:** [{behance}]({behance})
- **Motion & Creative Showreel:** [{showreel}]({showreel})

## Education & Certifications
- **Bachelor of Design (B.Des)** | Product & Interaction Design
"""

    return {
        "company": job.company,
        "role": job.role,
        "summary": summary_text,
        "matched_skills": job.matched_skills,
        "markdown": tailored_markdown.strip(),
        "docx_path": str(docx_path),
        "pdf_path": str(out_pdf),
        "pdf_filename": out_pdf.name,
        "page_budget": "1" if is_one_page else "2",
        "country": req.country or "us",
        "is_middle_east": is_middle_east,
    }


@app.post("/api/resume/render-custom")
def render_custom_pdf_endpoint(req: RenderCustomPdfRequest):
    job = build_job(
        text=req.text,
        company=req.company,
        role=req.role,
        profession=req.profession,
    )
    builder = ResumeBuilder()
    data, docx_path = builder.build(job)
    
    slug = slugify(job.company)
    out_pdf = RESUMES_DIR / f"{slug}_resume.pdf"
    render_resume_pdf(data, out_pdf)

    return {
        "pdf_filename": out_pdf.name,
        "pdf_path": str(out_pdf),
        "accent_color": req.accent_color,
        "mode": req.mode
    }


@app.get("/api/resume/preview/{filename}")
def preview_pdf_endpoint(filename: str):
    file_path = RESUMES_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Resume PDF not found.")
    return FileResponse(
        file_path,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )


@app.post("/api/email/draft")
def draft_email_endpoint(req: DraftEmailRequest):
    settings = get_settings()
    candidate_name = settings.candidate_name or "Candidate"
    portfolio = settings.candidate_portfolio or ""
    
    provider = req.llm_provider or os.getenv("LLM_PROVIDER", "gemini")
    api_key = req.llm_api_key or os.getenv(f"{provider.upper()}_API_KEY") or os.getenv("LLM_API_KEY")
    
    if api_key:
        try:
            client = get_llm_client(LLMConfig(provider=provider, api_key=api_key))
            system_prompt = (
                "You are an expert career agent writing short, conversational cold outreach emails to hiring managers.\n"
                "RULES:\n"
                "- Write in first person (I / my).\n"
                "- 3-4 short paragraphs maximum. No corporate fluff or filler.\n"
                "- Do NOT say 'I hope this email finds you well' or 'I am writing to express my keen interest'.\n"
                "- Immediately reference the specific role and company, and highlight 2 directly relevant capabilities.\n"
                "- Include a natural sentence pointing to the attached resume and portfolio link.\n"
                "- Output format: First line: 'Subject: <subject>', followed by body text."
            )
            prompt = (
                f"Candidate: {candidate_name}\n"
                f"Portfolio: {portfolio}\n"
                f"Role: {req.role}\n"
                f"Company: {req.company}\n"
                f"Job Details: {req.job_text[:2000]}\n\n"
                "Draft the email."
            )
            res = client.generate(prompt, system_prompt=system_prompt).strip()
            lines = res.splitlines()
            subject = f"Application: {req.role} — {candidate_name}"
            body_lines = []
            for line in lines:
                if line.lower().startswith("subject:"):
                    subject = line.split(":", 1)[1].strip()
                else:
                    body_lines.append(line)
            body = "\n".join(body_lines).strip()
            return {"subject": subject, "body": body}
        except Exception:
            pass

    subject = f"{req.role} — {candidate_name}"
    body = (
        f"Hi {req.company} Team,\n\n"
        f"I came across the {req.role} opening at {req.company} and wanted to reach out directly.\n\n"
        f"My background centers on shipping end-to-end solutions, driving user impact, and fast cross-functional execution. "
        + (f"You can explore some of my recent live work here: {portfolio}\n\n" if portfolio else "\n")
        + "I have attached my tailored resume for your review and would love to connect briefly if this aligns with what you need.\n\n"
        f"Best regards,\n{candidate_name}\n{settings.candidate_phone}\n{settings.candidate_email}"
    )
    return {"subject": subject, "body": body}


@app.post("/api/email/send")
def send_email_endpoint(req: SendEmailRequest):
    settings = get_settings()
    client = GmailClient()
    
    attachments = []
    if req.resume_path and Path(req.resume_path).exists():
        attachments.append(req.resume_path)

    outcome = client.send_email(
        to=req.to,
        subject=req.subject,
        body=req.body,
        attachments=attachments,
    )
    
    status = "Sent" if not outcome.get("dry_run") else "Dry Run"
    message_id = outcome.get("id", "")

    app_id = record_application(
        company=req.company,
        role=req.role,
        url=req.url or "",
        contact_email=req.to,
        status=status,
        resume_path=req.resume_path or "",
        email_subject=req.subject,
        email_body=req.body,
        gmail_message_id=message_id,
    )

    try:
        if settings.tracker_spreadsheet_id and not settings.dry_run:
            sheet = SheetClient()
            sheet.update_tracker(
                company=req.company,
                role=req.role,
                url=req.url or "",
                resume=req.resume_path or "",
                status=status,
            )
    except Exception:
        pass

    return {
        "status": "ok",
        "dry_run": settings.dry_run,
        "message_id": message_id,
        "app_id": app_id,
        "message": f"Email successfully {'dispatched' if not settings.dry_run else 'simulated (DRY_RUN active)'} to {req.to}",
    }


@app.get("/api/tracker/applications")
def list_applications_endpoint():
    return list_applications()


@app.get("/api/tracker/stats")
def get_tracker_stats():
    apps = list_applications()
    total = len(apps)
    sent = sum(1 for a in apps if a.get("status") in ("Sent", "Applied"))
    interviews = sum(1 for a in apps if a.get("status") == "Interview")
    offers = sum(1 for a in apps if a.get("status") == "Offer")
    dry_runs = sum(1 for a in apps if a.get("status") == "Dry Run")
    return {
        "total": total,
        "sent": sent,
        "interviews": interviews,
        "offers": offers,
        "dry_runs": dry_runs
    }


@app.post("/api/tracker/delete")
def delete_application_endpoint(req: DeleteApplicationRequest):
    success = delete_application(req.app_id)
    return {"status": "ok" if success else "error"}


@app.post("/api/tracker/clear-all")
def clear_all_applications_endpoint():
    clear_all_applications()
    return {"status": "ok", "message": "All applications reset to 0."}


# --- Gmail Authentication & Inbound Scanner Endpoints ---

@app.get("/api/gmail/status")
def gmail_status_endpoint():
    client = GmailClient()
    return client.get_auth_status()


@app.post("/api/gmail/disconnect")
def disconnect_gmail_endpoint():
    try:
        client = GmailClient()
        res = client.disconnect()
        return {"status": "ok", "message": "Gmail integration disconnected successfully.", "auth": client.get_auth_status()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/gmail/save-credentials")
def save_credentials_endpoint(req: SaveCredentialsRequest):
    try:
        data = json.loads(req.credentials_json)
        if "installed" not in data and "web" not in data:
            raise ValueError("Invalid credentials.json format: must contain 'installed' or 'web' client configuration.")
        cred_path = PROJECT_ROOT / "credentials.json"
        cred_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return {"status": "ok", "message": "credentials.json saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/gmail/sync-workspace")
def sync_workspace_credentials_endpoint():
    try:
        import shutil
        ws_cred = Path(r"g:\job-hunt-workspace-private\job-agent\credentials.json")
        ws_token = Path(r"g:\job-hunt-workspace-private\job-agent\token.json")
        app_cred = PROJECT_ROOT / "credentials.json"
        app_token = PROJECT_ROOT / "token.json"
        synced = []
        if ws_cred.exists():
            shutil.copy(ws_cred, app_cred)
            synced.append("credentials.json")
        if ws_token.exists():
            shutil.copy(ws_token, app_token)
            synced.append("token.json")
        client = GmailClient()
        return {"status": "ok", "synced": synced, "auth": client.get_auth_status()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/gmail/authorize")
def authorize_gmail_endpoint():
    try:
        import threading
        client = GmailClient()
        cred_path = PROJECT_ROOT / "credentials.json"
        if not cred_path.exists():
            import shutil
            ws_cred = Path(r"g:\job-hunt-workspace-private\job-agent\credentials.json")
            if ws_cred.exists():
                shutil.copy(ws_cred, cred_path)
            else:
                raise HTTPException(status_code=400, detail="credentials.json not found. Please upload or paste your credentials.json first.")
        
        threading.Thread(target=client.run_interactive_oauth, daemon=True).start()
        return {
            "status": "started",
            "message": "OAuth server started. Browser opened automatically. Choose your Google account and approve permissions."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/gmail/scan")
def scan_inbound_endpoint(req: Optional[ScanInboundRequest] = None):
    try:
        client = GmailClient()
        status = client.get_auth_status()
        if not status.get("authenticated"):
            return {
                "status": "unauthenticated",
                "message": "Gmail is not connected. Please authorize Gmail first.",
                "replies": [],
                "scanned_count": 0,
                "matched_count": 0,
            }
        
        apps = list_applications()
        query = req.query if req and req.query else "-from:me newer_than:30d"
        max_res = req.max_results if req and req.max_results else 30

        replies = client.scan_inbound_replies(
            tracked_applications=apps,
            query=query,
            max_results=max_res,
        )

        for r in replies:
            record_inbound_reply(
                application_id=r.get("matched_app_id"),
                gmail_message_id=r.get("gmail_message_id"),
                thread_id=r.get("thread_id", ""),
                sender_name=r.get("sender_name", ""),
                sender_email=r.get("sender_email", ""),
                subject=r.get("subject", ""),
                snippet=r.get("snippet", ""),
                body_preview=r.get("body_preview", ""),
                intent=r.get("intent", ""),
                suggested_status=r.get("suggested_status", ""),
                badge=r.get("badge", ""),
                confidence=r.get("confidence", 0.0),
                matched_company=r.get("matched_company", ""),
                matched_role=r.get("matched_role", ""),
                received_date=r.get("date", ""),
            )

        matched_count = sum(1 for r in replies if r.get("matched_app_id"))
        return {
            "status": "ok",
            "scanned_count": len(replies),
            "matched_count": matched_count,
            "replies": replies,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gmail scan failed: {e}")


@app.get("/api/gmail/replies")
def get_inbound_replies_endpoint(limit: int = 30):
    return list_inbound_replies(limit)


@app.post("/api/email/create-draft")
def create_draft_endpoint(req: SendEmailRequest):
    try:
        client = GmailClient()
        attachments = []
        if req.resume_path and Path(req.resume_path).exists():
            attachments.append(req.resume_path)
        
        outcome = client.create_draft(
            to=req.to,
            subject=req.subject,
            body=req.body,
            attachments=attachments,
        )
        return outcome
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create draft: {e}")


@app.post("/api/config/toggle-dry-run")
def toggle_dry_run_endpoint(req: ToggleDryRunRequest):
    profile = get_profile()
    profile["dry_run"] = req.dry_run
    save_profile(profile)
    env_path = PROJECT_ROOT / ".env"
    lines = []
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    val = "true" if req.dry_run else "false"
    found = False
    new_lines = []
    for line in lines:
        if line.strip().startswith("DRY_RUN="):
            new_lines.append(f'DRY_RUN="{val}"\n')
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f'DRY_RUN="{val}"\n')
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    return {"status": "ok", "dry_run": req.dry_run}


@app.post("/api/tracker/update-status")
def update_status_endpoint(req: UpdateStatusRequest):
    success = update_status(req.app_id, req.status, req.notes)
    return {"status": "ok" if success else "error"}


@app.post("/api/tracker/delete")
def delete_application_endpoint(req: DeleteAppRequest):
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM applications WHERE id = ?", (req.app_id,))
        conn.commit()
    return {"status": "ok"}


@app.post("/api/tracker/clear-all")
def clear_all_applications_endpoint():
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM applications")
        conn.commit()
    return {"status": "ok", "message": "All applications cleared"}




@app.get("/api/profile")
def get_profile_endpoint():
    return get_profile()


@app.post("/api/profile")
def save_profile_endpoint(payload: ProfilePayload):
    data = payload.dict()
    res = save_profile(data)
    # Also sync .env for LLM and DRY_RUN
    env_path = PROJECT_ROOT / ".env"
    env_lines = []
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            env_lines = f.readlines()
    
    settings_to_update = {
        "CANDIDATE_NAME": data.get("full_name", ""),
        "CANDIDATE_EMAIL": data.get("email", ""),
        "CANDIDATE_PHONE": data.get("phone", ""),
        "CANDIDATE_LOCATION": data.get("location", ""),
        "CANDIDATE_PORTFOLIO": data.get("portfolio_links", {}).get("figma", "") or data.get("portfolio_links", {}).get("behance", ""),
        "CANDIDATE_LINKEDIN": data.get("portfolio_links", {}).get("linkedin", ""),
        "LLM_PROVIDER": data.get("llm_provider", "gemini"),
        "DRY_RUN": "true" if data.get("dry_run", True) else "false",
        "TRACKER_SPREADSHEET_ID": data.get("google_sheet_id", ""),
    }
    if data.get("llm_api_key"):
        prov = data.get("llm_provider", "gemini").upper()
        settings_to_update[f"{prov}_API_KEY"] = data["llm_api_key"]

    updated_keys = set()
    new_lines = []
    for line in env_lines:
        if "=" in line and not line.strip().startswith("#"):
            k = line.split("=")[0].strip()
            if k in settings_to_update:
                new_lines.append(f'{k}="{settings_to_update[k]}"\n')
                updated_keys.add(k)
                continue
        new_lines.append(line)
    for k, v in settings_to_update.items():
        if k not in updated_keys and v:
            new_lines.append(f'{k}="{v}"\n')
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    return {"status": "ok", "profile": res}


@app.post("/api/profile/extract-cv")
def extract_cv_endpoint(req: ExtractCvRequest):
    """Parses raw pasted CV text into structured onboarding candidate fields."""
    import re
    text = req.cv_text.strip()
    if not text:
        return {"status": "error", "message": "Empty CV text provided"}

    extracted = {
        "full_name": "",
        "email": "",
        "phone": "",
        "target_role": "",
        "location": "",
        "portfolio_links": {},
        "projects_summary": "",
        "achievements_summary": "",
        "skills": []
    }

    # 1. Email extraction
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if email_match:
        extracted["email"] = email_match.group(0)

    # 2. Phone extraction
    phone_match = re.search(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    if phone_match:
        extracted["phone"] = phone_match.group(0)

    # 3. Name extraction (first non-empty line if reasonably short)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines:
        first_line = lines[0]
        if len(first_line) < 40 and not any(c in first_line for c in ['@', 'http', ':', '/', '\\']):
            extracted["full_name"] = first_line

    # 4. Links extraction
    figma_match = re.search(r'https?://[^\s]*figma\.com/[^\s]*', text, re.IGNORECASE)
    if figma_match: extracted["portfolio_links"]["figma"] = figma_match.group(0)
    behance_match = re.search(r'https?://[^\s]*behance\.net/[^\s]*', text, re.IGNORECASE)
    if behance_match: extracted["portfolio_links"]["behance"] = behance_match.group(0)
    notion_match = re.search(r'https?://[^\s]*notion\.(?:so|site)/[^\s]*', text, re.IGNORECASE)
    if notion_match: extracted["portfolio_links"]["notion"] = notion_match.group(0)
    github_match = re.search(r'https?://[^\s]*github\.com/[^\s]*', text, re.IGNORECASE)
    if github_match: extracted["portfolio_links"]["github"] = github_match.group(0)
    linkedin_match = re.search(r'https?://[^\s]*linkedin\.com/in/[^\s]*', text, re.IGNORECASE)
    if linkedin_match: extracted["portfolio_links"]["linkedin"] = linkedin_match.group(0)
    showreel_match = re.search(r'https?://[^\s]*(?:loom\.com|drive\.google\.com|youtube\.com|vimeo\.com)/[^\s]*', text, re.IGNORECASE)
    if showreel_match: extracted["portfolio_links"]["showreel"] = showreel_match.group(0)

    # 5. Role detection
    role_titles = [
        "Founding Product Designer", "Staff Product Designer", "Senior Product Designer", "Product Designer",
        "Lead Product Designer", "UI/UX Designer", "Staff Software Engineer", "Senior Software Engineer",
        "Full Stack Engineer", "Frontend Engineer", "Backend Engineer", "Engineering Manager", "Head of Product"
    ]
    for rt in role_titles:
        if rt.lower() in text.lower():
            extracted["target_role"] = rt
            break

    # 6. Quantified achievements extraction (bullet lines with metrics: %, $, +, x, etc.)
    achievements = []
    projects = []
    for line in lines:
        cleaned = line.lstrip('•-*+> ').strip()
        if not cleaned: continue
        # Detect metrics
        if any(c in cleaned for c in ['%', '$', '+']) and any(w in cleaned.lower() for w in ['increased', 'reduced', 'improved', 'scaled', 'growth', 'retention', 'revenue', 'velocity', 'users', 'latenc']):
            achievements.append("• " + cleaned)
        elif any(w in cleaned.lower() for w in ['led', 'built', 'designed', 'architected', 'spearheaded', 'developed', 'launched', 'created', 'managed', 'founded', 'engineered']):
            projects.append("• " + cleaned)

    if achievements:
        extracted["achievements_summary"] = "\n".join(achievements[:4])
    if projects:
        extracted["projects_summary"] = "\n".join(projects[:4])

    res = dict(extracted)
    res["status"] = "success"
    res["extracted"] = extracted
    return res


@app.post("/api/auth/register")
def register_candidate_endpoint(req: RegisterCandidateRequest):
    """Registers candidate, saves detailed profile & craft links, and sets is_onboarded to True."""
    payload = {
        "full_name": req.full_name,
        "email": req.email,
        "phone": req.phone,
        "target_role": req.target_role,
        "location": req.location,
        "experience_years": req.experience_years,
        "resume_markdown": req.cv_text,
        "portfolio_links": req.portfolio_links,
        "projects_summary": req.projects_summary,
        "achievements_summary": req.achievements_summary,
        "is_onboarded": True
    }
    updated = save_profile(payload)
    return {
        "status": "success",
        "message": "Candidate profile successfully registered and onboarded.",
        "profile": updated
    }


@app.get("/api/auth/session")
def auth_session_endpoint():
    """Checks session state and returns candidate onboarding status."""
    profile = get_profile()
    is_onboarded = profile.get("is_onboarded", False)
    return {
        "authenticated": True,
        "is_onboarded": is_onboarded,
        "profile": profile
    }


@app.get("/api/dashboard/stats")
def get_dashboard_stats_endpoint():
    return get_dashboard_analytics()


@app.post("/api/copilot/chat")
def copilot_chat_endpoint(req: CopilotChatRequest):
    profile = get_profile()
    llm_cfg = LLMConfig(
        provider=profile.get("llm_provider") or os.getenv("LLM_PROVIDER", "gemini"),
        api_key=profile.get("llm_api_key") or os.getenv("GEMINI_API_KEY", ""),
        model=profile.get("llm_model") or "gemini-1.5-flash",
    )
    client = get_llm_client(llm_cfg)
    
    topic_context = ""
    if req.action_topic:
        topic_context = f"[Context: Focus specifically on {req.action_topic}]\n"

    system_prompt = (
        "You are Career Copilot, an elite executive career strategist, design mentor, and technical job search advisor. "
        "Your advice is structured, actionable, modern, and direct (use clean bullet points, bold sections, and emojis). "
        f"Candidate Name: {profile.get('full_name', 'Candidate')}. "
        f"Target Role: {profile.get('target_role', 'Product Designer / Software Engineer')}. "
        f"Experience: {profile.get('experience_years', 'Senior')}. "
        f"Portfolio: {profile.get('portfolio_links', {})}.\n"
        "Always respond in high-craft markdown with specific recommendations."
    )
    try:
        reply = client.generate(req.message, system_prompt=system_prompt + "\n" + topic_context)
    except Exception as e:
        reply = (
            f"**Career Copilot Advice** (Fallback Mode - LLM Error: {e})\n\n"
            f"### Key Focus for {profile.get('target_role', 'your career')}:\n"
            "- **Portfolio Polish**: Ensure case studies highlight measurable outcome metrics (e.g. +35% retention) rather than just process steps.\n"
            "- **ATS Keyword Alignment**: Match technical tooling and leadership keywords from target job specs.\n"
            "- **Direct Outreach**: Connect with design/engineering managers directly with short, 3-sentence notes."
        )

    return {
        "reply": reply,
        "role": "assistant",
        "topic": req.action_topic
    }



# --- Route Aliases for Flexible Client Compatibility ---
@app.post("/api/parse-job")
def parse_job_alias(req: ParseJobRequest):
    return parse_job_endpoint(req)

@app.post("/api/analyze-job")
def analyze_job_alias(req: AnalyzeJobRequest):
    return analyze_job_endpoint(req)

@app.post("/api/tailor-resume")
def tailor_resume_alias(req: TailorResumeRequest):
    return tailor_resume_endpoint(req)

@app.post("/api/draft-email")
def draft_email_alias(req: DraftEmailRequest):
    return draft_email_endpoint(req)

# --- Leads Management Hub (Phase 2) ---

@app.get("/api/leads")
def get_leads_endpoint(
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(500),
    offset: int = Query(0),
):
    """Query leads with filtering, search, and pagination."""
    leads = list_leads(category=category, status=status, search=search, limit=limit, offset=offset)
    return {"leads": leads, "count": len(leads)}


@app.get("/api/leads/stats")
def get_leads_stats_endpoint():
    """Retrieve aggregated stats for leads queue."""
    return get_leads_stats()


@app.get("/api/leads/{lead_id}")
def get_lead_endpoint(lead_id: int):
    """Retrieve single lead by ID."""
    lead = get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@app.post("/api/leads")
def create_lead_endpoint(req: LeadCreateRequest):
    """Create a single new lead."""
    lead_id = record_lead(
        company=req.company,
        role=req.role,
        country=req.country,
        category=req.category,
        contact_email=req.contact_email,
        contact_person=req.contact_person,
        website=req.website,
        job_url=req.job_url,
        status=req.status,
        notes=req.notes,
    )
    return {"status": "ok", "lead_id": lead_id}


@app.post("/api/leads/update-status")
def update_lead_status_endpoint(req: LeadStatusUpdateRequest):
    """Update status or notes for a lead."""
    ok = update_lead_status(req.lead_id, req.status, req.notes)
    return {"status": "ok" if ok else "error"}


@app.post("/api/leads/import-csv")
def import_csv_endpoint(req: CsvImportRequest):
    """Import CSV data into the leads pipeline."""
    imported_leads: List[Dict[str, Any]] = []
    if req.leads:
        imported_leads = req.leads
    elif req.csv_text:
        import csv
        import io
        import re
        f = io.StringIO(req.csv_text.strip())
        reader = csv.reader(f)
        rows = list(reader)
        if rows:
            headers = [h.strip().lower() for h in rows[0]]
            for row in rows[1:]:
                if not row or not any(str(c).strip() for c in row):
                    continue
                lead_dict = {}
                for idx, val in enumerate(row):
                    if idx < len(headers):
                        h = headers[idx]
                        lead_dict[h] = val.strip()
                
                # Heuristic header mapping
                company = (
                    lead_dict.get("company")
                    or lead_dict.get("company / agency")
                    or lead_dict.get("company / target")
                    or lead_dict.get("organization")
                    or (row[0] if len(row) > 0 else "")
                ).strip()
                if not company:
                    continue

                raw_email = (
                    lead_dict.get("email")
                    or lead_dict.get("contact_email")
                    or lead_dict.get("hr email")
                    or lead_dict.get("email address")
                    or lead_dict.get("contact")
                    or ""
                )
                m = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", raw_email)
                email = m.group(0) if m else raw_email.strip()

                role = (
                    lead_dict.get("role")
                    or lead_dict.get("matched role(s)")
                    or lead_dict.get("target_role")
                    or lead_dict.get("position")
                    or "Product Designer"
                ).strip()

                country = (
                    lead_dict.get("country")
                    or lead_dict.get("country / region")
                    or lead_dict.get("location")
                    or ""
                ).strip()

                cat_raw = (
                    lead_dict.get("category")
                    or lead_dict.get("type")
                    or lead_dict.get("type / category")
                    or "Direct"
                ).strip()
                category = "Agency" if "agency" in cat_raw.lower() else ("YC Startups" if "yc" in cat_raw.lower() else "Direct")

                status = (lead_dict.get("status") or "To Contact").strip()
                notes = (lead_dict.get("notes") or lead_dict.get("reason") or "").strip()
                url = (lead_dict.get("job_url") or lead_dict.get("website") or lead_dict.get("opening source url(s)") or "").strip()

                imported_leads.append({
                    "company": company,
                    "role": role,
                    "country": country,
                    "category": category,
                    "contact_email": email,
                    "job_url": url,
                    "source_sheet": "CSV Import",
                    "status": status,
                    "notes": notes,
                })

    if not imported_leads:
        raise HTTPException(status_code=400, detail="No valid leads found in import payload")

    inserted = bulk_insert_leads(imported_leads)
    credits_remaining = grant_unmask_credits(inserted)
    return {
        "status": "ok",
        "inserted": inserted,
        "total_imported": len(imported_leads),
        "credits_granted": inserted,
        "unmasks_remaining": credits_remaining,
        "stats": get_leads_stats(),
    }


@app.post("/api/leads/find-email")
def find_email_endpoint(req: FindEmailRequest):
    """
    Generate corporate email permutations, test domain DNS,
    and verify deliverability on candidate emails.
    """
    res = discover_and_score_emails(
        contact_name=req.contact_name,
        company=req.company,
        domain=req.domain,
        verify_top=2,
    )
    if req.lead_id and res.get("primary_email"):
        try:
            lead = get_lead(req.lead_id)
            if lead and not lead.get("contact_email"):
                update_lead_status(req.lead_id, lead.get("status", "To Contact"), lead.get("notes", ""))
        except Exception:
            pass
    return res


@app.get("/api/staging/leads-feed")
def get_staging_leads_feed(
    is_pro: bool = Query(False),
    limit: int = Query(25),
    refresh: bool = Query(False),
    category: Optional[str] = Query(None),
):
    """
    Staging Leads Feed with 25-Lead 72h limit for Free tier and full access for Pro.
    Free tier masks emails (e.g. j***@company.com) with is_locked=True.
    """
    all_leads = list_leads(category=category, limit=1000)
    all_leads = sorted(all_leads, key=lambda l: l.get("id", 0), reverse=True)
    
    if is_pro:
        return {
            "is_pro": True,
            "total_available": len(all_leads),
            "showing": min(limit, len(all_leads)),
            "leads": all_leads[:limit],
            "message": "Pro Access Active: Full 590+ database unlocked."
        }
    
    # Free tier: 25 randomized sample from latest 72h pool
    sample_pool = all_leads[:150] if len(all_leads) > 150 else all_leads
    sample_size = min(limit, len(sample_pool))
    sampled = random.sample(sample_pool, sample_size) if sample_pool else []
    
    masked_leads = []
    for ld in sampled:
        copy_lead = dict(ld)
        lead_id = copy_lead.get("id")
        unmasked = is_lead_unmasked(lead_id) if lead_id else False
        raw_email = copy_lead.get("contact_email") or ""

        if unmasked:
            copy_lead["is_masked"] = False
            copy_lead["is_locked"] = False
            copy_lead["is_unmasked"] = True
            masked_leads.append(copy_lead)
            continue

        if raw_email and "@" in raw_email:
            parts = raw_email.split("@", 1)
            user_part = parts[0]
            dom_part = parts[1]
            masked_user = (user_part[:1] + "***") if len(user_part) > 1 else "***"
            copy_lead["contact_email"] = f"{masked_user}@{dom_part}"
            copy_lead["is_masked"] = True
        else:
            copy_lead["contact_email"] = "🔒 Upgrade to Reveal"
            copy_lead["is_masked"] = True
        copy_lead["is_locked"] = True
        copy_lead["is_unmasked"] = False
        masked_leads.append(copy_lead)
        
    return {
        "is_pro": False,
        "sample_period": "Latest 72 Hours (25 Leads Sample)",
        "total_available": len(all_leads),
        "showing": len(masked_leads),
        "leads": masked_leads,
        "upgrade_cta": "Upgrade to Pro to unlock all 590+ leads and direct verified emails."
    }


@app.post("/api/staging/verify-pro")
def verify_staging_pro_endpoint(req: VerifyProRequest):
    """
    Verifies license code or activation passkey for Pro tier.
    """
    code = (req.passkey or "").strip()
    profile = get_profile()
    active_passkey = (profile.get("activation_passkey") or "").strip()
    
    valid_keys = {"PRO-AOE-2026", "LIFETIME-ACCESS", "VIP-SCALE", "PRO2026", "DUNDER-MIFFLIN-PRO"}
    if active_passkey:
        valid_keys.add(active_passkey.upper())
        valid_keys.add(active_passkey)
        
    if code.upper() in valid_keys or (active_passkey and code == active_passkey) or code.upper().startswith("PRO-AOE-"):
        update_user_quota(is_pro=True, tier="pro", license_key=code)
        return {
            "status": "ok",
            "is_pro": True,
            "message": "Pro Access Activated! All 590+ leads and direct emails unlocked."
        }
    else:
        raise HTTPException(
            status_code=403,
            detail="Invalid passkey or license code. Try 'PRO-AOE-2026' or check Settings."
        )


@app.get("/api/staging/rss-sources")
def get_staging_rss_sources_endpoint():
    """
    Returns available curated RSS channels for staging ingestion.
    """
    return {
        "status": "ok",
        "channels": [
            {
                "key": k,
                "name": v["name"],
                "url": v["url"],
                "category": v["category"],
                "default_role": v["default_role"]
            }
            for k, v in DEFAULT_RSS_FEEDS.items()
        ]
    }


@app.post("/api/staging/ingest-rss")
def ingest_staging_rss_endpoint(req: IngestRSSRequest):
    """
    Ingests live jobs from curated WeWorkRemotely and RemoteOK RSS feeds
    directly into the staging SQLite database with deterministic deduplication.
    """
    adapter = RSSFeedAdapter()
    all_leads = []

    # 1. SSRF Early Validation: Check custom RSS URL first if provided
    if req.custom_rss_url:
        try:
            adapter.validate_url(req.custom_rss_url)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"SSRF violation: {str(e)}")

    channels = req.channels if req.channels is not None else ["wwr_design", "remoteok_all"]
    errors = []

    # Sync selected pre-configured channels
    for ch in channels:
        try:
            leads = adapter.sync_channel(ch, max_items=req.max_per_feed)
            all_leads.extend(leads)
        except Exception as e:
            errors.append(f"Channel '{ch}' error: {str(e)}")

    # Sync custom RSS URL if provided
    if req.custom_rss_url:
        try:
            xml_text = adapter.fetch_feed_xml(req.custom_rss_url)
            custom_leads = adapter.parse_feed(xml_text, channel_key="Custom Feed")
            all_leads.extend(custom_leads[:req.max_per_feed])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Feed error: {str(e)}")

    if not all_leads and errors:
        raise HTTPException(status_code=400, detail="; ".join(errors))

    ingest_result = ingest_rss_leads(all_leads)
    ingest_result["status"] = "ok"
    ingest_result["channels_synced"] = channels
    ingest_result["errors"] = errors
    return ingest_result


# --- Autonomous Batch Engine (Phase 3) ---

@app.post("/api/batch/run")
def run_batch_endpoint(req: BatchRunRequest):
    """
    Autonomous batch queue runner.
    Iterates over selected lead IDs:
    1. Tailors 1-page CV
    2. Drafts personalized outreach email
    3. Handles dispatch mode (draft to Gmail / dry-run / live-send)
    4. Guards with activation passkey if required.
    """
    profile = get_profile()
    
    # Safety freeze: Live sends are completely on hold for testing
    if req.mode == "live_send":
        raise HTTPException(
            status_code=400,
            detail="Live email dispatch is currently locked on hold for testing. Only 'draft' (Gmail Drafts) and 'dry_run' modes are active."
        )

    results: List[Dict[str, Any]] = []
    gmail = GmailClient()
    builder = ResumeBuilder()

    cand_name = profile.get("full_name") or "Candidate Name"
    cand_email = profile.get("email") or "user@example.com"
    cand_portfolio = profile.get("portfolio_links", {}).get("portfolio") or "https://portfolio.example.com"

    for lid in req.lead_ids:
        lead = get_lead(lid)
        if not lead:
            continue
        
        company = lead.get("company") or "Target Company"
        role = lead.get("role") or "Senior Product Designer"
        contact_email = lead.get("contact_email") or ""
        country = lead.get("country") or ""

        # Build mock or fetched job
        job_text = f"Hiring for {role} at {company}. Requirements: end-to-end design ownership, user research, design systems."
        job = build_job(text=job_text, company=company, role=role, url=lead.get("job_url") or "")

        # 1. Tailor Resume & Render PDF
        slug = slugify(company)
        pdf_path = RESUMES_DIR / f"{slug}_resume.pdf"
        try:
            data, _ = builder.build(job)
            render_resume_pdf(data, pdf_path)
            has_pdf = True
        except Exception:
            has_pdf = False

        # 2. Draft Email Body & Subject
        subject = f"{role} — {cand_name}"
        email_body = (
            f"Hi {company} Team,\n\n"
            f"I came across your {role} opening and wanted to reach out directly. "
            f"I've been designing high-impact web and mobile products with a strong focus on systematic design and user experience. "
            f"You can review my selected live work at {cand_portfolio}.\n\n"
            f"My tailored one-page CV is attached for your review. I'd love to connect for a quick 10-minute conversation.\n\n"
            f"Best regards,\n"
            f"{cand_name}\n"
            f"{cand_email}"
        )

        # 3. Action Dispatch
        msg_id = ""
        action_status = ""
        notes = f"Batch mode: {req.mode}"

        if req.mode == "live_send":
            if profile.get("dry_run", True):
                action_status = "Dry Run (Sent Simulated)"
                msg_id = f"mock-dryrun-{int(time.time())}-{lid}"
            else:
                if contact_email:
                    try:
                        res = gmail.send_email(
                            to=contact_email,
                            subject=subject,
                            body=email_body,
                            attachment=pdf_path if has_pdf else None,
                        )
                        msg_id = res.get("id", "")
                        action_status = "Applied"
                    except Exception as e:
                        action_status = f"Send Error: {e}"
                else:
                    action_status = "No Email Address"

            update_lead_status(lid, "Applied", notes)
            record_application(
                company=company,
                role=role,
                url=lead.get("job_url") or "",
                contact_email=contact_email,
                status="Applied",
                match_score=92.0,
                resume_path=str(pdf_path) if has_pdf else "",
                email_subject=subject,
                email_body=email_body,
                gmail_message_id=msg_id,
                notes=notes,
            )

        elif req.mode == "draft":
            # Attempt to create real Gmail draft
            draft_success = False
            if contact_email and gmail.is_authenticated():
                try:
                    d_res = gmail.create_draft(
                        to=contact_email,
                        subject=subject,
                        body=email_body,
                        attachment=pdf_path if has_pdf else None,
                    )
                    msg_id = d_res.get("id", "")
                    draft_success = True
                    action_status = "Gmail Draft Created"
                except Exception:
                    draft_success = False

            if not draft_success:
                action_status = "Local Draft Saved"

            update_lead_status(lid, "Drafted", notes)
            record_application(
                company=company,
                role=role,
                url=lead.get("job_url") or "",
                contact_email=contact_email,
                status="Drafted",
                match_score=90.0,
                resume_path=str(pdf_path) if has_pdf else "",
                email_subject=subject,
                email_body=email_body,
                gmail_message_id=msg_id,
                notes=notes,
            )

        else:  # "dry_run"
            action_status = "Dry Run Generated"
            update_lead_status(lid, "Tailored (Dry Run)", notes)
            record_application(
                company=company,
                role=role,
                url=lead.get("job_url") or "",
                contact_email=contact_email,
                status="Dry Run",
                match_score=88.0,
                resume_path=str(pdf_path) if has_pdf else "",
                email_subject=subject,
                email_body=email_body,
                notes=notes,
            )

        results.append({
            "lead_id": lid,
            "company": company,
            "role": role,
            "email": contact_email,
            "status": action_status,
            "message_id": msg_id,
            "pdf": str(pdf_path) if has_pdf else "",
        })

    return {
        "status": "ok",
        "mode": req.mode,
        "processed_count": len(results),
        "results": results,
    }


# --- Follow-Up Automation (Phase 4) ---

@app.get("/api/tracker/follow-ups")
def get_follow_ups_endpoint():
    """
    Return all applications or leads due for a 7-day follow-up.
    Identifies leads applied >= 7 days ago without inbound responses.
    """
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("""
            SELECT a.*, 
                   (SELECT count(*) FROM inbound_replies ir WHERE ir.application_id = a.id OR ir.matched_company = a.company) as reply_count
            FROM applications a
            WHERE a.status IN ('Applied', 'Sent')
              AND (a.follow_up_date <= date('now') OR a.applied_date <= date('now', '-7 days'))
            ORDER BY a.id DESC
        """)
        rows = [dict(r) for r in cur.fetchall() if r["reply_count"] == 0]
        return {"follow_ups": rows, "count": len(rows)}


@app.post("/api/email/draft-follow-up")
def draft_follow_up_endpoint(req: FollowUpRequest):
    """
    Generate a concise, high-converting 2-sentence follow-up email.
    """
    profile = get_profile()
    cand_name = profile.get("full_name") or "Candidate Name"
    cand_portfolio = profile.get("portfolio_links", {}).get("portfolio") or "https://portfolio.example.com"

    company = "Target Company"
    role = "Product Designer"
    contact_email = ""

    if req.target_type == "application":
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM applications WHERE id = ?", (req.target_id,)).fetchone()
            if row:
                company = row["company"]
                role = row["role"]
                contact_email = row["contact_email"]
    else:
        lead = get_lead(req.target_id)
        if lead:
            company = lead["company"]
            role = lead["role"] or "Product Designer"
            contact_email = lead["contact_email"]

    subject = f"Re: {role} — Following up ({company})"
    body = (
        f"Hi {company} Team,\n\n"
        f"Following up on my note from last week regarding the {role} role. "
        f"I wanted to reiterate my interest in the team's design direction and check if you're still reviewing portfolios: {cand_portfolio}.\n\n"
        f"Happy to jump on a brief 10-minute introductory call if there's a fit.\n\n"
        f"Best regards,\n"
        f"{cand_name}"
    )

    return {
        "company": company,
        "role": role,
        "to": contact_email,
        "subject": subject,
        "body": body,
    }



# =============================================================================
# AURAJOBS SCRAPER & INGESTION ENDPOINTS (Step 2 & 3)
# =============================================================================

@app.post("/api/scraper/trigger")
async def trigger_scraper_endpoint(req: ScraperTriggerRequest):
    """Trigger background job scrape and ingestion run."""
    if req.freshness_hours <= 0 or req.freshness_hours > 720:
        raise HTTPException(status_code=400, detail="Invalid freshness_hours: must be between 1 and 720 hours.")
    valid_modes = ["express", "comprehensive"]
    if req.mode.lower() not in valid_modes:
        raise HTTPException(status_code=400, detail=f"Invalid mode: must be one of {valid_modes}.")
    
    clean_role = req.role.strip()
    if not clean_role or len(clean_role) > 100:
        raise HTTPException(status_code=400, detail="Role keyword must be between 1 and 100 characters.")

    res = await scraper_service.trigger_scrape(
        role=clean_role,
        seniority=req.seniority,
        geo=req.geography,
        freshness=req.freshness_hours,
        mode=req.mode
    )
    return res


@app.get("/api/scraper/status")
def get_scraper_status_endpoint():
    """Poll real-time execution progress, logs, and telemetry."""
    return scraper_service.get_status()


@app.get("/api/scraper/history")
def get_scraper_history_endpoint(limit: int = 15):
    """Retrieve audit history of previous scraper ingestion runs."""
    runs = get_ingestion_history(limit)
    return {"runs": runs, "count": len(runs)}


# =============================================================================
# EMAIL VERIFICATION & ZERO-AUTH QUALITY GATES (Step 1)
# =============================================================================

@app.post("/api/leads/verify-email")
def verify_lead_email_endpoint(req: EmailVerifyRequest):
    """Verify deliverability and disposable status of a lead contact email."""
    target_email = req.email
    if not target_email:
        lead = get_lead(req.lead_id)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        target_email = lead.get("contact_email", "")

    if not target_email:
        return {"status": "error", "message": "No email address found for this lead"}

    result = verify_email_deliverability(target_email)
    update_lead_email_verification(req.lead_id, result["status"], result)

    return {
        "status": "ok",
        "lead_id": req.lead_id,
        "email": target_email,
        "verification": result
    }


# =============================================================================
# AGENTIC SKILLS: FIRST-READER & AUTOPSY (Step 4)
# =============================================================================

@app.post("/api/outreach/audit-pitch")
def audit_pitch_endpoint(req: PitchAuditRequest):
    """First-Reader simulation: evaluates attention retention, conciseness, and hook strength."""
    report = audit_outreach_pitch(subject=req.subject, body=req.body)
    return report


@app.get("/api/applications/autopsy")
def applications_autopsy_endpoint(days: int = 7):
    """Stalled applications autopsy: diagnoses cause of death and ranks resurrection pulse."""
    report = run_applications_autopsy(days_silent_threshold=days)
    return report


# =============================================================================
# BACKGROUND AUTONOMOUS REFRESH LOOP
# =============================================================================

@app.on_event("startup")
async def start_autonomous_background_scheduler():
    """Background worker periodically polling fresh job feeds."""
    async def scheduler_task():
        # Wait 30 seconds after server launch
        await asyncio.sleep(30)
        while True:
            try:
                profile = get_profile()
                target_role = profile.get("target_role") or "Product Designer"
                # If auto-refresh is idle, run a gentle express sweep every 6 hours
                if not scraper_service.is_running:
                    logger.info("Autonomous scheduler: Triggering scheduled lead refresh...")
                    await scraper_service.trigger_scrape(role=target_role, mode="Express")
            except Exception as e:
                logger.error(f"Scheduler loop error: {e}")
            # Sleep 6 hours (21600 seconds)
            await asyncio.sleep(21600)

    asyncio.create_task(scheduler_task())

# =============================================================================
# HIVE MULTI-AGENT ORCHESTRATION (Munder Difflin Architecture)
# =============================================================================

class HiveOrchestrateRequest(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    text: str
    url: Optional[str] = None


@app.post("/api/hive/orchestrate")
def hive_orchestrate_endpoint(req: HiveOrchestrateRequest):
    """Run the Munder Difflin-inspired Hive multi-agent pipeline on a job description."""
    from ..hive import HiveCoordinator
    try:
        coordinator = HiveCoordinator()
        result = coordinator.run_pipeline(
            text=req.text,
            company=req.company,
            role=req.role,
            url=req.url
        )
        return {"status": "ok", "result": result}
    except Exception as e:
        logger.error(f"Hive pipeline error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/hive/status")
def hive_status_endpoint():
    """Retrieve Hive multi-agent coordinator status, circuit breaker, and recent ledgers."""
    from ..hive import HiveCoordinator, HIVE_DIR
    coordinator = HiveCoordinator()
    recent_ledgers = sorted(list(HIVE_DIR.glob("*.json")), key=lambda p: p.stat().st_mtime, reverse=True)[:5]
    ledgers_summary = []
    for p in recent_ledgers:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            ledgers_summary.append({
                "session_id": data.get("session_id"),
                "status": data.get("board", {}).get("status"),
                "tasks_count": len(data.get("tasks", [])),
                "artifacts": data.get("board", {}).get("artifacts", {})
            })
        except Exception:
            continue
    return {
        "circuit_breaker": {
            "state": coordinator.breaker.state,
            "failures": coordinator.breaker.failures
        },
        "agents": ["michael", "jim", "dwight", "pam", "ryan", "angela", "toby", "scout", "resume_architect", "copywriter", "quality_reviewer", "supervisor"],
        "characters": [
            {"id": "michael", "name": "Michael Scott", "role": "Regional Manager", "desc": "Hive god-agent dispatcher & team leader"},
            {"id": "jim", "name": "Jim Halpert", "role": "Job Scout", "desc": "Public job board search & JD keyword extraction"},
            {"id": "dwight", "name": "Dwight Schrute", "role": "Resume Architect", "desc": "Militant 1-page Bahnschrift PDF builder"},
            {"id": "pam", "name": "Pam Beesly", "role": "Intake & Reception", "desc": "Candidate evidence bank & portfolio intake"},
            {"id": "ryan", "name": "Ryan Howard", "role": "Cold Outreach Copywriter", "desc": "3-sentence high-conversion pitch creator"},
            {"id": "angela", "name": "Angela Martin", "role": "Quality & Compliance", "desc": "First-Reader retention & WCAG AA contrast auditor"},
            {"id": "toby", "name": "Toby Flenderson", "role": "Inbound Recruiter Radar", "desc": "Gmail API recruiter reply & invite scanner"}
        ],
        "recent_runs": ledgers_summary
    }


# =============================================================================
# 90-SECOND AUTONOMOUS CONVERSION MACHINE ENDPOINTS
# =============================================================================

@app.post("/api/autopilot/run-90s")
def run_autopilot_90s_endpoint(req: AutoPilotRunRequest):
    """
    Executes the unified 90-second co-pilot pipeline:
    ATS keyword gap scoring, recruiter email discovery, 1-page Bahnschrift PDF CV,
    attention-scored cold pitch, application logging, and Day +7 follow-up schedule.
    """
    try:
        result = autopilot_service.run_90s_pipeline(
            lead_id=req.lead_id,
            company=req.company,
            role=req.role,
            job_url=req.job_url,
            jd_text=req.jd_text,
            contact_email=req.contact_email,
            contact_person=req.contact_person,
            profession=req.profession or "product-designer",
            llm_provider=req.llm_provider,
            llm_api_key=req.llm_api_key,
        )
        return result
    except Exception as exc:
        logger.exception(f"AutoPilot 90s pipeline error: {exc}")
        raise HTTPException(status_code=500, detail=f"AutoPilot execution error: {str(exc)}")


@app.get("/api/conversion/telemetry")
def get_conversion_telemetry_endpoint():
    """
    Returns real-time campaign conversion telemetry:
    100-target campaign progress, cycle time velocity (<90s), and recruiter response rate vs 18% benchmark.
    """
    return autopilot_service.get_conversion_telemetry()


# =============================================================================
# COMMERCIAL MICRO-SAAS ASSET: BILLING, UNMASK CREDITS & SHOWCASE
# =============================================================================

@app.get("/api/billing/tiers")
def get_billing_tiers_endpoint():
    """Returns commercial pricing tiers catalog."""
    return {
        "status": "ok",
        "tiers": [
            {
                "id": "free",
                "name": "Free Hunter",
                "price": "$0",
                "period": "forever",
                "badge": "Active Default",
                "leads_limit": "25 fresh leads / 72h sample",
                "unmasks_included": 3,
                "features": [
                    "25 curated fresh leads every 72 hours",
                    "3 direct recruiter email unmask credits",
                    "Give-to-Get: +1 credit per imported lead",
                    "Basic ATS keyword check & score",
                    "1-Page ReportLab CV preview"
                ]
            },
            {
                "id": "starter",
                "name": "Starter Hunter",
                "price": "$19",
                "period": "/mo",
                "badge": "Entry",
                "leads_limit": "100 leads / week",
                "unmasks_included": 50,
                "features": [
                    "100 fresh leads per week",
                    "50 recruiter email unmasks & MX check",
                    "1-Page Bahnschrift PDF CV export",
                    "Standard cold outreach pitch drafts",
                    "Email deliverability verification"
                ]
            },
            {
                "id": "pro",
                "name": "Pro Conversion Co-Pilot",
                "price": "$49",
                "period": "/mo",
                "badge": "Most Popular · High ROI",
                "popular": True,
                "leads_limit": "Unlimited (590+ database)",
                "unmasks_included": "Unlimited",
                "features": [
                    "Full access to 590+ target companies",
                    "Unlimited verified direct recruiter emails",
                    "⚡ 90-Second Autonomous Conversion Machine",
                    "First-Reader attention score optimizer (90+ rating)",
                    "Automated 7-Day Follow-Up Sequencer",
                    "Priority RSS & JobSpy multi-board sync"
                ]
            },
            {
                "id": "lifetime",
                "name": "Lifetime Hunter",
                "price": "$99",
                "period": "one-time",
                "badge": "Best Value",
                "leads_limit": "Lifetime Unlimited",
                "unmasks_included": "Lifetime Unlimited",
                "features": [
                    "Lifetime access to all future lead updates",
                    "Unlimited scraper & private RSS channel runs",
                    "One-click CSV & JSON lead exports",
                    "VIP Discord community & feature access"
                ]
            }
        ]
    }


@app.get("/api/billing/user-quota")
def get_user_quota_endpoint():
    """Returns active billing tier, remaining unmask credits, and Pro status."""
    return get_user_quota()


@app.post("/api/billing/checkout")
def billing_checkout_endpoint(req: BillingCheckoutRequest):
    """
    Processes simulated subscription/lifetime checkout, generates an authentic license passkey,
    and updates user quota in SQLite.
    """
    tier = req.tier.lower().strip()
    if tier not in ["starter", "pro", "lifetime"]:
        tier = "pro"

    import secrets
    random_hex = secrets.token_hex(4).upper()
    license_key = f"PRO-AOE-{random_hex}" if tier != "lifetime" else f"LIFETIME-AOE-{random_hex}"

    is_pro = True
    unmasks = 99999 if tier in ["pro", "lifetime"] else 50

    quota = update_user_quota(
        unmasks_remaining=unmasks,
        is_pro=is_pro,
        tier=tier,
        license_key=license_key
    )

    return {
        "status": "success",
        "message": f"Payment processed successfully! {tier.title()} tier activated.",
        "tier": tier,
        "is_pro": True,
        "license_key": license_key,
        "quota": quota
    }


@app.post("/api/leads/unmask")
def unmask_lead_endpoint(req: UnmaskLeadRequest):
    """
    Consumes 1 unmask credit for Free tier users (or unlimited for Pro),
    marks lead as unmasked in SQLite, and returns verified email.
    """
    result = consume_unmask_credit(req.lead_id)
    if result.get("status") == "quota_exceeded":
        raise HTTPException(
            status_code=403,
            detail="No unmask credits remaining. Upgrade to Pro or import CSV leads (+1 credit per lead)."
        )
    if result.get("status") == "error":
        raise HTTPException(status_code=404, detail=result.get("message"))
    return result


@app.get("/api/public/showcase")
def get_public_showcase_endpoint():
    """
    Public preview endpoint for community sharing of sanitized lead batches.
    """
    all_leads = list_leads(limit=25)
    sanitized = []
    for l in all_leads:
        sanitized.append({
            "company": l.get("company"),
            "role": l.get("role") or "Product Designer",
            "category": l.get("category") or "Direct",
            "country": l.get("country") or "Remote",
            "website": l.get("website") or "",
            "sample_snippet": (l.get("notes") or "")[:120]
        })
    return {
        "status": "ok",
        "community_name": "AOE Open Recruiter Showcase",
        "total_targets_catalog": 590,
        "sample_preview_count": len(sanitized),
        "leads": sanitized,
        "share_url": "http://127.0.0.1:8002/#leads"
    }


# =============================================================================
# PUBLIC JOB BOARDS API (Jim Halpert's Scout Desk)
# =============================================================================

@app.get("/api/public-jobs/search")
def search_public_jobs_endpoint(query: Optional[str] = "designer", limit: int = 10):
    """Query live public job feeds (Arbeitnow + tech fallbacks) for Jim's Scout desk."""
    import urllib.request
    results = []
    q_clean = (query or "").strip().lower()

    # Attempt live Arbeitnow public API
    try:
        req = urllib.request.Request(
            "https://www.arbeitnow.com/api/job-board-api",
            headers={"User-Agent": "AOE-Scout/1.0"}
        )
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for item in data.get("data", []):
                t = item.get("title", "")
                c = item.get("company_name", "")
                desc = item.get("description", "")
                tags = item.get("tags", [])
                text_to_match = f"{t} {c} {' '.join(tags)} {desc}".lower()
                if not q_clean or q_clean in text_to_match:
                    results.append({
                        "company": c,
                        "role": t,
                        "location": item.get("location", "Remote"),
                        "url": item.get("url", ""),
                        "tags": tags[:4],
                        "snippet": (desc[:180] + "...") if len(desc) > 180 else desc,
                        "source": "Arbeitnow Live Feed"
                    })
                if len(results) >= limit:
                    break
    except Exception as err:
        logger.debug(f"Live job board fetch skipped/failed: {err}")

    # Rich curated backup tech jobs to ensure instant, reliable Scout queries
    curated_pool = [
        {
            "company": "Spotify",
            "role": "Senior Product Designer",
            "location": "Stockholm / Remote",
            "url": "https://lifeatspotify.com/jobs",
            "tags": ["Design Systems", "Figma", "Mobile UI", "Audio UX"],
            "snippet": "Spotify is seeking a Senior Product Designer to drive personalized music discovery experiences for 600M+ global listeners.",
            "source": "Scout Curated Feed"
        },
        {
            "company": "Stripe",
            "role": "Frontend Infrastructure Engineer",
            "location": "San Francisco / Remote",
            "url": "https://stripe.com/jobs",
            "tags": ["TypeScript", "React", "Web Performance", "API Design"],
            "snippet": "Craft developer platforms and lightning-fast checkout experiences handling billions of dollars in global commerce.",
            "source": "Scout Curated Feed"
        },
        {
            "company": "Figma",
            "role": "Design Systems Engineer",
            "location": "New York / Remote",
            "url": "https://figma.com/careers",
            "tags": ["Figma Plugins", "Canvas 2D", "WebGL", "TypeScript"],
            "snippet": "Build the next generation of multiplayer design tools, interactive tokens, and high-velocity vector editing primitives.",
            "source": "Scout Curated Feed"
        },
        {
            "company": "Linear",
            "role": "Senior Product Engineer",
            "location": "Remote (Global)",
            "url": "https://linear.app/careers",
            "tags": ["TypeScript", "React", "Desktop Apps", "Keyboard First"],
            "snippet": "Craft magical, keyboard-first issue tracking and project planning tools for modern software development teams.",
            "source": "Scout Curated Feed"
        },
        {
            "company": "Apple",
            "role": "Software Engineer - AI Tools",
            "location": "Cupertino / Remote",
            "url": "https://jobs.apple.com",
            "tags": ["Python", "FastAPI", "Machine Learning", "Workflow Automation"],
            "snippet": "Create developer toolchains, AI agent orchestration pipelines, and intelligent interfaces across Apple platforms.",
            "source": "Scout Curated Feed"
        },
        {
            "company": "Airbnb",
            "role": "Lead UX Engineer",
            "location": "San Francisco / Remote",
            "url": "https://careers.airbnb.com",
            "tags": ["Design Systems", "WCAG AA", "React", "Micro-Interactions"],
            "snippet": "Lead accessibility, micro-animations, and unified design token standards across Airbnb web and mobile platforms.",
            "source": "Scout Curated Feed"
        },
        {
            "company": "GitHub",
            "role": "Full Stack Engineer (Copilot Team)",
            "location": "Remote",
            "url": "https://github.com/about/careers",
            "tags": ["Python", "TypeScript", "LLM Pipelines", "Developer Tools"],
            "snippet": "Build developer-first generative AI agent capabilities integrated directly into the developer workflow.",
            "source": "Scout Curated Feed"
        }
    ]

    for item in curated_pool:
        if len(results) >= limit:
            break
        text_to_match = f"{item['company']} {item['role']} {' '.join(item['tags'])} {item['snippet']}".lower()
        if not q_clean or q_clean in text_to_match:
            if not any(r["company"] == item["company"] and r["role"] == item["role"] for r in results):
                results.append(item)

    return {"query": query, "count": len(results), "jobs": results}


# =============================================================================
# REAL-TIME EVENT STREAMING & SUPERVISOR CHAT
# =============================================================================

_HIVE_EVENT_QUEUES: List[asyncio.Queue] = []

def _on_hive_event(payload: Dict[str, Any]) -> None:
    loop = None
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        pass
    for q in list(_HIVE_EVENT_QUEUES):
        if loop and loop.is_running():
            loop.call_soon_threadsafe(q.put_nowait, payload)
        else:
            try:
                q.put_nowait(payload)
            except Exception:
                pass

from ..hive import subscribe_hive_events
subscribe_hive_events(_on_hive_event)


@app.get("/api/hive/stream")
async def hive_stream_endpoint():
    """Server-Sent Events endpoint streaming real-time Hive agent state to the 2D office canvas."""
    q: asyncio.Queue = asyncio.Queue()
    _HIVE_EVENT_QUEUES.append(q)

    async def event_generator():
        try:
            yield f"data: {json.dumps({'type': 'connected', 'message': 'Subscribed to AOE Operations Floor event stream'})}\n\n"
            while True:
                try:
                    payload = await asyncio.wait_for(q.get(), timeout=15.0)
                    yield f"data: {json.dumps(payload)}\n\n"
                except asyncio.TimeoutError:
                    yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"
        finally:
            if q in _HIVE_EVENT_QUEUES:
                _HIVE_EVENT_QUEUES.remove(q)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


class HiveChatRequest(BaseModel):
    message: str
    context_lead_id: Optional[int] = None


@app.post("/api/hive/chat")
async def hive_chat_endpoint(req: HiveChatRequest):
    """Chat with Michael Scott (Regional Manager) to dispatch tasks or query the floor."""
    msg = req.message.strip().lower()
    from ..hive import HiveCoordinator
    
    if "that's what she said" in msg or "thats what she said" in msg:
        return {
            "reply": 'Michael Scott: "THAT\'S WHAT SHE SAID! Ha! Classic. Now back to business. Which company are we targeting today?"',
            "action": "banter"
        }

    if "tailor" in msg or "apply" in msg or "run" in msg or "dispatch" in msg:
        target_lead = None
        if req.context_lead_id:
            target_lead = get_lead(req.context_lead_id)
        else:
            leads = list_leads(limit=20)
            for l in leads:
                if l.get("status") in ["To Contact", "Not Contacted", None]:
                    target_lead = l
                    break
        
        if target_lead:
            company = target_lead.get("company", "Target")
            role = target_lead.get("role", "Product Designer")
            text = f"{company} is looking for a {role}. Requirements: end-to-end UX/UI, design systems, Figma, agile collaboration."
            
            coordinator = HiveCoordinator()
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, lambda: coordinator.run_pipeline(
                text=text,
                company=company,
                role=role,
                url=target_lead.get("job_url") or target_lead.get("website")
            ))
            return {
                "reply": f'Michael Scott: "Boom! Dispatched the Scranton team for **{company}** ({role}). Jim (Scout), Dwight (Architect), Ryan (Copywriter), and Angela (Reviewer) nailed it!"',
                "action": "orchestrated",
                "result": result
            }
        else:
            return {
                "reply": 'Michael Scott: "I\'m ready! Paste a job description or pick a lead from your Leads Queue, and I\'ll send Jim (Scout) and Dwight (Architect) straight to work."',
                "action": "prompt_jd"
            }

    elif "status" in msg or "how" in msg or "who" in msg or "report" in msg:
        apps = list_applications()
        leads = list_leads(limit=500)
        return {
            "reply": f'Michael Scott: "Dunder Mifflin Scranton Regional Manager reporting! We have **{len(leads)} target leads** in the queue, **{len(apps)} applications** logged. Jim (Scout) is on the phones, Dwight (Architect) is guarding the paper, Pam is managing reception, Ryan is on his laptop, Angela is auditing, and Toby is in the annex."',
            "action": "status"
        }

    elif "scan" in msg or "reply" in msg or "inbox" in msg or "toby" in msg:
        client = GmailClient()
        replies = client.check_replies(max_results=10)
        return {
            "reply": f'Toby Flenderson: "Scanned Gmail in the breakroom... found **{len(replies)} recruiter response(s)** in your connected account."',
            "action": "scanned",
            "replies": replies
        }

    else:
        return {
            "reply": f'Michael Scott: "Regional Manager standing by! Tell me: \'Tailor next lead\', \'Scan recruiter replies\', or \'Search jobs at Spotify\'. Or click on Jim, Dwight, or Pam\'s desk!"',
            "action": "default"
        }


if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

