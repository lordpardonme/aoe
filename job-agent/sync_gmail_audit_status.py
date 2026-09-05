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

# 1. Update Adams Multilingual (Row 101)
update_range_adams = "'Master Job Tracker'!E101:H101"
body_adams = {'values': [['Applied - Rejected', today_str, '', 'Replied 2026-08-25: Cannot support non-EU sponsorship. Gmail ID: 1a0384b01263280c']]}
service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range_adams, valueInputOption='RAW', body=body_adams).execute()
print("Updated Adams Multilingual to 'Applied - Rejected'.")

# 2. Update Ravecruitment (Row 116)
update_range_rave = "'Master Job Tracker'!E116:H116"
body_rave = {'values': [['Applied - Reply Received', today_str, '', 'Replied 2026-08-25: No current open roles. Gmail ID: 1a038515ef11e043']]}
service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range_rave, valueInputOption='RAW', body=body_rave).execute()
print("Updated Ravecruitment to 'Applied - Reply Received'.")

# 3. Update Sawaeed (Row 120)
update_range_sawaeed = "'Master Job Tracker'!E120:H120"
body_sawaeed = {'values': [['Undeliverable / Bounced', today_str, '', 'Bounced 2026-08-25: Domain sawaeed.ae not found. Gmail ID: 1a03864cbde6f32a']]}
service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range_sawaeed, valueInputOption='RAW', body=body_sawaeed).execute()
print("Updated Sawaeed to 'Undeliverable / Bounced'.")

print("GMAIL RECONCILIATION UPDATES APPLIED TO LIVE SHEET!")
