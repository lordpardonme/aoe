import sys
import io
from pathlib import Path
from datetime import date, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

today_str = "2026-08-25"
follow_up_str = "2026-09-01"
gmail_id = "1a0384b01263280c"
email_target = "amsterdam@adamsrecruitment.com"
company_target = "Adams Multilingual"

# 1. Update Master Job Tracker
res_m = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
m_rows = res_m.get('values', [])
print(f"Master Job Tracker has {len(m_rows)} rows.")

updated_master = False
for idx, r in enumerate(m_rows[1:], start=2):
    r_padded = r + [''] * (14 - len(r))
    country, company, email, l_type, status, dt_applied, dt_follow, notes, scan_status, role, url, conf, rec_act, dt_scan = r_padded
    if email_target.lower() in email.lower() or company_target.lower() in company.lower():
        print(f"Found match in Master Job Tracker at row {idx}: {company} | {email} | Status: {status}")
        # Columns: A:Country, B:Company, C:Email, D:Type, E:Status, F:Date Applied, G:Follow-up Date, H:Notes, ...
        # Update E, F, G, H
        update_range = f"'Master Job Tracker'!E{idx}:H{idx}"
        new_notes = (notes + " | " if notes else "") + f"Sent Master Product Designer CV + visa sponsorship narrative. Gmail ID: {gmail_id}"
        body = {'values': [['Applied', today_str, follow_up_str, new_notes]]}
        service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body=body).execute()
        print(f"Updated Master Job Tracker row {idx} to Applied.")
        updated_master = True

# 2. Update Agencies Aug 2026 if present
try:
    res_a = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Agencies Aug 2026'!A1:J").execute()
    a_rows = res_a.get('values', [])
    for idx, r in enumerate(a_rows[1:], start=2):
        r_padded = r + [''] * (10 - len(r))
        comp, cat, em, mgr, lnk, stat, dt_add, dt_cont, mid, nts = r_padded
        if email_target.lower() in em.lower() or company_target.lower() in comp.lower():
            print(f"Found match in Agencies Aug 2026 at row {idx}: {comp} | {em}")
            update_range = f"'Agencies Aug 2026'!F{idx}:I{idx}"
            body = {'values': [['Applied', dt_add, today_str, gmail_id]]}
            service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body=body).execute()
            print(f"Updated Agencies Aug 2026 row {idx}.")
except Exception as e:
    print(f"Note on Agencies Aug 2026: {e}")

# 3. Update Priority Outreach Backlog if present
try:
    res_p = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Priority Outreach Backlog'!A1:J").execute()
    p_rows = res_p.get('values', [])
    for idx, r in enumerate(p_rows[1:], start=2):
        r_padded = r + [''] * (10 - len(r))
        prio, src, ctry, comp, em, typ, role, stat, rec_pitch, nts = r_padded
        if email_target.lower() in em.lower() or company_target.lower() in comp.lower():
            print(f"Found match in Priority Outreach Backlog at row {idx}: {comp} | {em}")
            update_range = f"'Priority Outreach Backlog'!H{idx}:J{idx}"
            new_nts = (nts + " | " if nts else "") + f"Applied {today_str}, ID: {gmail_id}"
            body = {'values': [['Applied', rec_pitch, new_nts]]}
            service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body=body).execute()
            print(f"Updated Priority Outreach Backlog row {idx}.")
except Exception as e:
    print(f"Note on Priority Outreach Backlog: {e}")

# 4. Append to Sent By Me
# Columns: A: Company / Lead, B: Email(s), C: Type, D: Status, E: Date Sent, F: Subject, G: Gmail Message ID, H: Tracker Match, I: Recommended Action, J: Source / Owner, K: Notes
sent_by_me_row = [
    "Adams Multilingual Recruitment",
    email_target,
    "Agency",
    "Applied",
    today_str,
    "Product & UI/UX Designer Representation (Amsterdam & Netherlands) - Mohd Hayaat Ali",
    gmail_id,
    "Master Job Tracker",
    f"Follow up {follow_up_str}",
    "Amsterdam sponsor-list lead / Agency",
    "Master Product Designer CV + explicit visa sponsorship & NL availability narrative"
]

res_append = service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    range="'Sent By Me'!A1",
    valueInputOption='RAW',
    insertDataOption='INSERT_ROWS',
    body={'values': [sent_by_me_row]}
).execute()

print(f"Successfully appended row to 'Sent By Me': {res_append.get('updates')}")
print("\nALL GOOGLE SHEET UPDATES COMPLETED CLEANLY!")
