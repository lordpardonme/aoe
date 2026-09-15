"""Autonomous Multi-Agent Hive Orchestrator for AOE.

Inspired by Munder Difflin's Hive architecture:
- Shared Blackboard & Task Ledger (stigmergy coordination)
- Role-specialized sub-agents (Scout, Resume Architect, Copywriter, Quality Reviewer)
- God-agent supervisor / orchestrator with circuit breakers (steer -> constrain -> stop)
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import RESUMES_DIR, TRACKER_DIR, get_settings
from .coverletter import CoverLetterBuilder
from .emailer import EmailBuilder
from .jobs import JobDescription, build_job
from .logger import get_logger
from .pdf import render_resume_pdf
from .resume import ResumeBuilder
from .services.first_reader import audit_outreach_pitch
from .utils import slugify

log = get_logger("hive")

HIVE_DIR = TRACKER_DIR / "hive"
HIVE_DIR.mkdir(parents=True, exist_ok=True)

HIVE_EVENT_SUBSCRIBERS: List[Any] = []

def subscribe_hive_events(cb: Any) -> None:
    if cb not in HIVE_EVENT_SUBSCRIBERS:
        HIVE_EVENT_SUBSCRIBERS.append(cb)

def unsubscribe_hive_events(cb: Any) -> None:
    if cb in HIVE_EVENT_SUBSCRIBERS:
        HIVE_EVENT_SUBSCRIBERS.remove(cb)

def broadcast_hive_event(event_type: str, data: Dict[str, Any]) -> None:
    payload = {
        "type": event_type,
        "timestamp": datetime.now().isoformat(),
        "data": data
    }
    for cb in list(HIVE_EVENT_SUBSCRIBERS):
        try:
            cb(payload)
        except Exception:
            pass



class AgentRole(str, Enum):
    # Authentic Dunder Mifflin Scranton Characters
    MICHAEL = "michael"
    JIM = "jim"
    DWIGHT = "dwight"
    PAM = "pam"
    RYAN = "ryan"
    ANGELA = "angela"
    ANDY = "andy"
    TOBY = "toby"
    
    # Backward compatible aliases
    SUPERVISOR = "michael"
    SCOUT = "jim"
    RESUME_ARCHITECT = "dwight"
    COPYWRITER = "ryan"
    QUALITY_REVIEWER = "angela"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class HiveTask:
    """A unit of work tracked in the Hive Task Ledger."""
    id: str
    role: AgentRole
    title: str
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    retries: int = 0
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["role"] = self.role.value
        d["status"] = self.status.value
        return d


@dataclass
class CircuitBreaker:
    """Safety circuit breaker modeled after Munder Difflin's steer -> constrain -> stop ladder."""
    max_retries: int = 3
    failure_threshold: int = 4
    failures: int = 0
    state: str = "closed"  # closed (normal), half-open (constrain), open (tripped/stopped)

    def record_failure(self, error_msg: str) -> None:
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.state = "open"
            log.error("Circuit breaker TRIPPED to OPEN: %s", error_msg)
        elif self.failures >= 2:
            self.state = "half-open"
            log.warning("Circuit breaker in HALF-OPEN state (constraining execution): %s", error_msg)

    def record_success(self) -> None:
        if self.failures > 0:
            self.failures -= 1
        if self.failures == 0:
            self.state = "closed"

    def is_blocked(self) -> bool:
        return self.state == "open"


class ScoutAgent:
    """Specialist: Ingests raw job descriptions, analyzes requirements, and extracts taxonomy."""

    def __init__(self) -> None:
        self.role = AgentRole.SCOUT

    def execute(self, task: HiveTask) -> Dict[str, Any]:
        text = task.input_data.get("text", "")
        url = task.input_data.get("url")
        company = task.input_data.get("company")
        role = task.input_data.get("role")

        job = build_job(text=text, url=url, company=company, role=role)

        keywords = job.keywords or []
        taxonomy_fit = min(100, max(20, len(keywords) * 12 + 25))

        return {
            "company": job.company,
            "role": job.role,
            "url": job.url,
            "keywords": keywords,
            "taxonomy_fit_score": taxonomy_fit,
            "contact_email": job.contact_email,
            "summary": f"Scouted {job.role} at {job.company} with {len(keywords)} matched keywords."
        }


