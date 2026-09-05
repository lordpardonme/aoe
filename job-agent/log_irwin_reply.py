import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

today_str = "2026-08-25"
gmail_id = "1a038be78f7dab3e"

# Update Master Job Tracker Row 106
note_val = f"Replied to Christine 2026-08-25: Inquired on core sectors & creative/brand placement. Gmail ID: {gmail_id}"
body = {'values': [['Applied - Reply Received', today_str, '', note_val]]}
service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!E106:H106", valueInputOption='RAW', body=body).execute()
print("Updated Master Job Tracker Row 106 to 'Applied - Reply Received'.")

# Append to Sent By Me
sent_row = [
    "Irwin & Dow (Christine)",
    "christine@irwinanddow.com",
    "Agency",
    "Sent",
    today_str,
    "RE: Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali",
    gmail_id,
    "Master Job Tracker",
    "Awaiting response on creative placement",
    "UAE Agency Follow-up",
    "Inquired on core recruitment sectors & creative / art direction placement"
]
service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    range="'Sent By Me'!A1",
    valueInputOption='RAW',
    insertDataOption='INSERT_ROWS',
    body={'values': [sent_row]}
).execute()
print("Appended reply to Sent By Me.")
