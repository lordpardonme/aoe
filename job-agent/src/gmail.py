"""Gmail API client — send email with attachments, HTML and plain text."""

from __future__ import annotations

import base64
import mimetypes
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Iterable, List, Optional

from .config import GOOGLE_SCOPES, get_settings, load_google_credentials
from .logger import get_logger
from .utils import retry

log = get_logger("gmail")


class GmailClient:
    """Thin wrapper over the Gmail API for sending application emails."""

    def __init__(self) -> None:
        self._service = None
        self._settings = get_settings()

    # --- service ---------------------------------------------------------
    @property
    def service(self):
        """Lazily build (and cache) the authenticated Gmail service."""
        if self._service is None:
            from googleapiclient.discovery import build

            creds = load_google_credentials(GOOGLE_SCOPES)
            self._service = build("gmail", "v1", credentials=creds)
            log.info("Gmail service initialised")
        return self._service

    # --- message construction -------------------------------------------
    def _build_message(
        self,
        *,
        to: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        attachments: Optional[Iterable[str | Path]] = None,
        sender: Optional[str] = None,
    ) -> dict:
        attachments = list(attachments or [])

        # Choose the right container: alternative for text+html, mixed if files.
        if attachments:
            outer = MIMEMultipart("mixed")
            body_part = self._alternative(body, html_body)
            outer.attach(body_part)
            for path in attachments:
                outer.attach(self._attachment(Path(path)))
        else:
            outer = self._alternative(body, html_body)

        outer["To"] = to
        outer["From"] = sender or self._settings.sender_email or "me"
        outer["Subject"] = subject

        raw = base64.urlsafe_b64encode(outer.as_bytes()).decode()
        return {"raw": raw}

    @staticmethod
    def _alternative(body: str, html_body: Optional[str]):
        if html_body:
            part = MIMEMultipart("alternative")
            part.attach(MIMEText(body, "plain", "utf-8"))
            part.attach(MIMEText(html_body, "html", "utf-8"))
            return part
        return MIMEText(body, "plain", "utf-8")

    @staticmethod
    def _attachment(path: Path) -> MIMEApplication:
        if not path.exists():
            raise FileNotFoundError(f"Attachment not found: {path}")
        ctype, _ = mimetypes.guess_type(str(path))
        maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
        part = MIMEApplication(path.read_bytes(), _subtype=subtype)
        part.add_header(
            "Content-Disposition", "attachment", filename=path.name
        )
        part.add_header("Content-Type", f"{maintype}/{subtype}", name=path.name)
        return part

    # --- public API ------------------------------------------------------
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        attachments: Optional[List[str | Path]] = None,
        *,
        html_body: Optional[str] = None,
        sender: Optional[str] = None,
    ) -> dict:
        """Send an email via the Gmail API.

        Args:
            to: recipient address.
            subject: subject line.
            body: plain-text body.
            attachments: optional list of file paths to attach.
            html_body: optional HTML alternative body.
            sender: override the ``From`` header (defaults to config / ``me``).

        Returns:
            The Gmail API send response (with the message id), or a dry-run stub.

        Raises:
            ValueError: if *to* is empty.
        """
        if not to:
            raise ValueError("Cannot send email: no recipient address provided.")

        message = self._build_message(
            to=to,
            subject=subject,
            body=body,
            html_body=html_body,
            attachments=attachments,
            sender=sender,
        )

        if self._settings.dry_run:
            log.warning(
                "DRY_RUN enabled — NOT sending. Would send to %s | subject=%r | "
                "attachments=%d",
                to, subject, len(attachments or []),
            )
            return {"id": "DRY_RUN", "dry_run": True, "to": to, "subject": subject}

        return self._send(message)

    @retry(attempts=3, backoff_seconds=2.0)
    def _send(self, message: dict) -> dict:
        result = (
            self.service.users()
            .messages()
            .send(userId="me", body=message)
            .execute()
        )
        log.info("Email sent — Gmail message id=%s", result.get("id"))
        return result

    @retry(attempts=2, backoff_seconds=2.0)
    def get_profile(self) -> dict:
        """Return the authenticated Gmail profile (used by ``test``)."""
        return self.service.users().getProfile(userId="me").execute()
