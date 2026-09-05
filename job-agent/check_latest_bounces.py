import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('gmail', 'v1', credentials=creds)

print("Scanning Gmail for new incoming messages, bounces, and replies since last check...")

res = service.users().messages().list(userId='me', q="-from:hayaat0806@gmail.com", maxResults=30).execute()
messages = res.get('messages', [])

print(f"Found {len(messages)} recent messages.\n")

bounces = []
replies = []
auto_replies = []

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
    
    is_bounce = 'mailer-daemon' in from_h.lower() or 'postmaster' in from_h.lower() or 'failure' in subj_h.lower() or 'undeliverable' in subj_h.lower()
    is_auto = 'autoreply' in from_h.lower() or 'automatic reply' in subj_h.lower() or 'out of office' in subj_h.lower() or 'auto-response' in subj_h.lower()
    
    item = {
        'id': m_id,
        'thread_id': tid,
        'from': from_h,
        'subject': subj_h,
        'date': date_h,
        'snippet': snip
    }
    
    if is_bounce:
        bounces.append(item)
    elif is_auto:
        auto_replies.append(item)
    else:
        replies.append(item)

print("=== NEW BOUNCES DETECTED ===")
if bounces:
    for b in bounces:
        print(f"• Date: {b['date']}")
        print(f"  From: {b['from']}")
        print(f"  Subject: {b['subject']}")
        print(f"  Snippet: {b['snippet']}\n")
else:
    print("None found.\n")

print("=== NEW REPLIES / INCOMING MESSAGES ===")
if replies:
    for r in replies:
        print(f"• Date: {r['date']} | From: {r['from']}")
        print(f"  Subject: {r['subject']}")
        print(f"  Snippet: {r['snippet']}\n")
else:
    print("None found.\n")

print("=== AUTOMATED CONFIRMATIONS ===")
if auto_replies:
    for a in auto_replies:
        print(f"• Date: {a['date']} | From: {a['from']}")
        print(f"  Subject: {a['subject']}")
        print(f"  Snippet: {a['snippet']}\n")
else:
    print("None found.\n")
