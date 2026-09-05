import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

today_str = "2026-08-25"
follow_up_str = "2026-09-01"
new_email = "lilium@anchor.eu"
gmail_id = "1a038da23c605c2f"

# 1. Update Master Job Tracker Row 207 (Email, Status, Date, Notes)
update_range = "'Master Job Tracker'!C207:H207"
note_val = f"Master Germany CV + electric air mobility, vertiport booking & IoT fleet dispatch. Updated contact: lilium@anchor.eu | Gmail ID: {gmail_id}"
body = {'values': [[new_email, 'Direct Employer', 'Applied', today_str, follow_up_str, note_val]]}
service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body=body).execute()
print("Updated Master Job Tracker row 207 with lilium@anchor.eu.")

# 2. Append to Sent By Me
sent_row = [
    "Lilium (Anchor)",
    new_email,
    "Direct Employer",
    "Applied",
    today_str,
    "Senior Product Designer (Aviation Operations & Passenger Interface UX) - Mohd Hayaat Ali",
    gmail_id,
    "Master Job Tracker",
    f"Follow up {follow_up_str}",
    "Germany Direct Employer Sourcing",
    "Master Germany CV + electric air mobility, vertiport booking, IoT fleet dispatch & safety UI"
]
service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    range="'Sent By Me'!A1",
    valueInputOption='RAW',
    insertDataOption='INSERT_ROWS',
    body={'values': [sent_row]}
).execute()
print("Appended to Sent By Me.")

# 3. Append to local staging log
log_path = Path("Job Hunt/resumes/batch-staging-log.md")
current_log = log_path.read_text(encoding='utf-8')
staging_entry = f"| 2026-08-25 17:47 IST | Lilium (Munich) | Senior Product Designer / UI-UX | {new_email} | SENT | `{gmail_id}` | `Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf` | Senior Product Designer (Aviation Operations & Passenger Interface UX) - Mohd Hayaat Ali | Master Germany CV + electric air mobility & vertiport booking pitch |"
new_log = current_log.rstrip() + "\n" + staging_entry + "\n"
log_path.write_text(new_log, encoding='utf-8')
print("Updated local batch-staging-log.md.")

print("LILIUM ANCHOR UPDATE COMPLETED CLEANLY!")
