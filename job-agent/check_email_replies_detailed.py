import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('gmail', 'v1', credentials=creds)

print("Scanning Gmail for recent inbound messages (bounces, human replies, forms, consent requests)...")

res = service.users().messages().list(userId='me', q="-from:hayaat0806@gmail.com", maxResults=40).execute()
messages = res.get('messages', [])

print(f"Found {len(messages)} recent incoming messages.\n")

bounces = []
actionable_replies = []
auto_confirmations = []
other_messages = []

for m in messages:
    m_id = m['id']
    msg = service.users().messages().get(
        userId='me',
        id=m_id,
        format='metadata',
        metadataHeaders=['From', 'To', 'Subject', 'Date']
    ).execute()
    
    headers = {h['name'].lower(): h['value'] for h in msg.get('payload', {}).get('headers', [])}
    from_h = headers.get('from', '')
    subj_h = headers.get('subject', '')
    date_h = headers.get('date', '')
    snip = msg.get('snippet', '')
    tid = msg.get('threadId', '')
    
    item = {
        'id': m_id,
        'thread_id': tid,
        'from': from_h,
        'subject': subj_h,
        'date': date_h,
        'snippet': snip
    }
    
    is_bounce = 'mailer-daemon' in from_h.lower() or 'postmaster' in from_h.lower() or 'failure' in subj_h.lower() or 'undeliverable' in subj_h.lower()
    is_auto = 'autoreply' in from_h.lower() or 'automatic reply' in subj_h.lower() or 'out of office' in subj_h.lower() or 'auto-response' in subj_h.lower() or 'no-reply' in from_h.lower() or 'noreply' in from_h.lower()
    
    if is_bounce:
        bounces.append(item)
    elif 'cutshort' in from_h.lower() or 'questionnaire' in snip.lower() or 'consent' in snip.lower() or subj_h.lower().startswith('re:'):
        actionable_replies.append(item)
    elif is_auto:
        auto_confirmations.append(item)
    else:
        other_messages.append(item)

print("=== 1. BOUNCES / UNDELIVERABLE (ACTION: MARK AS BOUNCED) ===")
if bounces:
    for b in bounces:
        print(f"• ID: {b['id']} | Date: {b['date']}")
        print(f"  From: {b['from']}")
        print(f"  Subject: {b['subject']}")
        print(f"  Snippet: {b['snippet']}\n")
else:
    print("None found.\n")

print("=== 2. THREAD REPLIES / ACTIONABLE MESSAGES (ACTION: REVIEW & RESPOND) ===")
if actionable_replies:
    for a in actionable_replies:
        print(f"• ID: {a['id']} | Thread: {a['thread_id']} | Date: {a['date']}")
        print(f"  From: {a['from']}")
        print(f"  Subject: {a['subject']}")
        print(f"  Snippet: {a['snippet']}\n")
else:
    print("None found.\n")

print("=== 3. AUTOMATED CONFIRMATIONS ===")
if auto_confirmations:
    for c in auto_confirmations:
        print(f"• From: {c['from']} | Date: {c['date']}")
        print(f"  Subject: {c['subject']}")
        print(f"  Snippet: {c['snippet']}\n")
else:
    print("None found.\n")
