import sys
import io
import re
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('gmail', 'v1', credentials=creds)

print("Querying Gmail for recent received messages and replies...")

# 1. Search for incoming messages (not from hayaat0806@gmail.com)
query = "-from:hayaat0806@gmail.com"
res = service.users().messages().list(userId='me', q=query, maxResults=50).execute()
messages = res.get('messages', [])

print(f"Found {len(messages)} incoming messages matching query '{query}'.\n")

detailed_messages = []

for m in messages:
    m_id = m['id']
    msg = service.users().messages().get(userId='me', id=m_id, format='metadata', metadataHeaders=['From', 'To', 'Subject', 'Date']).execute()
    
    headers = {h['name'].lower(): h['value'] for h in msg.get('payload', {}).get('headers', [])}
    from_header = headers.get('from', '')
    subject_header = headers.get('subject', '')
    date_header = headers.get('date', '')
    snippet = msg.get('snippet', '')
    thread_id = msg.get('threadId', '')
    
    # Categorize
    is_bounce = 'mailer-daemon' in from_header.lower() or 'postmaster' in from_header.lower() or 'failure' in subject_header.lower() or 'undeliverable' in subject_header.lower()
    is_auto = 'autoreply' in from_header.lower() or 'automatic reply' in subject_header.lower() or 'out of office' in subject_header.lower() or 'auto-response' in subject_header.lower()
    is_reply = subject_header.strip().lower().startswith('re:')
    
    detailed_messages.append({
        'id': m_id,
        'thread_id': thread_id,
        'from': from_header,
        'subject': subject_header,
        'date': date_header,
        'snippet': snippet,
        'is_bounce': is_bounce,
        'is_auto': is_auto,
        'is_reply': is_reply
    })

# Print categorized summary
bounces = [m for m in detailed_messages if m['is_bounce']]
auto_replies = [m for m in detailed_messages if m['is_auto']]
replies = [m for m in detailed_messages if m['is_reply'] and not m['is_bounce'] and not m['is_auto']]
other = [m for m in detailed_messages if not m['is_bounce'] and not m['is_auto'] and not m['is_reply']]

print("=== 1. HUMAN REPLIES / THREAD RESPONSES ===")
if replies:
    for r in replies:
        print(f"• FROM: {r['from']}")
        print(f"  DATE: {r['date']}")
        print(f"  SUBJECT: {r['subject']}")
        print(f"  SNIPPET: {r['snippet']}")
        print(f"  THREAD ID: {r['thread_id']}\n")
else:
    print("None found.\n")

print("=== 2. BOUNCES / UNDELIVERABLE NOTICES ===")
if bounces:
    for b in bounces:
        print(f"• FROM: {b['from']}")
        print(f"  DATE: {b['date']}")
        print(f"  SUBJECT: {b['subject']}")
        print(f"  SNIPPET: {b['snippet']}\n")
else:
    print("None found.\n")

print("=== 3. AUTOMATED / OUT OF OFFICE REPLIES ===")
if auto_replies:
    for a in auto_replies:
        print(f"• FROM: {a['from']}")
        print(f"  DATE: {a['date']}")
        print(f"  SUBJECT: {a['subject']}")
        print(f"  SNIPPET: {a['snippet']}\n")
else:
    print("None found.\n")

print("=== 4. OTHER INCOMING MESSAGES (TOP 10) ===")
for o in other[:10]:
    print(f"• FROM: {o['from']} | DATE: {o['date']}")
    print(f"  SUBJECT: {o['subject']}")
    print(f"  SNIPPET: {o['snippet']}\n")
