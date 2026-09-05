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
gmail_id = "1a0385b4561b567d"
email_target = "kai.mao@transsion.com"
company_target = "Transsion"

# 1. Update Master Job Tracker (Row 125)
update_range = f"'Master Job Tracker'!E125:H125"
note_val = f"Master Product Designer CV + mobile OS & consumer ecosystem pitch. Gmail ID: {gmail_id}"
body = {'values': [['Applied', today_str, follow_up_str, note_val]]}
service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body=body).execute()
print(f"Updated Master Job Tracker row 125.")

# 2. Update Agencies (Row 69)
try:
    update_range_a = f"'Agencies'!E69:F69"
    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range_a, valueInputOption='RAW', body={'values': [['Applied', today_str]]}).execute()
    print(f"Updated Agencies row 69.")
except Exception as e:
    print(f"Agencies update note: {e}")

# 3. Update Priority Outreach Backlog (Row 22)
try:
    res_p = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Priority Outreach Backlog'!A1:J").execute()
    p_rows = res_p.get('values', [])
    for p_idx, r in enumerate(p_rows[1:], start=2):
        if len(r) > 4 and email_target.lower() in r[4].lower():
            update_range_p = f"'Priority Outreach Backlog'!H{p_idx}:J{p_idx}"
            rec_pitch = r[8] if len(r) > 8 else ''
            nts = r[9] if len(r) > 9 else ''
            new_nts = (nts + " | " if nts else "") + f"Applied {today_str}, ID: {gmail_id}"
            service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range_p, valueInputOption='RAW', body={'values': [['Applied', rec_pitch, new_nts]]}).execute()
            print(f"Updated Priority Backlog row {p_idx}.")
except Exception as e:
    print(f"Priority Backlog note: {e}")

# 4. Append to Sent By Me
sent_row = [
    "Transsion Holdings (Kai Mao)",
    email_target,
    "Direct Employer / Recruiter",
    "Applied",
    today_str,
    "Product & UI/UX Designer (Mobile OS & Consumer Ecosystem) - Mohd Hayaat Ali",
    gmail_id,
    "Master Job Tracker",
    f"Follow up {follow_up_str}",
    "China / Global Sourcing (Shenzhen / Global)",
    "Master Product Designer CV + mobile OS & consumer ecosystem pitch"
]
service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    range="'Sent By Me'!A1",
    valueInputOption='RAW',
    insertDataOption='INSERT_ROWS',
    body={'values': [sent_row]}
).execute()
print(f"Appended to Sent By Me.")

# 5. Append to local staging log
log_path = Path("Job Hunt/resumes/batch-staging-log.md")
current_log = log_path.read_text(encoding='utf-8')
staging_entry = f"| 2026-08-25 15:28 IST | Transsion Holdings (Kai Mao) | Product & UI/UX Designer (Mobile OS) | {email_target} | SENT | `{gmail_id}` | `Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf` | Product & UI/UX Designer (Mobile OS & Consumer Ecosystem) - Mohd Hayaat Ali | Master Product Designer CV + mobile OS & consumer apps narrative |"
new_log = current_log.rstrip() + "\n" + staging_entry + "\n"
log_path.write_text(new_log, encoding='utf-8')
print("Updated local batch-staging-log.md.")

print("TRANSSION LOGGING COMPLETED CLEANLY!")
