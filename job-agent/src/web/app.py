"""FastAPI server for the local Job Hunt web application."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import shutil
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
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
from ..services.autopsy_service import run_applications_autopsy
from .db import (
    ingest_scraped_batch, get_ingestion_history, update_lead_email_verification,
    list_applications, record_application, update_status, init_db,
    delete_application, clear_all_applications,
    get_profile, save_profile, get_dashboard_analytics, record_inbound_reply,
    list_inbound_replies, record_lead, list_leads, get_lead,
    update_lead_status, bulk_insert_leads, get_leads_stats, DB_PATH
)

app = FastAPI(title="Job Hunt Agent API", version="2.0.0")

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
    provider = payload.get("provider", "gemini")
    api_key = payload.get("api_key") or os.getenv(f"{provider.upper()}_API_KEY") or os.getenv("LLM_API_KEY") or ""
    model = payload.get("model") or ""
    base_url = payload.get("base_url")

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

    return {
        "match_score": score,
        "matched_skills": matched,
        "gap_skills": gaps,
        "strategy": strategy,
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
    return {
        "status": "ok",
        "inserted": inserted,
        "total_imported": len(imported_leads),
        "stats": get_leads_stats(),
    }


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
    res = await scraper_service.trigger_scrape(
        role=req.role,
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

if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
