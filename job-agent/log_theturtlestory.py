import sys
import io
import time
from datetime import datetime, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

today_str = datetime.now().strftime('%Y-%m-%d')
follow_up_str = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

gmail_id = '1a0420c583550315'
company = 'The Turtle Story'
email = 'careers@theturtlestory.com'
role = 'Senior Video Editor'
subject = 'Senior Video Editor (Thane / Mumbai Studio) - Mohd Hayaat Ali'

def retry_api(fn, max_retries=5, delay=2):
    for i in range(max_retries):
        try:
            return fn()
        except Exception as e:
            print(f"Attempt {i+1} failed with error: {e}. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2
    raise Exception("Max retries exceeded.")

# 1. Check Master Job Tracker
res_m = retry_api(lambda: service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute())
m_rows = res_m.get('values', [])
print(f"Master Job Tracker current total rows: {len(m_rows)}")

master_match_idx = None
for i, r in enumerate(m_rows[1:], start=2):
    if len(r) > 1 and 'turtle' in r[1].lower():
        master_match_idx = i
        print(f"Found existing row in Master Job Tracker at row {i}: {r}")
        break

if master_match_idx:
    range_update = f"'Master Job Tracker'!E{master_match_idx}:H{master_match_idx}"
    update_body = {
        'values': [['Applied', today_str, follow_up_str, f'Tailored Senior Video Editor CV sent. Gmail ID: {gmail_id}']]
    }
    retry_api(lambda: service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_update,
        valueInputOption='USER_ENTERED',
        body=update_body
    ).execute())
    print(f"Updated Master Job Tracker row {master_match_idx}")
else:
    new_master_row = [
        'India / Mumbai',
        company,
        email,
        'Direct Employer',
        'Applied',
        today_str,
        follow_up_str,
        f'Tailored Senior Video Editor CV + portfolio & drive showreel. WFO Wagle Estate Thane Mumbai. Gmail ID: {gmail_id}',
        'Applied',
        role,
        email,
        'High',
        f'Follow up {follow_up_str}',
        today_str
    ]
    retry_api(lambda: service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="'Master Job Tracker'!A:N",
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body={'values': [new_master_row]}
    ).execute())
    print("Appended new row to Master Job Tracker")

# 2. Append to Sent By Me
new_sent_row = [
    company,
    email,
    'Direct Employer',
    'Applied',
    today_str,
    subject,
    gmail_id,
    company,
    f'Follow up on {follow_up_str}',
    'User Sourced Job Post',
    'Tailored Senior Video Editor CV + Creative Showreel + Visual Portfolio. WFO Thane Mumbai.'
]
retry_api(lambda: service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    range="'Sent By Me'!A:K",
    valueInputOption='USER_ENTERED',
    insertDataOption='INSERT_ROWS',
    body={'values': [new_sent_row]}
).execute())
print("Appended new row to Sent By Me")

# 3. Append to Social Leads Jul 2026 if tab exists
new_social_row = [
    'User Sourced Job Post',
    company,
    role,
    'Wagle Estate, Thane, Mumbai',
    email,
    today_str,
    'APPLY',
    'Direct hiring post for Senior Video Editor in Mumbai/Thane',
    f'SENT ({gmail_id})',
    'Full-time WFO Thane Mumbai; tailored Senior Video Editor CV attached.'
]
try:
    retry_api(lambda: service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="'Social Leads Jul 2026'!A:J",
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body={'values': [new_social_row]}
    ).execute())
    print("Appended new row to Social Leads Jul 2026")
except Exception as e:
    print(f"Could not append to Social Leads tab: {e}")

print("Sheet logging completed successfully.")
