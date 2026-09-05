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

agency_backlog = []
agency_applied = []
other_backlog = []

for idx, r in enumerate(data, start=2):
    r_padded = r + [''] * (14 - len(r))
    country, company, email, l_type, status, dt_applied, dt_follow, notes, scan_status, role, url, conf, rec_act, dt_scan = r_padded
    
    is_agency = 'agency' in l_type.lower() or 'recruiter' in l_type.lower() or 'agency' in notes.lower() or 'consultancy' in company.lower()
    
    if status.strip().lower() == 'to contact':
        if is_agency:
            agency_backlog.append({
                'row': idx,
                'country': country or 'Unknown',
                'company': company,
                'email': email,
                'type': l_type,
                'notes': notes
            })
        else:
            other_backlog.append({
                'row': idx,
                'country': country or 'Unknown',
                'company': company,
                'email': email,
                'type': l_type,
                'notes': notes
            })
    elif 'applied' in status.strip().lower():
        if is_agency:
            agency_applied.append(company)

print(f"Total Agencies in Master Backlog (To Contact): {len(agency_backlog)}")
print(f"Total Agencies already Applied: {len(agency_applied)}")
print(f"Total Direct Employers / Startups in Backlog: {len(other_backlog)}")

# Country breakdown of agency backlog
country_counts = {}
for a in agency_backlog:
    c = a['country'].strip() or 'Unknown'
    country_counts[c] = country_counts.get(c, 0) + 1

print("\n--- AGENCY BACKLOG BY REGION ---")
for c, cnt in sorted(country_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"• {c}: {cnt} agencies")

print("\n--- DETAILED AGENCY BACKLOG LIST ---")
for a in agency_backlog:
    print(f"Row {a['row']}: [{a['country']}] {a['company']} | {a['email']}")
