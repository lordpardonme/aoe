import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

res_m = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
rows = res_m.get('values', [])[1:]

non_uae = []
uae = []

for idx, r in enumerate(rows, start=2):
    r_padded = r + [''] * (14 - len(r))
    country, company, email, l_type, status, dt_applied, dt_follow, notes, scan_status, role, url, conf, rec_act, dt_scan = r_padded
    st = status.strip().lower()
    
    if st == 'to contact' and email.strip():
        ctry = country.strip()
        lead_info = {
            'row': idx,
            'country': ctry,
            'company': company.strip(),
            'email': email.strip(),
            'type': l_type.strip(),
            'role': role.strip(),
            'notes': notes.strip()
        }
        ctry_raw = ctry.lower()
        if 'uae' in ctry_raw or 'dubai' in ctry_raw or 'abu dhabi' in ctry_raw or 'gcc' in ctry_raw or 'mena' in ctry_raw:
            uae.append(lead_info)
        else:
            non_uae.append(lead_info)

print(f"=== NON-UAE LEADS TO CONTACT ({len(non_uae)}) ===")
for l in non_uae:
    print(f"Row {l['row']} | {l['country']} | {l['company']} | {l['email']} | Type: {l['type']} | Role: {l['role']}")

print(f"\n=== UAE LEADS TO CONTACT ({len(uae)} total, showing first 15) ===")
for l in uae[:15]:
    print(f"Row {l['row']} | {l['country']} | {l['company']} | {l['email']} | Type: {l['type']} | Role: {l['role']}")
