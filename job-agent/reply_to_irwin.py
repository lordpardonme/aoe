import sys
import io
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('gmail', 'v1', credentials=creds)

to_email = "christine@irwinanddow.com"
subject = "RE: Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali"
thread_id = "1a0386413cadf29a"
body_file = Path("Job Hunt/resumes/irwin-reply-email.txt")
body_text = body_file.read_text(encoding='utf-8')

message = MIMEText(body_text)
message['to'] = to_email
message['subject'] = subject
message['In-Reply-To'] = "1a038b68093bb4ca"
message['References'] = "1a038b68093bb4ca"

raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
body = {
    'raw': raw,
    'threadId': thread_id
}

print(f"Sending thread reply to {to_email} (Thread ID: {thread_id})...")
sent = service.users().messages().send(userId='me', body=body).execute()
print(f"SENT reply successfully! ID: {sent['id']}, Thread ID: {sent['threadId']}")
