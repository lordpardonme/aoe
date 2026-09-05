import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

# Check Master Job Tracker Agencies with status 'To Contact'
res_m = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
m_rows = res_m.get('values', [])[1:]

master_agencies_to_contact = []
for idx, r in enumerate(m_rows, start=2):
    r_pad = r + [''] * (14 - len(r))
    country, comp, email, l_type, status, dt_app, dt_fol, notes, sc_st, role, url, conf, rec, sc_dt = r_pad
    if 'agency' in l_type.lower() and status.strip().lower() == 'to contact' and email.strip():
        master_agencies_to_contact.append({'row': idx, 'country': country, 'company': comp, 'email': email, 'notes': notes})

print(f"Master Job Tracker pending agencies: {len(master_agencies_to_contact)}")
for a in master_agencies_to_contact:
    print(f"  Row {a['row']:3d} | {a['country']:15s} | {a['company']:30s} | {a['email']}")

# Check Agencies tab
res_a = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Agencies'!A1:N").execute()
a_rows = res_a.get('values', [])[1:]
agencies_tab_to_contact = []
for idx, r in enumerate(a_rows, start=2):
    r_pad = r + [''] * (14 - len(r))
    country, comp, email, l_type, status, dt_app, dt_fol, notes, sc_st, role, url, conf, rec, sc_dt = r_pad
    if status.strip().lower() == 'to contact' and email.strip():
        agencies_tab_to_contact.append({'row': idx, 'country': country, 'company': comp, 'email': email})

print(f"\nAgencies tab pending: {len(agencies_tab_to_contact)}")
for a in agencies_tab_to_contact:
    print(f"  Row {a['row']:3d} | {a['country']:15s} | {a['company']:30s} | {a['email']}")

# Check Agencies Aug 2026 tab
res_aug = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Agencies Aug 2026'!A1:Z").execute()
aug_rows = res_aug.get('values', [])[1:]
aug_to_contact = []
for idx, r in enumerate(aug_rows, start=2):
    if len(r) > 4 and r[4].strip().lower() == 'to contact' and len(r) > 2 and r[2].strip():
        aug_to_contact.append({'row': idx, 'company': r[1], 'email': r[2]})

print(f"\nAgencies Aug 2026 tab pending: {len(aug_to_contact)}")

# Check IT Services Aug 2026 tab
res_it = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'IT Services Aug 2026'!A1:Z").execute()
it_rows = res_it.get('values', [])[1:]
it_to_contact = []
for idx, r in enumerate(it_rows, start=2):
    if len(r) > 4 and r[4].strip().lower() == 'to contact' and len(r) > 2 and r[2].strip():
        it_to_contact.append({'row': idx, 'company': r[1], 'email': r[2]})

print(f"\nIT Services Aug 2026 tab pending: {len(it_to_contact)}")
