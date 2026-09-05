import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('gmail', 'v1', credentials=creds)

t = service.users().threads().get(userId='me', id='1a0391fb8264209f').execute()
print(f"Blinkist Thread has {len(t.get('messages', []))} messages:\n")

for i, m in enumerate(t.get('messages', [])):
    headers = {h['name'].lower(): h['value'] for h in m.get('payload', {}).get('headers', [])}
    print(f"=== MESSAGE {i+1} ===")
    print(f"From: {headers.get('from', '')}")
    print(f"To: {headers.get('to', '')}")
    print(f"Date: {headers.get('date', '')}")
    print(f"Subject: {headers.get('subject', '')}")
    print(f"Snippet: {m.get('snippet', '')}\n")