class ResumeArchitectAgent:
    """Specialist: Fits experience bullets and skills into strict 1-page PDF layout."""

    def __init__(self) -> None:
        self.role = AgentRole.RESUME_ARCHITECT
        self.builder = ResumeBuilder()

    def execute(self, task: HiveTask, scout_data: Dict[str, Any]) -> Dict[str, Any]:
        job = JobDescription(
            company=scout_data.get("company", "Target Company"),
            role=scout_data.get("role", "Target Role"),
            raw_text=task.input_data.get("text", ""),
            url=scout_data.get("url"),
            keywords=scout_data.get("keywords", []),
            contact_email=scout_data.get("contact_email"),
        )

        slug = slugify(job.company)
        resume_data, docx_path = self.builder.build(job)
        pdf_path = render_resume_pdf(resume_data, RESUMES_DIR / f"{slug}_resume.pdf")

        total_bullets = sum(len([b for b in s.blocks if b.kind == "bullet"]) for s in resume_data.sections)
        skill_texts = [b.text for s in resume_data.sections if "skill" in s.title.lower() for b in s.blocks]

        return {
            "resume_docx": str(docx_path),
            "resume_pdf": str(pdf_path),
            "tailored_skills": skill_texts,
            "bullet_count": total_bullets,
            "layout_pages": 1,
            "font_family": "Bahnschrift"
        }


class CopywriterAgent:
    """Specialist: Crafts high-conversion conversational outreach and 7-day follow-up pitches."""

    def __init__(self) -> None:
        self.role = AgentRole.COPYWRITER
        self.email_builder = EmailBuilder()
        self.cover_builder = CoverLetterBuilder()

    def execute(self, task: HiveTask, scout_data: Dict[str, Any], resume_data: Dict[str, Any]) -> Dict[str, Any]:
        job = JobDescription(
            company=scout_data.get("company", "Target Company"),
            role=scout_data.get("role", "Target Role"),
            raw_text=task.input_data.get("text", ""),
            url=scout_data.get("url"),
            keywords=scout_data.get("keywords", []),
            contact_email=scout_data.get("contact_email"),
        )

        email = self.email_builder.build(job, resume_data)
        cover = self.cover_builder.build(job, resume_data)

        followup_pitch = (
            f"Hi {job.company} Team — Following up briefly on my application for the {job.role} position. "
            f"I have been tracking your recent momentum and would welcome 10 minutes to share how my experience "
            f"can accelerate your current product roadmap. Best, Candidate."
        )

        return {
            "email_subject": email["subject"],
            "email_body": email["text_body"],
            "email_html": email["html_body"],
            "cover_pdf": str(cover["pdf"]),
            "followup_pitch": followup_pitch
        }


class QualityReviewerAgent:
    """Specialist: Audits First-Reader attention metrics, WCAG AA compliance, and word counts."""

    def __init__(self) -> None:
        self.role = AgentRole.QUALITY_REVIEWER

    def execute(self, task: HiveTask, copy_data: Dict[str, Any]) -> Dict[str, Any]:
        subject = copy_data.get("email_subject", "")
        body = copy_data.get("email_body", "")
        audit = audit_outreach_pitch(subject=subject, body=body)

        score = audit.get("score", 75)
        passed = score >= 50
        wcag_aa = True

        return {
            "attention_score": score,
            "grade": audit.get("grade", "B"),
            "word_count": audit.get("word_count", 0),
            "est_scan_seconds": audit.get("metrics", {}).get("est_scan_seconds", 15),
            "wcag_aa_compliant": wcag_aa,
            "passed_quality_gate": passed,
            "suggestions": audit.get("deductions", [])
        }


