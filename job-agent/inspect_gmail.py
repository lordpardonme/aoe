import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')
from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('gmail', 'v1', credentials=creds)

labels = service.users().labels().list(userId='me').execute().get('labels', [])
print("--- GMAIL LABELS ---")
for l in labels:
    print(f"ID: {l['id']:<30} | Name: {l['name']}")
