import sys
import io
import re
import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
gmail = build('gmail', 'v1', credentials=creds)
sheets = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

# Read entire Master Job Tracker
res_master = sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
rows = res_master.get('values', [])
headers = rows[0]
data = rows[1:]

print(f"Total rows in Master Job Tracker: {len(data)}")

# Let's fetch all Sent messages from Gmail
print("Fetching all sent messages from Gmail...")
sent_messages = []
page_token = None
while True:
    res_s = gmail.users().messages().list(userId='me', q='from:me', maxResults=500, pageToken=page_token).execute()
    sent_messages.extend(res_s.get('messages', []))
    page_token = res_s.get('nextPageToken')
    if not page_token or len(sent_messages) >= 1000:
        break

print(f"Total sent Gmail messages in account: {len(sent_messages)}")

# Fetch headers of sent messages to extract recipients
sent_recipients = {}
for sm in sent_messages:
    m = gmail.users().messages().get(userId='me', id=sm['id'], format='metadata', metadataHeaders=['To', 'Subject', 'Date']).execute()
    hdrs = {h['name'].lower(): h['value'] for h in m['payload'].get('headers', [])}
    to_h = hdrs.get('to', '').lower()
    subject_h = hdrs.get('subject', '')
    date_h = hdrs.get('date', '')
    for em in re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', to_h):
        if em not in sent_recipients:
            sent_recipients[em] = []
        sent_recipients[em].append({'id': sm['id'], 'subject': subject_h, 'date': date_h})

print(f"Unique sent recipient email addresses: {len(sent_recipients)}")

# Fetch all bounces
bounce_query = 'from:mailer-daemon OR from:postmaster OR subject:"Delivery Status Notification (Failure)" OR subject:"Undeliverable"'
res_b = gmail.users().messages().list(userId='me', q=bounce_query, maxResults=500).execute()
bounced_emails = set()
for b in res_b.get('messages', []):
    m = gmail.users().messages().get(userId='me', id=b['id'], format='full').execute()
    snippet = m.get('snippet', '')
    for em in re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', snippet):
        if not any(k in em.lower() for k in ['mailer-daemon', 'googlemail', 'hayaat', 'gmail.com', 'postmaster']):
            bounced_emails.add(em.lower())

print(f"Unique bounced email addresses in Gmail: {len(bounced_emails)}")

# Cross check each Master row
mismatches_found = []
status_counts = {}

for idx, r in enumerate(data):
    row_num = idx + 2
    country = r[0] if len(r) > 0 else ''
    company = r[1] if len(r) > 1 else ''
    email = r[2] if len(r) > 2 else ''
    lead_type = r[3] if len(r) > 3 else ''
    status = r[4] if len(r) > 4 else ''
    date_applied = r[5] if len(r) > 5 else ''
    notes = r[7] if len(r) > 7 else ''
    
    status_counts[status] = status_counts.get(status, 0) + 1
    
    row_emails = [e.lower() for e in re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', email)]
    
    # Check 1: Is marked "To Contact", but Gmail actually sent an email to this address?
    sent_matches = [e for e in row_emails if e in sent_recipients]
    if status == 'To Contact' and sent_matches:
        mismatches_found.append({
            'row': row_num,
            'company': company,
            'email': email,
            'current_status': status,
            'issue': 'Marked To Contact, but Gmail shows email was SENT',
            'details': sent_recipients[sent_matches[0]]
        })
        
    # Check 2: Is marked "Applied", but Gmail shows it BOUNCED?
    bounce_matches = [e for e in row_emails if e in bounced_emails]
    if 'Applied' in status and bounce_matches and 'Undeliverable' not in status:
        mismatches_found.append({
            'row': row_num,
            'company': company,
            'email': email,
            'current_status': status,
            'issue': 'Marked Applied, but Gmail shows it BOUNCED / Undeliverable',
            'details': bounce_matches
        })

print("\n" + "="*70)
print("MASTER TRACKER STATUS BREAKDOWN:")
print("="*70)
for st, cnt in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  • {st or '[Empty]'}: {cnt} rows")

print("\n" + "="*70)
print(f"DISCREPANCIES & AUDIT FLAGS FOUND IN MASTER SHEET: {len(mismatches_found)}")
print("="*70)
for m in mismatches_found:
    print(f"Row {m['row']:3d} | Company: {m['company']} | Email: {m['email']}")
    print(f"  Current Status: {m['current_status']}")
    print(f"  Audit Flag: {m['issue']}")
    print(f"  Details: {m['details']}")
    print("-" * 50)
