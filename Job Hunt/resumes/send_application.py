#!/usr/bin/env python3
"""
Send ONE job application email with a PDF attachment, from hayaat0806@gmail.com.

Readable and auditable. This is the canonical send step of the JD->packet->send
pipeline. It does NOT generate content - it sends exactly the body file and
attachment you pass. (Never use the opaque job-agent .pyc bytecode for sending.)

Usage:
  python send_application.py --to X --subject "Y" --body-file body.txt --attachment resume.pdf [--dry-run]

Auth: uses the existing OAuth token at job-agent/token.json
(account hayaat0806@gmail.com, gmail.send scope - verified 2026-07-29).
"""
import argparse
import base64
import mimetypes
from email.message import EmailMessage
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN = Path(r"C:\Users\mohdh\Desktop\Job Hunt\job-agent\token.json")
SENDER = "hayaat0806@gmail.com"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True)
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body-file", required=True)
    ap.add_argument("--attachment", required=True, nargs="+", help="one or more PDF/file attachments")
    ap.add_argument("--dry-run", action="store_true", help="build but do not send")
    a = ap.parse_args()

    body = Path(a.body_file).read_text(encoding="utf-8")
    attachments = [Path(p) for p in a.attachment]
    for att in attachments:
        if not att.exists():
            raise SystemExit(f"attachment not found: {att}")

    msg = EmailMessage()
    msg["To"] = a.to
    msg["From"] = SENDER
    msg["Subject"] = a.subject
    msg.set_content(body)
    for att in attachments:
        ctype, _ = mimetypes.guess_type(str(att))
        maintype, subtype = (ctype or "application/pdf").split("/", 1)
        msg.add_attachment(att.read_bytes(), maintype=maintype, subtype=subtype, filename=att.name)

    if a.dry_run:
        att_names = ", ".join(f"{att.name} ({att.stat().st_size} B)" for att in attachments)
        print(f"DRY-RUN to={a.to} subject={a.subject!r} attach=[{att_names}]")
        return

    creds = Credentials.from_authorized_user_file(str(TOKEN))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    svc = build("gmail", "v1", credentials=creds)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    sent = svc.users().messages().send(userId="me", body={"raw": raw}).execute()
    att_summary = ", ".join(att.name for att in attachments)
    print(f"SENT to={a.to} id={sent['id']} threadId={sent['threadId']} attach=[{att_summary}]")


if __name__ == "__main__":
    main()
