import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
rows = res.get('values', [])[1:]

still_missing = []
for i, r in enumerate(rows, 2):
    row = r + [''] * (14 - len(r))
    country, comp, email, l_type, status, dt_app, dt_foll, notes, scan_st, role, url, conf, rec_act, dt_scan = row
    em = email.strip()
    if status.strip().lower() == 'to contact' and (not em or any(k in em.lower() for k in ['find', 'linkedin', 'website', 'portal', 'n/a', 'none', '[']) or '@' not in em):
        still_missing.append({'row': i, 'company': comp.strip(), 'country': country.strip(), 'type': l_type.strip()})

print(f"Total remaining companies without direct email: {len(still_missing)}")
for idx, x in enumerate(still_missing, 1):
    print(f"{idx:3d}. Row {x['row']:3d} | {x['company']:<35} | {x['country']:<15} | {x['type']}")
