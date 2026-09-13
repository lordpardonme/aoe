"""Gmail API client — send email with attachments, HTML/plain text, draft creation, and inbound reply scanner."""

from __future__ import annotations

import base64
import email.utils
import json
import mimetypes
import os
import re
import shutil
import threading
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .config import GOOGLE_SCOPES, PROJECT_ROOT, get_settings, load_google_credentials
from .logger import get_logger
from .utils import retry

log = get_logger("gmail")

WORKSPACE_PRIVATE_DIR = Path(r"g:\job-hunt-workspace-private\job-agent")


class GmailClient:
    """Enhanced wrapper over the Gmail API for sending, drafting, and scanning inbound replies."""

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

    def manual_sync_from_workspace(self) -> List[str]:
        """Explicitly copy credentials.json/token.json from private workspace when requested by user."""
        synced = []
        try:
            cred_path = self._settings.credentials_path
            token_path = self._settings.token_path

            ws_cred = WORKSPACE_PRIVATE_DIR / "credentials.json"
            ws_token = WORKSPACE_PRIVATE_DIR / "token.json"

            if not cred_path.exists() and ws_cred.exists():
                shutil.copy(ws_cred, cred_path)
                synced.append("credentials.json")
                log.info("Explicitly synced credentials.json from workspace")

            if not token_path.exists() and ws_token.exists():
                shutil.copy(ws_token, token_path)
                synced.append("token.json")
                log.info("Explicitly synced token.json from workspace")
        except Exception as e:
            log.warning("Workspace credential sync error: %s", e)
        return synced

    def disconnect(self) -> Dict[str, Any]:
        """Disconnect Gmail integration by clearing cached client and removing local token.json."""
        self._service = None
        removed = []
        token_path = self._settings.token_path
        if token_path.exists():
            try:
                token_path.unlink()
                removed.append("token.json")
                log.info("Removed local token.json for Gmail disconnect")
            except Exception as e:
                log.warning("Failed to unlink token.json: %s", e)
        return {"status": "disconnected", "removed": removed}

    # --- auth status & operations ---------------------------------------
    def get_auth_status(self) -> Dict[str, Any]:
        """Check current Google OAuth status, credentials existence, and profile."""
        cred_exists = self._settings.credentials_path.exists()
        token_exists = self._settings.token_path.exists()
        dry_run = self._settings.dry_run

        if not token_exists and not cred_exists:
            return {
                "authenticated": False,
                "email": "",
                "messages_total": 0,
                "credentials_exist": False,
                "token_exists": False,
                "dry_run": dry_run,
                "error": "No Google Cloud credentials or OAuth token found.",
            }

        if not token_exists:
            return {
                "authenticated": False,
                "email": "",
                "messages_total": 0,
                "credentials_exist": cred_exists,
                "token_exists": False,
                "dry_run": dry_run,
                "error": "Google credentials found, but account not authorized. Click 'Authorize Gmail Account'.",
            }

        try:
            profile = self.get_profile()
            return {
                "authenticated": True,
                "email": profile.get("emailAddress", ""),
                "messages_total": profile.get("messagesTotal", 0),
                "credentials_exist": cred_exists,
                "token_exists": token_exists,
                "dry_run": dry_run,
                "error": None,
            }
        except Exception as e:
            return {
                "authenticated": False,
                "email": "",
                "messages_total": 0,
                "credentials_exist": cred_exists,
                "token_exists": token_exists,
                "dry_run": dry_run,
                "error": str(e),
            }

    def run_interactive_oauth(self) -> None:
        """Run the OAuth InstalledAppFlow in a background thread."""
        from google_auth_oauthlib.flow import InstalledAppFlow

        cred_path = self._settings.credentials_path
        if not cred_path.exists():
            raise FileNotFoundError(f"Missing credentials file at {cred_path}")

        flow = InstalledAppFlow.from_client_secrets_file(
            str(cred_path), GOOGLE_SCOPES
        )
        creds = flow.run_local_server(port=0, open_browser=True)
        self._settings.token_path.write_text(creds.to_json(), encoding="utf-8")
        self._service = None  # Reset cached service to reload new creds
        log.info("Interactive OAuth flow completed successfully.")

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

        # Choose container: alternative for text+html, mixed if files.
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

    # --- public Send & Draft API -----------------------------------------
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
        """Send an email via the Gmail API."""
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

        # HARD SAFETY LOCK: Live sending is completely on hold for testing
        log.warning(
            "LIVE SEND LOCKED ON HOLD FOR TESTING — Simulating dispatch to %s | subject=%r | attachments=%d",
            to, subject, len(attachments or []),
        )
        return {"id": "LOCKED_DRY_RUN", "dry_run": True, "to": to, "subject": subject}

        # Original live send path kept below for future activation:
        # return self._send(message)

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

    def create_draft(
        self,
        to: str,
        subject: str,
        body: str,
        attachments: Optional[List[str | Path]] = None,
        *,
        html_body: Optional[str] = None,
        sender: Optional[str] = None,
    ) -> dict:
        """Create a message draft in the user's Gmail Drafts folder."""
        if not to:
            raise ValueError("Cannot draft email: no recipient address provided.")

        message = self._build_message(
            to=to,
            subject=subject,
            body=body,
            html_body=html_body,
            attachments=attachments,
            sender=sender,
        )

        draft = (
            self.service.users()
            .drafts()
            .create(userId="me", body={"message": message})
            .execute()
        )
        log.info("Draft created — Gmail draft id=%s", draft.get("id"))
        return {
            "status": "ok",
            "draft_id": draft.get("id"),
            "message_id": draft.get("message", {}).get("id"),
            "to": to,
            "subject": subject,
        }

    @retry(attempts=2, backoff_seconds=2.0)
    def get_profile(self) -> dict:
        """Return the authenticated Gmail profile."""
        return self.service.users().getProfile(userId="me").execute()

    # --- Inbound Scanner & Parsing --------------------------------------
    @staticmethod
    def _extract_body(payload: dict) -> str:
        """Extract clean text content from message payload."""
        body_data = ""
        if "parts" in payload:
            for part in payload["parts"]:
                mime = part.get("mimeType", "")
                if mime == "text/plain" and "data" in part.get("body", {}):
                    body_data = part["body"]["data"]
                    break
                elif "parts" in part:
                    sub = GmailClient._extract_body(part)
                    if sub:
                        return sub
            if not body_data:
                for part in payload["parts"]:
                    if part.get("mimeType", "") == "text/html" and "data" in part.get("body", {}):
                        body_data = part["body"]["data"]
                        break
        elif "body" in payload and "data" in payload["body"]:
            body_data = payload["body"]["data"]

        if body_data:
            try:
                raw_bytes = base64.urlsafe_b64decode(body_data.encode("ASCII"))
                decoded = raw_bytes.decode("utf-8", errors="replace")
                clean = re.sub(r"<[^>]+>", " ", decoded)
                clean = re.sub(r"\s+", " ", clean).strip()
                return clean
            except Exception:
                return ""
        return ""

    @staticmethod
    def classify_reply_intent(subject: str, snippet: str, body_text: str) -> Dict[str, Any]:
        """Classify message intent into Interview, Rejection, Assessment, or Under Review."""
        text = f"{subject} {snippet} {body_text}".lower()

        # Interview
        interview_keywords = [
            "interview", "schedule a call", "schedule an interview", "schedule some time",
            "calendly.com", "calendar invite", "speak with you", "discuss your application",
            "chat with our team", "next steps with your application", "invitation to interview",
            "phone screening", "zoom link", "google meet", "time slot", "availability for a quick call"
        ]
        if any(k in text for k in interview_keywords):
            return {
                "intent": "Interview",
                "suggested_status": "Interview",
                "confidence": 0.95,
                "badge": "🎉 Interview Request",
            }

        # Rejection
        rejection_keywords = [
            "unfortunately", "other candidates", "not moving forward", "regret to inform",
            "pursuing other", "decided not to proceed", "high volume of applications",
            "not selected", "wish you the best in your search", "will not be moving forward",
            "we are unable to offer you"
        ]
        if any(k in text for k in rejection_keywords):
            return {
                "intent": "Rejected",
                "suggested_status": "Rejected",
                "confidence": 0.90,
                "badge": "❌ Not Moving Forward",
            }

        # Assessment / Challenge
        assessment_keywords = [
            "assessment", "take-home", "design challenge", "technical challenge",
            "coding test", "hackerrank", "codility", "assignment", "portfolio review task"
        ]
        if any(k in text for k in assessment_keywords):
            return {
                "intent": "Assessment",
                "suggested_status": "Screening",
                "confidence": 0.85,
                "badge": "📋 Design Challenge / Assessment",
            }

        # Under Review / Acknowledgment
        review_keywords = [
            "application received", "received your application", "reviewing your application",
            "thank you for applying", "under review", "in our database", "received your resume"
        ]
        if any(k in text for k in review_keywords):
            return {
                "intent": "Under Review",
                "suggested_status": "Under Review",
                "confidence": 0.80,
                "badge": "📨 Application Received / Reviewing",
            }

        return {
            "intent": "Uncategorized",
            "suggested_status": "Applied",
            "confidence": 0.50,
            "badge": "📩 Update / Follow-up",
        }

    def scan_inbound_replies(
        self,
        tracked_applications: Optional[List[Dict[str, Any]]] = None,
        query: str = "-from:me newer_than:30d",
        max_results: int = 40,
    ) -> List[Dict[str, Any]]:
        """Scan Gmail for inbound recruiter replies, classify them, and match with applications."""
        tracked_applications = tracked_applications or []
        res = self.service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
        messages = res.get("messages", [])

        replies = []
        for m in messages:
            msg_id = m["id"]
            try:
                msg = self.service.users().messages().get(userId="me", id=msg_id, format="full").execute()
                payload = msg.get("payload", {})
                headers = {h["name"].lower(): h["value"] for h in payload.get("headers", [])}

                from_header = headers.get("from", "")
                subject = headers.get("subject", "")
                date_header = headers.get("date", "")
                snippet = msg.get("snippet", "")
                body_text = self._extract_body(payload)

                sender_email = ""
                sender_name = from_header
                parsed_addr = email.utils.parseaddr(from_header)
                if parsed_addr[1]:
                    sender_email = parsed_addr[1].lower()
                    sender_name = parsed_addr[0] or parsed_addr[1]

                classification = self.classify_reply_intent(subject, snippet, body_text)

                matched_app = None
                sender_domain = sender_email.split("@")[-1] if "@" in sender_email else ""

                for app in tracked_applications:
                    contact_email = (app.get("contact_email") or "").lower()
                    contact_domain = contact_email.split("@")[-1] if "@" in contact_email else ""
                    company = (app.get("company") or "").lower()
                    role = (app.get("role") or "").lower()

                    if contact_email and (sender_email == contact_email or (sender_domain and sender_domain == contact_domain and sender_domain not in ("gmail.com", "outlook.com", "yahoo.com"))):
                        matched_app = app
                        break
                    if company and len(company) > 2 and (company in subject.lower() or company in from_header.lower()):
                        matched_app = app
                        break

                replies.append({
                    "gmail_message_id": msg_id,
                    "thread_id": msg.get("threadId", ""),
                    "sender_name": sender_name,
                    "sender_email": sender_email,
                    "from_header": from_header,
                    "subject": subject,
                    "date": date_header,
                    "snippet": snippet,
                    "body_preview": body_text[:300],
                    "intent": classification["intent"],
                    "suggested_status": classification["suggested_status"],
                    "badge": classification["badge"],
                    "confidence": classification["confidence"],
                    "matched_app_id": matched_app.get("id") if matched_app else None,
                    "matched_company": matched_app.get("company") if matched_app else None,
                    "matched_role": matched_app.get("role") if matched_app else None,
                })
            except Exception as ex:
                log.warning("Failed to parse message %s: %s", msg_id, ex)

        return replies
