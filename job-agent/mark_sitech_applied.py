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
gmail_id = "1a0386bf3616ebff"
email_target = "alaa@sitech.me"
company_target = "Sitech"

# 1. Update Master Job Tracker (Row 255)
update_range = f"'Master Job Tracker'!E255:H255"
note_val = f"Master Gulf CV (with photo) + MENA platforms & SaaS pitch. Gmail ID: {gmail_id}"
body = {'values': [['Applied', today_str, follow_up_str, note_val]]}
service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body=body).execute()
print("Updated Master Job Tracker row 255.")

# 2. Update Direct Employers if present
try:
    res_d = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Direct Employers'!A1:N").execute()
    d_rows = res_d.get('values', [])
    for d_idx, r in enumerate(d_rows[1:], start=2):
        if len(r) > 2 and email_target.lower() in r[2].lower():
            update_range_d = f"'Direct Employers'!E{d_idx}:H{d_idx}"
            service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range_d, valueInputOption='RAW', body={'values': [['Applied', today_str, follow_up_str, note_val]]}).execute()
            print(f"Updated Direct Employers row {d_idx}.")
except Exception as e:
    print(f"Direct Employers note: {e}")

# 3. Update Priority Outreach Backlog if present
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
    "Sitech (Alaa)",
    email_target,
    "Direct Employer",
    "Applied",
    today_str,
    "Senior Product Designer / UI-UX (MENA Platforms & SaaS) - Mohd Hayaat Ali",
    gmail_id,
    "Master Job Tracker",
    f"Follow up {follow_up_str}",
    "Jordan / MENA Direct Employer Sourcing",
    "Master Gulf CV (with photo) + MENA platforms & SaaS pitch"
]
service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    range="'Sent By Me'!A1",
    valueInputOption='RAW',
    insertDataOption='INSERT_ROWS',
    body={'values': [sent_row]}
).execute()
print("Appended to Sent By Me.")

# 5. Append to local staging log
log_path = Path("Job Hunt/resumes/batch-staging-log.md")
current_log = log_path.read_text(encoding='utf-8')
staging_entry = f"| 2026-08-25 15:46 IST | Sitech (Jordan / MENA) | Senior Product Designer / UI-UX | {email_target} | SENT | `{gmail_id}` | `Mohd_Hayaat_Ali_Master_Product_Designer_CV_Gulf.pdf` | Senior Product Designer / UI-UX (MENA Platforms & SaaS) - Mohd Hayaat Ali | Master Gulf CV (with photo) + MENA platforms & SaaS pitch |"
new_log = current_log.rstrip() + "\n" + staging_entry + "\n"
log_path.write_text(new_log, encoding='utf-8')
print("Updated local batch-staging-log.md.")

print("SITECH JORDAN LOGGING COMPLETED CLEANLY!")
