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

gmail_id = '1a045348df3b07fb'
company = 'Fakhruddin Properties'
email = 'd.dheeraj@fakhruddinproperties.com'
role = 'Creative Specialist'
subject = 'Creative Specialist (Real Estate Brand & Marketing Collateral) - Mohd Hayaat Ali'

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
    if len(r) > 1 and 'fakhruddin' in r[1].lower():
        master_match_idx = i
        print(f"Found existing row in Master Job Tracker at row {i}: {r}")
        break

if master_match_idx:
    range_update = f"'Master Job Tracker'!E{master_match_idx}:H{master_match_idx}"
    update_body = {
        'values': [['Applied', today_str, follow_up_str, f'Tailored Creative Specialist CV sent to d.dheeraj@fakhruddinproperties.com. Gmail ID: {gmail_id}']]
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
        'UAE / Dubai',
        company,
        email,
        'Direct Employer',
        'Applied',
        today_str,
        follow_up_str,
        f'Tailored Creative Specialist CV (luxury brochures, fact sheets, payment plans, OOH, WhatsApp/social creatives, AI tools). UAE relocation. Gmail ID: {gmail_id}',
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
    'Tailored Creative Specialist CV (with photo & UAE credentials) + Portfolio + Drive Showreel. Real estate collateral & AI workflows.'
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
    'Dubai, UAE',
    email,
    today_str,
    'APPLY',
    'Direct hiring post for Creative Specialist (Dubai real estate marketing collateral)',
    f'SENT ({gmail_id})',
    'Tailored Creative Specialist CV with photo & UAE credentials.'
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
