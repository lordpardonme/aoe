import sys
import re
from pathlib import Path

# Add job-agent to path
sys.path.insert(0, 'job-agent')
from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

# 1. Read staging log
with open('Job Hunt/resumes/batch-staging-log.md', 'r', encoding='utf-8') as f:
    log_content = f.read()

# Format: | Timestamp | Company | Role | Email | Status | Gmail Message ID | PDF Attachment | Subject | Notes |
pattern = r'\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*`?([a-f0-9]+)`?\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|'
matches = re.findall(pattern, log_content)

print(f'Parsed {len(matches)} rows from batch-staging-log.md')

# 2. Get existing message IDs from Sent By Me
res_sent = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Sent By Me!G:G').execute()
existing_sent_ids = set(r[0].strip() for r in res_sent.get('values', []) if r)

new_sent_rows = []
new_master_rows = []

for m in matches:
    timestamp, company, role, email, status, msg_id, attachment, subject, notes = [x.strip() for x in m]
    if msg_id in existing_sent_ids:
        continue
    
    date_sent = timestamp.split(' ')[0]
    
    # Classify type
    lower_corp = (company + " " + role).lower()
    if any(k in lower_corp for k in ['agency', 'consultan', 'recruitment', 'hr', 'staffing', 'talent arabia', 'reach group', 'metamorfs', 'hirextra', 'vyze', 'otb', 'tiger recruitment', 'mindfield', 'rfs hr', 'caliberly', 'parker connect']):
        lead_type = 'Agency'
    elif 'freelance' in lower_corp or 'part-time' in lower_corp:
        lead_type = 'Freelance / Contract'
    else:
        lead_type = 'Direct Employer'
        
    # Sent By Me row: Company, Email, Type, Status, Date Sent, Subject, Gmail Message ID, Tracker Match, Recommended Action, Source / Owner, Notes
    sent_row = [
        company,
        email,
        lead_type,
        'Sent',
        date_sent,
        subject,
        msg_id,
        'Direct Match',
        'Follow up in 7 days',
        'Mohd Hayaat Ali',
        notes
    ]
    new_sent_rows.append(sent_row)
    
    # Master Job Tracker row: Country, Company, Email, Type, Status, Date Applied, Follow-up Date, Notes, Opening Scan Status, Matched Role, Opening URL, Confidence, Recommended Action, Scan Date
    region = 'UAE / Dubai' if any(k in (subject + " " + company + " " + notes).lower() for k in ['dubai', 'uae', 'abu dhabi', 'gulf', 'gcc']) else 'India'
    master_row = [
        region,
        company,
        email,
        lead_type,
        'Applied',
        date_sent,
        '2026-08-31',
        f'{notes} (Gmail ID: {msg_id})',
        'Applied - Sourced via Agent Batch',
        role,
        '',
        'High',
        'Follow up if no response',
        date_sent
    ]
    new_master_rows.append(master_row)

print(f'New rows to append to Sent By Me: {len(new_sent_rows)}')
print(f'New rows to append to Master Job Tracker: {len(new_master_rows)}')

if new_sent_rows:
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range='Sent By Me!A1',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': new_sent_rows}
    ).execute()
    print('Appended new rows to Sent By Me.')

if new_master_rows:
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range='Master Job Tracker!A1',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': new_master_rows}
    ).execute()
    print('Appended new rows to Master Job Tracker.')

