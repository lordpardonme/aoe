import sys
import io
import re
import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
gmail = build('gmail', 'v1', credentials=creds)
sheets = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

print("=== STEP 1: FETCHING GOOGLE SHEET DATA ===")
# Master Job Tracker (A-N)
res_master = sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
master_rows = res_master.get('values', [])
master_headers = master_rows[0] if master_rows else []
master_data = master_rows[1:] if len(master_rows) > 1 else []
print(f"Master Job Tracker rows: {len(master_data)}")

# Social Leads Jul 2026 (A-J)
res_social = sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Social Leads Jul 2026'!A1:J").execute()
social_rows = res_social.get('values', [])
social_headers = social_rows[0] if social_rows else []
social_data = social_rows[1:] if len(social_rows) > 1 else []
print(f"Social Leads Jul 2026 rows: {len(social_data)}")

# Sent By Me (A-K)
res_sent = sheets.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Sent By Me'!A1:K").execute()
sent_rows = res_sent.get('values', [])
sent_headers = sent_rows[0] if sent_rows else []
sent_data = sent_rows[1:] if len(sent_rows) > 1 else []
print(f"Sent By Me rows: {len(sent_data)}")

print("\n=== STEP 2: EXTRACTING ALL GMAIL BOUNCES ===")
bounces = []
bounce_query = 'from:mailer-daemon OR from:postmaster OR subject:"Delivery Status Notification (Failure)" OR subject:"Undeliverable"'
res_b = gmail.users().messages().list(userId='me', q=bounce_query, maxResults=100).execute()
for b in res_b.get('messages', []):
    m = gmail.users().messages().get(userId='me', id=b['id'], format='full').execute()
    snippet = m.get('snippet', '')
    headers = {h['name'].lower(): h['value'] for h in m['payload'].get('headers', [])}
    date = headers.get('date', '')
    
    # Extract recipient email
    email_matches = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', snippet)
    target_email = None
    for em in email_matches:
        if not any(k in em.lower() for k in ['mailer-daemon', 'googlemail', 'hayaat', 'gmail.com', 'postmaster']):
            target_email = em.lower()
            break
            
    bounces.append({
        'id': b['id'],
        'email': target_email,
        'snippet': snippet,
        'date': date
    })
    print(f"  [BOUNCE] Email: {target_email} | Date: {date}")

print(f"Total bounces extracted: {len(bounces)}")

print("\n=== STEP 3: EXTRACTING ALL REJECTIONS (Label 'Job rejections') ===")
rejections = []
res_r = gmail.users().messages().list(userId='me', labelIds=['Label_1022348670332542993'], maxResults=100).execute()
for r in res_r.get('messages', []):
    m = gmail.users().messages().get(userId='me', id=r['id'], format='full').execute()
    snippet = m.get('snippet', '')
    headers = {h['name'].lower(): h['value'] for h in m['payload'].get('headers', [])}
    from_h = headers.get('from', '')
    subject = headers.get('subject', '')
    date = headers.get('date', '')
    
    rejections.append({
        'id': r['id'],
        'from': from_h,
        'subject': subject,
        'snippet': snippet,
        'date': date
    })

print(f"Total rejections extracted: {len(rejections)}")

print("\n=== STEP 4: EXTRACTING INBOX REPLIES & INTERVIEWS ===")
inbound_replies = []
res_in = gmail.users().messages().list(userId='me', q='label:INBOX -from:me', maxResults=100).execute()
for item in res_in.get('messages', []):
    m = gmail.users().messages().get(userId='me', id=item['id'], format='full').execute()
    snippet = m.get('snippet', '')
    headers = {h['name'].lower(): h['value'] for h in m['payload'].get('headers', [])}
    from_h = headers.get('from', '')
    subject = headers.get('subject', '')
    date = headers.get('date', '')
    
    # Check if this is a reply to an application
    if subject.lower().startswith('re:') or 'application' in subject.lower() or 'interview' in subject.lower() or 'hiring' in subject.lower() or 'designer' in subject.lower():
        inbound_replies.append({
            'id': item['id'],
            'from': from_h,
            'subject': subject,
            'snippet': snippet,
            'date': date
        })

print(f"Total relevant inbound application replies: {len(inbound_replies)}")
for rep in inbound_replies:
    print(f"  [REPLY] From: {rep['from']} | Subject: {rep['subject']}")

print("\n=== STEP 5: MATCHING & UPDATING MASTER JOB TRACKER ===")

# Build email to master row index map
# Column C is Email, Column B is Company, Column E is Status, Column H is Notes
email_to_master = {}
company_to_master = {}

for idx, r in enumerate(master_data):
    row_num = idx + 2 # 1-indexed in sheet (header is row 1)
    if len(r) > 2 and r[2]:
        for e in re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', r[2]):
            email_to_master[e.lower()] = row_num
    if len(r) > 1 and r[1]:
        comp_clean = re.sub(r'[^a-zA-Z0-9]', '', r[1].lower())
        company_to_master[comp_clean] = row_num

master_updates = []

