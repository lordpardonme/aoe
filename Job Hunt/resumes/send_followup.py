#!/usr/bin/env python3
"""
Send ONE threaded follow-up email as a reply to an existing Gmail thread.

Readable and auditable. Preserves thread continuity by adding In-Reply-To,
References headers and sending with the Gmail threadId.

Usage:
  python send_followup.py --to X --subject "Re: Y" --body-file body.txt --thread-id TID --in-reply-to MSG_ID [--attachment file.pdf] [--dry-run]
"""
import sys
import io
import argparse
import base64
import mimetypes
from email.message import EmailMessage
from pathlib import Path

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
TOKEN = REPO_ROOT / "job-agent" / "token.json"
SENDER = "hayaat0806@gmail.com"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True)
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body-file", required=True)
    ap.add_argument("--thread-id", required=True, help="Gmail threadId of the conversation")
    ap.add_argument("--in-reply-to", required=True, help="Message-ID header of the message being replied to")
    ap.add_argument("--attachment", nargs="*", default=[], help="Optional PDF/file attachment(s)")
    ap.add_argument("--dry-run", action="store_true", help="Preview without sending")
    a = ap.parse_args()

    body_path = Path(a.body_file)
    if not body_path.exists():
        raise SystemExit(f"Body file not found: {body_path}")
    body = body_path.read_text(encoding="utf-8")

    attachments = [Path(p) for p in a.attachment]
    for att in attachments:
        if not att.exists():
            raise SystemExit(f"Attachment not found: {att}")

    # Ensure subject starts with Re:
    subject = a.subject
    if not subject.lower().startswith("re:"):
        subject = f"Re: {subject}"

    msg = EmailMessage()
    msg["To"] = a.to
    msg["From"] = SENDER
    msg["Subject"] = subject
    msg["In-Reply-To"] = a.in_reply_to
    msg["References"] = a.in_reply_to
    msg.set_content(body)

    for att in attachments:
        ctype, _ = mimetypes.guess_type(str(att))
        maintype, subtype = (ctype or "application/pdf").split("/", 1)
        msg.add_attachment(att.read_bytes(), maintype=maintype, subtype=subtype, filename=att.name)

    if a.dry_run:
        att_str = ", ".join(att.name for att in attachments) if attachments else "none"
        print(f"[DRY-RUN] To: {a.to} | ThreadId: {a.thread_id} | In-Reply-To: {a.in_reply_to}")
        print(f"Subject: {subject}")
        print(f"Attachment: {att_str}")
        print("Body snippet:")
        print(body[:150] + "...")
        return

    if not TOKEN.exists():
        raise SystemExit(f"Token not found at {TOKEN}")

    creds = Credentials.from_authorized_user_file(str(TOKEN))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    svc = build("gmail", "v1", credentials=creds)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    sent = svc.users().messages().send(userId="me", body={"raw": raw, "threadId": a.thread_id}).execute()
    print(f"SENT to={a.to} id={sent['id']} threadId={sent['threadId']}")


if __name__ == "__main__":
    main()