# 3. Update Dashboard with Clean & Complete Metrics
dashboard_data = [
    ['Job Hunt Live Operating Dashboard', 'Automated & Synced with Live Gmail & Master Tracker', ''],
    [],
    ['Core Pipeline Metrics (KPI)', 'Live Value / Count', 'Description / Source'],
    ['Total Master Leads Tracked', '=COUNTA(\'Master Job Tracker\'!B2:B)', 'Master Job Tracker total companies'],
    ['Total Outbound Applications Sent', '=COUNTA(\'Sent By Me\'!A2:A)-1', 'All verified outbound Gmail sends'],
    ['Status: Applied (Active Pipeline)', '=COUNTIF(\'Master Job Tracker\'!E2:E,"Applied*")', 'Active submitted applications'],
    ['Status: To Contact (Remaining Master)', '=COUNTIF(\'Master Job Tracker\'!E2:E,"To Contact")', 'Uncontacted leads in Master Tracker'],
    ['Status: Delivery Issues / Bounced', '=COUNTIF(\'Master Job Tracker\'!E2:E,"Undeliverable*")', 'Bounced addresses'],
    ['Follow-ups Scheduled (Active)', '=COUNTIF(\'Master Job Tracker\'!G2:G,"<>")-1', 'Target follow-up calendar rows'],
    ['Overall Response / Reply Rate', '=TEXT(IFERROR((COUNTIF(\'Master Job Tracker\'!E2:E,"*Reply*") + COUNTIF(\'Master Job Tracker\'!E2:E,"*Interview*")) / COUNTIF(\'Master Job Tracker\'!E2:E,"Applied*"), 0), "0.0%")', 'Replies & interview callbacks'],
    [],
    ['August 2026 Batch Queues', 'Uncontacted Count', 'Sheet Location'],
    ['Agencies (Aug 2026 Batch)', '=COUNTIF(\'Agencies Aug 2026\'!F2:F,"To Contact")', 'Agencies Aug 2026 tab'],
    ['IT Services & Software (Aug 2026 Batch)', '=COUNTIF(\'IT Services Aug 2026\'!F2:F,"To Contact")', 'IT Services Aug 2026 tab'],
    ['YC Startups (Aug 2026 Batch)', '=COUNTIF(\'YC Startups Aug 2026\'!F2:F,"To Contact")', 'YC Startups Aug 2026 tab'],
    [],
    ['Lead Sourcing Distribution', 'Count', 'Category'],
    ['Direct Employers Tracked', '=COUNTIF(\'Master Job Tracker\'!D2:D,"Direct Employer")', 'Direct Companies'],
    ['Staffing & Recruitment Agencies', '=COUNTIF(\'Master Job Tracker\'!D2:D,"Agency")', 'Recruitment Agencies'],
    ['Freelance / Contract Mandates', '=COUNTIF(\'Master Job Tracker\'!D2:D,"Freelance*")', 'Freelance / Projects'],
    ['LinkedIn Search Leads', '=COUNTIF(\'Master Job Tracker\'!D2:D,"LinkedIn Search")', 'LinkedIn Sourced'],
    [],
    ['Latest Outbound Activity', 'Live Details', 'Source Sheet Key'],
    ['Latest Sent Company / Lead', '=INDEX(\'Sent By Me\'!A:A, COUNTA(\'Sent By Me\'!A:A))', 'Sent By Me (Last Row)'],
    ['Latest Sent Recipient Email', '=INDEX(\'Sent By Me\'!B:B, COUNTA(\'Sent By Me\'!A:A))', 'Sent By Me (Last Row)'],
    ['Latest Sent Subject Line', '=INDEX(\'Sent By Me\'!F:F, COUNTA(\'Sent By Me\'!A:A))', 'Sent By Me (Last Row)'],
    ['Latest Sent Date', '=INDEX(\'Sent By Me\'!E:E, COUNTA(\'Sent By Me\'!A:A))', 'Sent By Me (Last Row)'],
    ['Latest Gmail Message ID', '=INDEX(\'Sent By Me\'!G:G, COUNTA(\'Sent By Me\'!A:A))', 'Sent By Me (Last Row)']
]

# Clear existing dashboard range first
service.spreadsheets().values().clear(
    spreadsheetId=spreadsheet_id,
    range='Dashboard!A1:Z100'
).execute()

# Write updated dashboard
service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='Dashboard!A1:C28',
    valueInputOption='USER_ENTERED',
    body={'values': dashboard_data}
).execute()

print('Successfully updated and refreshed Dashboard!')
