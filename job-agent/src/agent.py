"""End-to-end application orchestration.

:class:`JobAgent` ties every module together into the ``apply`` pipeline:
fetch/parse JD -> tailor resume -> cover letter -> email -> PDFs -> send ->
update tracker -> persist everything -> return a summary.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import RESUMES_DIR, TRACKER_DIR, get_settings
from .coverletter import CoverLetterBuilder
from .emailer import EmailBuilder
from .gmail import GmailClient
from .jobs import JobDescription, build_job, fetch_from_url, load_from_file
from .logger import get_logger
from .pdf import render_resume_pdf
from .resume import ResumeBuilder
from .sheet import SheetClient
from .utils import slugify

log = get_logger("agent")


@dataclass
class ApplicationResult:
    """Summary of a completed (or dry-run) application."""

    company: str
    role: str
    url: Optional[str]
    keywords: List[str]
    files: Dict[str, str] = field(default_factory=dict)
    email_to: Optional[str] = None
    email_status: str = "not_sent"
    tracker_status: str = "not_updated"
    dry_run: bool = True
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class JobAgent:
    """High-level façade over the whole pipeline."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.resume_builder = ResumeBuilder()
        self.cover_builder = CoverLetterBuilder()
        self.email_builder = EmailBuilder()

    # --- job acquisition -------------------------------------------------
    def job_from_url(self, url: str, *, company: str | None = None, role: str | None = None) -> JobDescription:
        text = fetch_from_url(url)
        return build_job(text=text, url=url, company=company, role=role)

    def job_from_file(self, path: str, *, company: str | None = None, role: str | None = None) -> JobDescription:
        text = load_from_file(path)
        return build_job(text=text, url=None, company=company, role=role)

    def job_from_text(self, text: str, *, company: str | None = None, role: str | None = None) -> JobDescription:
        return build_job(text=text, url=None, company=company, role=role)

    # --- document generation --------------------------------------------
    def generate_documents(self, job: JobDescription) -> Dict[str, Path]:
        """Tailor resume, cover letter and email; render all PDFs."""
        slug = slugify(job.company)
        files: Dict[str, Path] = {}

        resume_data, resume_docx = self.resume_builder.build(job)
        resume_pdf = render_resume_pdf(resume_data, RESUMES_DIR / f"{slug}_resume.pdf")
        files["resume_docx"] = resume_docx
        files["resume_pdf"] = resume_pdf

        cover = self.cover_builder.build(job, resume_data)
        files["cover_md"] = cover["md"]
        files["cover_docx"] = cover["docx"]
        files["cover_pdf"] = cover["pdf"]

        email = self.email_builder.build(job, resume_data)
        files["email_md"] = email["md"]  # type: ignore[assignment]
        files["email_html"] = email["html"]  # type: ignore[assignment]
        self._last_email = email  # cache for send step
        return files

    # --- send + track ----------------------------------------------------
    def send_application_email(
        self, job: JobDescription, files: Dict[str, Path], recipient: str | None = None
    ) -> Dict[str, Any]:
        email = getattr(self, "_last_email", None) or self.email_builder.build(job, self.resume_builder.tailor(job))
        to = recipient or job.contact_email or self.settings.default_recipient
        if not to:
            log.warning("No recipient available — skipping email send.")
            return {"status": "skipped_no_recipient", "to": None}

        client = GmailClient()
        attachments = [p for k, p in files.items() if k in ("resume_pdf", "cover_pdf")]
        result = client.send_email(
            to=to,
            subject=str(email["subject"]),
            body=str(email["text_body"]),
            html_body=str(email["html_body"]),
            attachments=attachments,
        )
        status = "dry_run" if result.get("dry_run") else "sent"
        return {"status": status, "to": to, "message_id": result.get("id")}

    def update_tracker(self, job: JobDescription, files: Dict[str, Path], status: str = "Applied", notes: str = "") -> Dict[str, Any]:
        client = SheetClient()
        return client.update_tracker(
            company=job.company,
            role=job.role,
            url=job.url or "",
            resume=str(files.get("resume_pdf", "")),
            status=status,
            notes=notes,
        )

    # --- full pipeline ---------------------------------------------------
    def apply(
        self,
        job: JobDescription,
        *,
        send: bool = True,
        update_sheet: bool = True,
        recipient: str | None = None,
    ) -> ApplicationResult:
        """Run the complete apply pipeline and return an :class:`ApplicationResult`."""
        log.info("=== APPLY START === company=%r role=%r", job.company, job.role)
        files = self.generate_documents(job)

        email_to = recipient or job.contact_email or self.settings.default_recipient
        email_status = "not_sent"
        if send:
            outcome = self.send_application_email(job, files, recipient)
            email_status = outcome["status"]
            email_to = outcome.get("to") or email_to

        tracker_status = "not_updated"
        if update_sheet:
            t = self.update_tracker(job, files, notes=f"Auto-applied via Job Agent")
            tracker_status = "remote+local" if t.get("remote") else "local_only"

        result = ApplicationResult(
            company=job.company,
            role=job.role,
            url=job.url,
            keywords=job.keywords,
            files={k: str(v) for k, v in files.items()},
            email_to=email_to,
            email_status=email_status,
            tracker_status=tracker_status,
            dry_run=self.settings.dry_run,
        )
        self._persist_result(job, result)
        log.info("=== APPLY DONE === %s / %s", job.company, job.role)
        return result

    # --- persistence -----------------------------------------------------
    def _persist_result(self, job: JobDescription, result: ApplicationResult) -> Path:
        """Save a JSON record of the application under ``tracker/``."""
        slug = slugify(job.company)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = TRACKER_DIR / f"{slug}_{stamp}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        payload = result.to_dict()
        payload["job"] = {
            "company": job.company,
            "role": job.role,
            "url": job.url,
            "contact_email": job.contact_email,
            "keywords": job.keywords,
        }
        out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        log.info("Saved application record -> %s", out)
        return out
