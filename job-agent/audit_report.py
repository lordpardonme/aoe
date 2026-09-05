import sys
import io
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
gmail = build('gmail', 'v1', credentials=creds)
sheets = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

# Read Master Job Tracker
res_master = sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
master_rows = res_master.get('values', [])
master_headers = master_rows[0]
master_data = master_rows[1:]

# Read Sent By Me
res_sent = sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Sent By Me'!A1:K").execute()
sent_rows = res_sent.get('values', [])
sent_headers = sent_rows[0]
sent_data = sent_rows[1:]

# Read Social Leads
res_social = sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Social Leads Jul 2026'!A1:J").execute()
social_rows = res_social.get('values', [])
social_headers = social_rows[0]
social_data = social_rows[1:]

print("=====================================================================")
print("FULL READ-ONLY GMAIL AUDIT & CROSS-CHECK REPORT")
print("=====================================================================")

# --- 1. BOUNCES AUDIT ---
print("\n[1] BOUNCES & DELIVERY FAILURES DETECTED IN GMAIL:")
bounce_query = 'from:mailer-daemon OR from:postmaster OR subject:"Delivery Status Notification (Failure)" OR subject:"Undeliverable"'
res_b = gmail.users().messages().list(userId='me', q=bounce_query, maxResults=100).execute()
bounces_found = []

for b in res_b.get('messages', []):
    m = gmail.users().messages().get(userId='me', id=b['id'], format='full').execute()
    snippet = m.get('snippet', '')
    headers = {h['name'].lower(): h['value'] for h in m['payload'].get('headers', [])}
    date = headers.get('date', '')
    
    # Extract failed recipient email
    email_matches = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', snippet)
    target_email = None
    for em in email_matches:
        if not any(k in em.lower() for k in ['mailer-daemon', 'googlemail', 'hayaat', 'gmail.com', 'postmaster']):
            target_email = em.lower()
            break
            
    # Find matching company in Master / Sent By Me
    matched_companies = []
    for r in master_data:
        if len(r) > 2 and target_email and target_email in r[2].lower():
            matched_companies.append(f"Master: {r[1]} (Status: {r[4] if len(r) > 4 else 'N/A'})")
    for r in sent_data:
        if len(r) > 1 and target_email and target_email in r[1].lower():
            matched_companies.append(f"Sent By Me: {r[0]}")
            
    bounces_found.append({
        'msg_id': b['id'],
        'email': target_email,
        'date': date,
        'matched': list(set(matched_companies)),
        'snippet': snippet[:120]
    })

print(f"Total bounce notifications: {len(bounces_found)}")
for i, bf in enumerate(bounces_found, 1):
    print(f" {i:2d}. Failed Email: {bf['email']}")
    print(f"     Date: {bf['date']}")
    print(f"     Matched Tracker Record: {', '.join(bf['matched']) if bf['matched'] else 'Not in tracker'}")
    print(f"     Snippet: {bf['snippet']}")
    print()

# --- 2. JOB REJECTIONS AUDIT ---
print("\n[2] REJECTIONS FROM 'Job rejections' LABEL & KEYWORD SEARCH:")
rejections_found = []
res_r = gmail.users().messages().list(userId='me', labelIds=['Label_1022348670332542993'], maxResults=100).execute()

for r in res_r.get('messages', []):
    m = gmail.users().messages().get(userId='me', id=r['id'], format='full').execute()
    snippet = m.get('snippet', '')
    headers = {h['name'].lower(): h['value'] for h in m['payload'].get('headers', [])}
    from_h = headers.get('from', '')
    subject = headers.get('subject', '')
    date = headers.get('date', '')
    
    # Try matching to company
    matched_comp = None
    for row in master_data:
        comp_name = row[1] if len(row) > 1 else ''
        comp_clean = re.sub(r'[^a-zA-Z0-9]', '', comp_name.lower())
        if len(comp_clean) >= 4 and (comp_clean in re.sub(r'[^a-zA-Z0-9]', '', subject.lower()) or comp_clean in re.sub(r'[^a-zA-Z0-9]', '', from_h.lower())):
            matched_comp = f"Master: {comp_name} (Row status: {row[4] if len(row) > 4 else 'N/A'})"
            break
            
    rejections_found.append({
        'msg_id': r['id'],
        'from': from_h,
        'subject': subject,
        'date': date,
        'matched': matched_comp,
        'snippet': snippet[:120]
    })

print(f"Total rejection emails: {len(rejections_found)}")
for i, rf in enumerate(rejections_found, 1):
    print(f" {i:2d}. From: {rf['from']}")
    print(f"     Subject: {rf['subject']}")
    print(f"     Date: {rf['date']}")
    print(f"     Matched Tracker Record: {rf['matched'] or 'Direct ATS/Portal Rejection'}")
    print(f"     Snippet: {rf['snippet']}")
    print()

# --- 3. REPLIES & INTERVIEW RESPONSES AUDIT ---
print("\n[3] INCOMING CANDIDATE REPLIES & RECRUITER THREADS:")
replies_found = []
res_in = gmail.users().messages().list(userId='me', q='label:INBOX -from:me', maxResults=100).execute()

for item in res_in.get('messages', []):
    m = gmail.users().messages().get(userId='me', id=item['id'], format='full').execute()
    snippet = m.get('snippet', '')
    headers = {h['name'].lower(): h['value'] for h in m['payload'].get('headers', [])}
    from_h = headers.get('from', '')
    subject = headers.get('subject', '')
    date = headers.get('date', '')
    
    # Filter for real replies to our applications
    if subject.lower().startswith('re:') or any(k in subject.lower() for k in ['application', 'interview', 'hiring', 'designer']):
        if not any(k in from_h.lower() for k in ['totaljobs', 'linkedin job alerts', 'naukrigulf', 'indeed', 'builtin']):
            replies_found.append({
                'msg_id': item['id'],
                'from': from_h,
                'subject': subject,
                'date': date,
                'snippet': snippet[:140]
            })

print(f"Total human/recruiter replies & auto-responses: {len(replies_found)}")
for i, rep in enumerate(replies_found, 1):
    print(f" {i:2d}. From: {rep['from']}")
    print(f"     Subject: {rep['subject']}")
    print(f"     Date: {rep['date']}")
    print(f"     Snippet: {rep['snippet']}")
    print()