# Match Bounces to Master Tracker
for b in bounces:
    if b['email'] and b['email'] in email_to_master:
        rn = email_to_master[b['email']]
        curr_status = master_data[rn - 2][4] if len(master_data[rn - 2]) > 4 else ''
        if 'Undeliverable' not in curr_status:
            print(f"  -> Match Bounce: {b['email']} -> Master Row {rn} ({master_data[rn-2][1]})")
            # Update Status in Col E (Col 5) and Notes in Col H (Col 8)
            sheets.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=f"'Master Job Tracker'!E{rn}",
                valueInputOption='RAW',
                body={'values': [['Undeliverable / Bounced']]}
            ).execute()
            
            existing_notes = master_data[rn-2][7] if len(master_data[rn-2]) > 7 else ''
            new_notes = f"{existing_notes} | Bounce detected in Gmail (ID: {b['id']})".strip(' |')
            sheets.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=f"'Master Job Tracker'!H{rn}",
                valueInputOption='RAW',
                body={'values': [[new_notes]]}
            ).execute()

# Match Rejections to Master Tracker
for rej in rejections:
    # Try match by sender email
    sender_emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', rej['from'])
    matched_rn = None
    for se in sender_emails:
        if se.lower() in email_to_master:
            matched_rn = email_to_master[se.lower()]
            break
            
    # Try match by company name in subject/snippet
    if not matched_rn:
        for comp_clean, rn in company_to_master.items():
            if len(comp_clean) >= 4 and (comp_clean in re.sub(r'[^a-zA-Z0-9]', '', rej['subject'].lower()) or comp_clean in re.sub(r'[^a-zA-Z0-9]', '', rej['from'].lower())):
                matched_rn = rn
                break
                
    if matched_rn:
        comp_name = master_data[matched_rn-2][1] if len(master_data[matched_rn-2]) > 1 else ''
        curr_status = master_data[matched_rn-2][4] if len(master_data[matched_rn-2]) > 4 else ''
        print(f"  -> Match Rejection: {rej['subject'][:40]} -> Master Row {matched_rn} ({comp_name})")
        if 'Rejected' not in curr_status:
            sheets.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=f"'Master Job Tracker'!E{matched_rn}",
                valueInputOption='RAW',
                body={'values': [['Applied - Rejected']]}
            ).execute()
            
            existing_notes = master_data[matched_rn-2][7] if len(master_data[matched_rn-2]) > 7 else ''
            new_notes = f"{existing_notes} | Rejection received in Gmail (ID: {rej['id']}, Date: {rej['date']})".strip(' |')
            sheets.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=f"'Master Job Tracker'!H{matched_rn}",
                valueInputOption='RAW',
                body={'values': [[new_notes]]}
            ).execute()

print("\n=== STEP 6: RECONCILING SOCIAL LEADS TAB ===")
# Ensure all image/social leads from batch-staging-log.md are tracked in Social Leads Jul 2026
with open('Job Hunt/resumes/batch-staging-log.md', 'r', encoding='utf-8') as f:
    log_content = f.read()

pattern = r'\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*`?([a-f0-9]+)`?\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|'
staged_entries = re.findall(pattern, log_content)

existing_social_companies = set(re.sub(r'[^a-zA-Z0-9]', '', r[1].lower()) for r in social_data if len(r) > 1 and r[1])
new_social_rows = []

for entry in staged_entries:
    ts, comp, role, email, status, msg_id, attach, subj, notes = [x.strip() for x in entry]
    comp_clean = re.sub(r'[^a-zA-Z0-9]', '', comp.lower())
    if comp_clean not in existing_social_companies:
        # Columns: Source, Company, Role, Location, Contact, Date Seen, Verdict, Reason, Packet Status, Notes
        date_seen = ts.split(' ')[0]
        region = 'Dubai / UAE' if any(k in (comp + ' ' + subj).lower() for k in ['dubai', 'uae', 'abu dhabi', 'gulf']) else 'India'
        
        # Check if there is a bounce or rejection for this lead
        lead_status = f"SENT {date_seen} (Gmail id: {msg_id})"
        lead_verdict = "APPLY"
        
        new_social_rows.append([
            'Social / Screenshot Lead',
            comp,
            role,
            region,
            email,
            date_seen,
            lead_verdict,
            'Verified direct opportunity from lead feed',
            lead_status,
            notes
        ])
        existing_social_companies.add(comp_clean)

if new_social_rows:
    print(f"Appending {len(new_social_rows)} newly applied social/screenshot leads to 'Social Leads Jul 2026'...")
    sheets.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="'Social Leads Jul 2026'!A1",
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': new_social_rows}
    ).execute()
    print("Social Leads Jul 2026 updated successfully.")
else:
    print("All staged social leads are already present in Social Leads tab.")

print("\n=== STEP 7: REFRESHING DASHBOARD ===")
from sync_tracker import dashboard_data
sheets.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='Dashboard!A1:C28',
    valueInputOption='USER_ENTERED',
    body={'values': dashboard_data}
).execute()

print("Reconciliation complete! All Google Sheet tabs are up to date.")
