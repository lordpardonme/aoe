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

# Check Master Job Tracker for all Netherlands rows
res_m = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
m_rows = res_m.get('values', [])
headers = m_rows[0]
data = m_rows[1:]

nl_leads = []

for idx, r in enumerate(data, start=2):
    r_padded = r + [''] * (14 - len(r))
    country, company, email, l_type, status, dt_applied, dt_follow, notes, scan_status, role, url, conf, rec_act, dt_scan = r_padded
    if 'netherlands' in country.lower() or 'amsterdam' in country.lower() or 'netherlands' in notes.lower():
        nl_leads.append({
            'row': idx,
            'country': country,
            'company': company,
            'email': email,
            'type': l_type,
            'status': status,
            'notes': notes
        })

print(f"Total Netherlands leads found in Master Job Tracker: {len(nl_leads)}")
print("\n--- NETHERLANDS LEADS BREAKDOWN ---")
for l in nl_leads:
    print(f"Row {l['row']}: [{l['status']}] {l['company']} | {l['email']} | Type: {l['type']}")