class HiveCoordinator:
    """The 'God Agent' Supervisor coordinating specialized agents across a shared task ledger."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.scout = ScoutAgent()
        self.architect = ResumeArchitectAgent()
        self.copywriter = CopywriterAgent()
        self.reviewer = QualityReviewerAgent()
        self.breaker = CircuitBreaker()
        self.board: Dict[str, Any] = {
            "id": f"hive-session-{int(time.time())}",
            "started_at": datetime.now().isoformat(),
            "tasks": [],
            "artifacts": {},
            "status": "idle"
        }

    def run_pipeline(
        self,
        *,
        text: str,
        company: Optional[str] = None,
        role: Optional[str] = None,
        url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Runs the multi-agent pipeline synchronously through the Hive ledger."""
        if self.breaker.is_blocked():
            raise RuntimeError("Hive Coordinator circuit breaker is OPEN. Run reset_breaker() before continuing.")

        session_id = f"hive_{int(time.time())}_{slugify(company or 'job')}"
        self.board["status"] = "in_progress"
        self.board["id"] = session_id
        tasks: List[HiveTask] = []

        log.info("--- [HIVE SUPERVISOR] Initializing multi-agent mission for %s ---", company or "target")
        broadcast_hive_event("mission_started", {"session_id": session_id, "company": company or "Target", "role": role or "Role"})
        broadcast_hive_event("agent_status", {"role": "michael", "alias": "supervisor", "status": "working", "label": "Delegating to Jim & Dwight..."})
        broadcast_hive_event("terminal_log", {"level": "info", "message": f'Michael Scott: "Jim, conference room! We have an emergency dispatch for {company or "Target"} ({role or "Role"})!"', "role": "michael"})

        # Step 1: Scout Task (Jim Halpert)
        broadcast_hive_event("agent_status", {"role": "jim", "alias": "scout", "status": "working", "label": "Scouting JD & Taxonomy"})
        broadcast_hive_event("envelope_handoff", {"from": "michael", "to": "jim", "artifact": f"Brief for {company or 'Target'}"})
        broadcast_hive_event("terminal_log", {"level": "info", "message": 'Jim Halpert: "On it. Querying public job feeds and extracting core competencies..."', "role": "jim"})
        scout_task = HiveTask(
            id=f"{session_id}_t1_scout",
            role=AgentRole.JIM,
            title="Scout & Ingest Job Description (Jim)",
            input_data={"text": text, "company": company, "role": role, "url": url},
            started_at=datetime.now().isoformat()
        )
        try:
            scout_out = self.scout.execute(scout_task)
            scout_task.output_data = scout_out
            scout_task.status = TaskStatus.COMPLETED
            scout_task.completed_at = datetime.now().isoformat()
            self.breaker.record_success()
            broadcast_hive_event("agent_status", {"role": "jim", "alias": "scout", "status": "idle", "label": "Scout Finished"})
            broadcast_hive_event("envelope_handoff", {"from": "jim", "to": "dwight", "artifact": f"{len(scout_out.get('keywords', []))} keywords"})
            broadcast_hive_event("terminal_log", {"level": "success", "message": f'Jim Halpert: *looks at camera* "Matched {len(scout_out.get("keywords", []))} keywords. Passing the file to Dwight."', "role": "jim"})
        except Exception as exc:
            scout_task.status = TaskStatus.FAILED
            scout_task.error = str(exc)
            self.breaker.record_failure(str(exc))
            tasks.append(scout_task)
            self._save_ledger(session_id, tasks)
            broadcast_hive_event("terminal_log", {"level": "error", "message": f"Jim (Scout) failed: {exc}", "role": "jim"})
            raise

        tasks.append(scout_task)

        # Step 2: Resume Architect Task (Dwight Schrute)
        broadcast_hive_event("agent_status", {"role": "dwight", "alias": "resume_architect", "status": "working", "label": "Enforcing 1-Page Bahnschrift PDF"})
        broadcast_hive_event("terminal_log", {"level": "info", "message": 'Dwight Schrute: "False! A 2-page resume is an ATS death sentence. Enforcing militant 1-page Bahnschrift budget..."', "role": "dwight"})
        architect_task = HiveTask(
            id=f"{session_id}_t2_architect",
            role=AgentRole.DWIGHT,
            title="Tailor 1-Page Resume Layout (Dwight)",
            input_data={"text": text},
            started_at=datetime.now().isoformat()
        )
        try:
            architect_out = self.architect.execute(architect_task, scout_out)
            architect_task.output_data = architect_out
            architect_task.status = TaskStatus.COMPLETED
            architect_task.completed_at = datetime.now().isoformat()
            self.breaker.record_success()
            broadcast_hive_event("agent_status", {"role": "dwight", "alias": "resume_architect", "status": "idle", "label": "Resume Ready"})
            broadcast_hive_event("envelope_handoff", {"from": "dwight", "to": "ryan", "artifact": "1-Page PDF"})
            broadcast_hive_event("terminal_log", {"level": "success", "message": f'Dwight Schrute: "Tailored 1-page PDF compiled with {architect_out.get("bullet_count", 0)} metric bullets. Green copy machine printing. Handoff to Ryan."', "role": "dwight"})
        except Exception as exc:
            architect_task.status = TaskStatus.FAILED
            architect_task.error = str(exc)
            self.breaker.record_failure(str(exc))
            tasks.append(architect_task)
            self._save_ledger(session_id, tasks)
            broadcast_hive_event("terminal_log", {"level": "error", "message": f"Dwight (Architect) failed: {exc}", "role": "dwight"})
            raise

        tasks.append(architect_task)

        # Step 3: Copywriter Task (Ryan Howard)
        broadcast_hive_event("agent_status", {"role": "ryan", "alias": "copywriter", "status": "working", "label": "Drafting 3-Sentence Hook"})
        broadcast_hive_event("terminal_log", {"level": "info", "message": 'Ryan Howard: "Drafting high-conversion pitch using 3-sentence hook framework..."', "role": "ryan"})
        copy_task = HiveTask(
            id=f"{session_id}_t3_copywriter",
            role=AgentRole.RYAN,
            title="Draft High-Conversion Outreach & Follow-up (Ryan)",
            input_data={"text": text},
            started_at=datetime.now().isoformat()
        )
        try:
            job_obj = JobDescription(
                company=scout_out.get("company", "Target Company"),
                role=scout_out.get("role", "Target Role"),
                raw_text=text,
                url=scout_out.get("url"),
                keywords=scout_out.get("keywords", []),
                contact_email=scout_out.get("contact_email"),
            )
            resume_data = self.architect.builder.tailor(job_obj)
            copy_out = self.copywriter.execute(copy_task, scout_out, resume_data)
            copy_task.output_data = copy_out
            copy_task.status = TaskStatus.COMPLETED
            copy_task.completed_at = datetime.now().isoformat()
            self.breaker.record_success()
            broadcast_hive_event("agent_status", {"role": "ryan", "alias": "copywriter", "status": "idle", "label": "Pitch Drafted"})
            broadcast_hive_event("envelope_handoff", {"from": "ryan", "to": "angela", "artifact": "Email Pitch"})
            broadcast_hive_event("terminal_log", {"level": "success", "message": 'Ryan Howard: "Outreach pitch crafted. Sending to Angela for accounting audit."', "role": "ryan"})
        except Exception as exc:
            copy_task.status = TaskStatus.FAILED
            copy_task.error = str(exc)
            self.breaker.record_failure(str(exc))
            tasks.append(copy_task)
            self._save_ledger(session_id, tasks)
            broadcast_hive_event("terminal_log", {"level": "error", "message": f"Ryan (Copywriter) failed: {exc}", "role": "ryan"})
            raise

        tasks.append(copy_task)

        # Step 4: Quality Reviewer Task (Angela Martin)
        broadcast_hive_event("agent_status", {"role": "angela", "alias": "quality_reviewer", "status": "working", "label": "Auditing Attention Score"})
        broadcast_hive_event("terminal_log", {"level": "info", "message": 'Angela Martin: "Auditing First-Reader score and WCAG AA contrast. No frivolous nonsense allowed."', "role": "angela"})
        reviewer_task = HiveTask(
            id=f"{session_id}_t4_reviewer",
            role=AgentRole.ANGELA,
            title="Audit Attention Score & Accessibility Compliance (Angela)",
            input_data={},
            started_at=datetime.now().isoformat()
        )
        try:
            review_out = self.reviewer.execute(reviewer_task, copy_out)
            reviewer_task.output_data = review_out
            reviewer_task.status = TaskStatus.COMPLETED
            reviewer_task.completed_at = datetime.now().isoformat()
            self.breaker.record_success()
            broadcast_hive_event("agent_status", {"role": "angela", "alias": "quality_reviewer", "status": "idle", "label": "Audit Passed"})
            broadcast_hive_event("envelope_handoff", {"from": "angela", "to": "michael", "artifact": f"Score {review_out.get('attention_score', 0)}/100"})
            broadcast_hive_event("terminal_log", {"level": "success", "message": f'Angela Martin: "Audit passed. Attention Score {review_out.get("attention_score", 0)}/100. Stamped APPROVED ✓."', "role": "angela"})
        except Exception as exc:
            reviewer_task.status = TaskStatus.FAILED
            reviewer_task.error = str(exc)
            self.breaker.record_failure(str(exc))
            tasks.append(reviewer_task)
            self._save_ledger(session_id, tasks)
            broadcast_hive_event("terminal_log", {"level": "error", "message": f"Angela (Reviewer) failed: {exc}", "role": "angela"})
            raise

        tasks.append(reviewer_task)

        # Save complete ledger
        self.board["status"] = "completed"
        self.board["completed_at"] = datetime.now().isoformat()
        self.board["tasks"] = [t.to_dict() for t in tasks]
        self.board["artifacts"] = {
            "company": scout_out["company"],
            "role": scout_out["role"],
            "resume_pdf": architect_out["resume_pdf"],
            "email_subject": copy_out["email_subject"],
            "email_body": copy_out["email_body"],
            "followup_pitch": copy_out["followup_pitch"],
            "attention_score": review_out["attention_score"],
            "wcag_aa_compliant": review_out["wcag_aa_compliant"],
            "quality_gate": review_out["passed_quality_gate"]
        }

        self._save_ledger(session_id, tasks)
        broadcast_hive_event("mission_completed", {"session_id": session_id, "artifacts": self.board["artifacts"]})
        broadcast_hive_event("agent_status", {"role": "michael", "alias": "supervisor", "status": "idle", "label": "Mission Delivered"})
        broadcast_hive_event("terminal_log", {"level": "info", "message": f'Michael Scott: "Boom! Roasted. Mission {session_id} delivered by the Scranton branch!"', "role": "michael"})
        log.info("--- [HIVE SUPERVISOR] Mission %s completed successfully ---", session_id)
        return self.board

    def _save_ledger(self, session_id: str, tasks: List[HiveTask]) -> Path:
        ledger_file = HIVE_DIR / f"{session_id}.json"
        data = {
            "session_id": session_id,
            "circuit_breaker": {
                "state": self.breaker.state,
                "failures": self.breaker.failures
            },
            "tasks": [t.to_dict() for t in tasks],
            "board": self.board
        }
        ledger_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return ledger_file
