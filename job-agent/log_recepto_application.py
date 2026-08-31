import sys
import io
from pathlib import Path
from datetime import datetime, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

today_str = datetime.now().strftime('%Y-%m-%d')
followup_str = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
gmail_id = '1a05731ded4133b5'

# 1. Master Job Tracker
master_row = [
    'India', # A: Country / Region
    'Recepto.ai', # B: Company / Agency
    'hr@recepto.ai', # C: Email
    'Direct Employer', # D: Type
    'Applied', # E: Status
    today_str, # F: Date Applied
    followup_str, # G: Follow-up Date
    f'Applied {today_str}: Master Product Designer CV + Recepto Cover Letter | Gmail ID: {gmail_id}', # H: Notes
    'Active Opening', # I: Opening Scan Status
    'Product Designer / Design Engineer', # J: Matched Role(s)
    'https://recepto.ai', # K: Opening Source URL(s)
    'High', # L: Confidence
    'Follow up in 7 days', # M: Recommended Action
    today_str, # N: Scan Date
]

service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    range="'Master Job Tracker'!A:N",
    valueInputOption='USER_ENTERED',
    insertDataOption='INSERT_ROWS',
    body={'values': [master_row]}
).execute()
print("Appended to Master Job Tracker.")

# 2. Sent By Me
sent_row = [
    'Recepto.ai', # A: Company / Lead
    'hr@recepto.ai', # B: Email(s)
    'Direct Employer', # C: Type
    'Applied', # D: Status
    today_str, # E: Date Sent
    'High-Trust Product Designer / Design Engineer - Mohd Hayaat Ali', # F: Subject
    gmail_id, # G: Gmail Message ID
    'Recepto.ai', # H: Tracker Match
    'Follow up in 7 days', # I: Recommended Action
    'Direct Outreach', # J: Source / Owner
    'Master Product Designer CV + Recepto Cover Letter attached', # K: Notes
]

service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    range="'Sent By Me'!A:K",
    valueInputOption='USER_ENTERED',
    insertDataOption='INSERT_ROWS',
    body={'values': [sent_row]}
).execute()
print("Appended to Sent By Me.")

# 3. Check Direct Employers tab
res_de = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Direct Employers'!A1:K").execute()
de_rows = res_de.get('values', [])
found_de = False
for idx, r in enumerate(de_rows):
    if len(r) > 1 and 'recepto' in str(r[1]).lower():
        found_de = True
        print(f"Found in Direct Employers at row {idx+1}")
        break

if not found_de:
    # Append to Direct Employers
    de_row = [
        'India', # A: Country
        'Recepto.ai', # B: Company
        'hr@recepto.ai', # C: Email
        'Applied', # D: Status
        today_str, # E: Date Applied
        followup_str, # F: Follow-up Date
        'Product Designer / Design Engineer', # G: Role
        'https://recepto.ai', # H: URL
        f'Applied {today_str} | Gmail ID: {gmail_id}', # I: Notes
    ]
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="'Direct Employers'!A:I",
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body={'values': [de_row]}
    ).execute()
    print("Appended to Direct Employers.")

print("All sheet logging complete.")
