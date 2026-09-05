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
rows = res_m.get('values', [])[1:]

country_groups = {}

for idx, r in enumerate(rows, start=2):
    r_padded = r + [''] * (14 - len(r))
    country, company, email, l_type, status, dt_applied, dt_follow, notes, scan_status, role, url, conf, rec_act, dt_scan = r_padded
    if status.strip().lower() == 'to contact' and email.strip():
        ctry_raw = country.strip().lower()
        if 'uae' in ctry_raw or 'dubai' in ctry_raw or 'abu dhabi' in ctry_raw or 'gcc' in ctry_raw or 'mena' in ctry_raw:
            c_name = 'UAE / GCC'
        elif 'germany' in ctry_raw:
            c_name = 'Germany'
        elif 'india' in ctry_raw:
            c_name = 'India'
        elif 'united kingdom' in ctry_raw or 'uk' in ctry_raw:
            c_name = 'United Kingdom'
        elif 'canada' in ctry_raw:
            c_name = 'Canada'
        elif 'france' in ctry_raw:
            c_name = 'France'
        elif 'spain' in ctry_raw:
            c_name = 'Spain'
        elif 'egypt' in ctry_raw:
            c_name = 'Egypt'
        elif 'jordan' in ctry_raw:
            c_name = 'Jordan'
        elif 'indonesia' in ctry_raw:
            c_name = 'Indonesia'
        elif 'remote' in ctry_raw or 'global' in ctry_raw:
            c_name = 'Global / Remote'
        else:
            c_name = country.strip() or 'Unspecified'
        
        country_groups[c_name] = country_groups.get(c_name, 0) + 1

print(f"Total distinct country/region groups with pending leads: {len(country_groups)}")
print("Total pending leads:", sum(country_groups.values()))
print("\n--- BREAKDOWN ---")
for c, cnt in sorted(country_groups.items(), key=lambda x: x[1], reverse=True):
    print(f"• {c}: {cnt} leads")
