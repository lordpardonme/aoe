import sys
import io
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

res_m = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
rows = res_m.get('values', [])
headers = rows[0]
data = rows[1:]

to_contact_by_country = {}

for idx, r in enumerate(data, start=2):
    r_padded = r + [''] * (14 - len(r))
    country, company, email, l_type, status, dt_applied, dt_follow, notes, scan_status, role, url, conf, rec_act, dt_scan = r_padded
    if status.strip().lower() == 'to contact' and email.strip():
        ctry = country.strip() or 'Unknown'
        if ctry not in to_contact_by_country:
            to_contact_by_country[ctry] = []
        to_contact_by_country[ctry].append({
            'row': idx,
            'company': company,
            'email': email,
            'type': l_type,
            'notes': notes
        })

print("--- REMAINING TO CONTACT LEADS BY COUNTRY ---")
for ctry, leads in sorted(to_contact_by_country.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\n• {ctry} ({len(leads)} leads):")
    for l in leads[:8]:
        print(f"    - Row {l['row']}: {l['company']} ({l['email']}) [{l['type']}]")
    if len(leads) > 8:
        print(f"    ... and {len(leads) - 8} more leads.")
