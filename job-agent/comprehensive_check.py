import sys
import io
import time
from datetime import datetime, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
gmail_service = build('gmail', 'v1', credentials=creds)
sheets_service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

def retry_api(fn, max_retries=4, delay=2):
    for i in range(max_retries):
        try:
            return fn()
        except Exception as e:
            time.sleep(delay)
            delay *= 2
    return fn()

print("========================================")
print("=== 1. GMAIL LIVE INBOX & REPLIES SCAN ===")
print("========================================")

# Search recent incoming messages across last 7 days
res = retry_api(lambda: gmail_service.users().messages().list(userId='me', q='-from:hayaat0806@gmail.com', maxResults=60).execute())
messages = res.get('messages', [])

human_replies = []
bounces = []
auto_replies = []
recruiter_alerts = []

for m in messages:
    m_id = m['id']
    msg = retry_api(lambda: gmail_service.users().messages().get(userId='me', id=m_id, format='metadata', metadataHeaders=['From', 'To', 'Subject', 'Date']).execute())
    headers = {h['name'].lower(): h['value'] for h in msg.get('payload', {}).get('headers', [])}
    
    from_h = headers.get('from', '')
    subj_h = headers.get('subject', '')
    date_h = headers.get('date', '')
    snippet = msg.get('snippet', '')
    thread_id = msg.get('threadId', '')
    
    from_lower = from_h.lower()
    subj_lower = subj_h.lower()
    
    if 'mailer-daemon' in from_lower or 'postmaster' in from_lower or 'failure' in subj_lower or 'undeliverable' in subj_lower or 'delay' in subj_lower:
        bounces.append({'from': from_h, 'subject': subj_h, 'date': date_h, 'snippet': snippet, 'id': m_id})
    elif 'autoreply' in from_lower or 'out of office' in from_lower or 'auto-response' in subj_lower or 'automatic reply' in subj_lower or 'out of the office' in snippet.lower():
        auto_replies.append({'from': from_h, 'subject': subj_h, 'date': date_h, 'snippet': snippet})
    elif subj_lower.startswith('re:'):
        human_replies.append({'from': from_h, 'subject': subj_h, 'date': date_h, 'snippet': snippet, 'thread_id': thread_id})
    elif any(k in from_lower or k in subj_lower for k in ['linkedin', 'naukri', 'wellfound', 'indeed', 'glassdoor', 'totaljobs', 'job alert']):
        recruiter_alerts.append({'from': from_h, 'subject': subj_h, 'date': date_h, 'snippet': snippet})

print(f"\n--- A. HUMAN REPLIES / APPLICATION THREADS ({len(human_replies)}) ---")
if human_replies:
    for r in human_replies:
        print(f"• FROM: {r['from']}")
        print(f"  DATE: {r['date']}")
        print(f"  SUBJECT: {r['subject']}")
        print(f"  SNIPPET: {r['snippet']}")
        print(f"  THREAD ID: {r['thread_id']}\n")
else:
    print("No direct replies found.\n")

print(f"--- B. BOUNCES & DELIVERY ISSUES ({len(bounces)}) ---")
if bounces:
    for b in bounces[:10]:
        print(f"• FROM: {b['from']} | DATE: {b['date']}")
        print(f"  SUBJECT: {b['subject']}")
        print(f"  SNIPPET: {b['snippet']}\n")
else:
    print("No recent bounces found.\n")

print(f"--- C. AUTOMATED / OUT OF OFFICE ({len(auto_replies)}) ---")
if auto_replies:
    for a in auto_replies:
        print(f"• FROM: {a['from']} | DATE: {a['date']} | SUBJ: {a['subject']}")
else:
    print("None.\n")

print(f"--- D. RECENT RECRUITER & JOB ALERTS (LATEST 5) ---")
for al in recruiter_alerts[:5]:
    print(f"• [{al['date']}] {al['from']}: {al['subject']}")

print("\n========================================")
print("=== 2. LIVE GOOGLE SHEET TRACKER AUDIT ===")
print("========================================")

meta = retry_api(lambda: sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute())
sheet_names = [s['properties']['title'] for s in meta['sheets']]
print(f"Sheets in Workbook ({len(sheet_names)}): {', '.join(sheet_names)}")

res_m = retry_api(lambda: sheets_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute())
m_rows = res_m.get('values', [])
print(f"\nMaster Job Tracker: {len(m_rows)} total rows (including header)")

status_counts = {}
for r in m_rows[1:]:
    st = r[4].strip() if len(r) > 4 else '[Blank]'
    status_counts[st] = status_counts.get(st, 0) + 1

for st, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  • {st}: {count}")

res_sent = retry_api(lambda: sheets_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Sent By Me'!A1:K").execute())
sent_rows = res_sent.get('values', [])
print(f"\nSent By Me log: {len(sent_rows)-1} outbound emails logged.")

# Check Dashboard values
res_d = retry_api(lambda: sheets_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="Dashboard!A1:C28", valueRenderOption='FORMATTED_VALUE').execute())
print("\nDashboard live values:")
for row in res_d.get('values', []):
    if any(row):
        print(f"  {row}")

print("\n========================================")
print("=== 3. FOLLOW-UPS OVERDUE / DUE TODAY ===")
print("========================================")

today = datetime.now().date()
overdue = []
due_soon = []

for idx, r in enumerate(m_rows[1:], start=2):
    r_padded = r + [''] * (14 - len(r))
    country, company, email, l_type, status, dt_applied, dt_follow, notes, scan_status, role, url, conf, rec_act, dt_scan = r_padded
    
    if status.strip().lower() == 'applied' and dt_follow.strip():
        try:
            f_date = datetime.strptime(dt_follow.strip(), '%Y-%m-%d').date()
            diff = (f_date - today).days
            item = {'row': idx, 'company': company, 'role': role, 'email': email, 'applied': dt_applied, 'follow_date': dt_follow, 'days_overdue': -diff}
            if diff < 0:
                overdue.append(item)
            elif diff <= 2:
                due_soon.append(item)
        except Exception:
            pass

print(f"Follow-ups Overdue: {len(overdue)}")
for o in overdue[:10]:
    print(f"  • Row {o['row']} | {o['company']} ({o['role'] or 'N/A'}) | Applied: {o['applied']} | Due: {o['follow_date']} ({o['days_overdue']} days overdue) | Email: {o['email']}")

print(f"\nFollow-ups Due Today / Next 2 Days: {len(due_soon)}")
for d in due_soon[:10]:
    print(f"  • Row {d['row']} | {d['company']} ({d['role'] or 'N/A'}) | Applied: {d['applied']} | Due: {d['follow_date']} | Email: {d['email']}")
