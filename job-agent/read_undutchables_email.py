import sys
import io
import base64

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('gmail', 'v1', credentials=creds)

msg_id = "1a0395a669988b7f" # Undutchables
msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

def get_body(payload):
    body = ''
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                body += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
            elif 'parts' in part:
                body += get_body(part)
    elif 'body' in payload and 'data' in payload['body']:
        body += base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
    return body

body_text = get_body(msg.get('payload', {}))
print("=== FULL EMAIL FROM UNDUTCHABLES ===")
print(body_text)
