import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

# Read Master Job Tracker emails
res_m = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
m_rows = res_m.get('values', [])
existing_emails = set()
for r in m_rows[1:]:
    if len(r) > 2 and r[2].strip():
        existing_emails.add(r[2].strip().lower())

# Read Agencies Aug 2026
res_aug = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Agencies Aug 2026'!A1:J").execute()
aug_rows = res_aug.get('values', [])[1:]

to_append_master = []
for r in aug_rows:
    comp = r[0] if len(r) > 0 else ''
    cat = r[1] if len(r) > 1 else ''
    email = r[2] if len(r) > 2 else ''
    hm = r[3] if len(r) > 3 else ''
    status = r[5] if len(r) > 5 else 'Applied'
    dt_c = r[7] if len(r) > 7 else '2026-08-25'
    gid = r[8] if len(r) > 8 else ''
    notes = f"{hm} | Agencies Aug 2026 | Gmail ID: {gid}".strip(' |')
    
    if email.strip().lower() not in existing_emails:
        master_row = [
            "India",
            comp,
            email,
            "Agency",
            "Applied",
            dt_c,
            "2026-09-01",
            notes,
            "Targeted",
            "Senior Product Designer",
            "",
            "High",
            "Follow up on 2026-09-01",
            dt_c
        ]
        to_append_master.append(master_row)

print(f"New rows to append to Master Job Tracker: {len(to_append_master)}")

if to_append_master:
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="'Master Job Tracker'!A1",
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': to_append_master}
    ).execute()
    print("Appended new rows to Master Job Tracker successfully!")
