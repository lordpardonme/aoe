import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

res_m = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
rows = res_m.get('values', [])[1:]

de_leads = []

for idx, r in enumerate(rows, start=2):
    r_padded = r + [''] * (14 - len(r))
    country, company, email, l_type, status, dt_applied, dt_follow, notes, scan_status, role, url, conf, rec_act, dt_scan = r_padded
    if 'germany' in country.lower() or 'germany' in notes.lower():
        de_leads.append({
            'row': idx,
            'company': company,
            'email': email,
            'type': l_type,
            'status': status,
            'notes': notes
        })

print(f"Total Germany leads in Master Tracker: {len(de_leads)}")

agencies = [l for l in de_leads if 'agency' in l['type'].lower() or 'agency' in l['notes'].lower()]
direct_employers = [l for l in de_leads if 'direct employer' in l['type'].lower() or ('agency' not in l['type'].lower() and 'agency' not in l['notes'].lower())]

print(f"\nAgencies: {len(agencies)}")
for a in agencies:
    print(f"  - Row {a['row']}: [{a['status']}] {a['company']} ({a['email']})")

print(f"\nDirect Employers: {len(direct_employers)}")
for d in direct_employers:
    print(f"  - Row {d['row']}: [{d['status']}] {d['company']} ({d['email']})")
