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

remaining_de = []

for idx, r in enumerate(rows, start=2):
    r_padded = r + [''] * (14 - len(r))
    country, company, email, l_type, status, dt_applied, dt_follow, notes, scan_status, role, url, conf, rec_act, dt_scan = r_padded
    if 'germany' in country.lower() or 'germany' in notes.lower():
        if status.strip().lower() == 'to contact' and email.strip():
            remaining_de.append({
                'row': idx,
                'company': company.strip(),
                'email': email.strip(),
                'type': l_type.strip(),
                'status': status.strip(),
                'notes': notes.strip()
            })

print(f"Total remaining Germany leads 'To Contact': {len(remaining_de)}")
print("\n--- REMAINING GERMANY TARGETS ---")
for i, d in enumerate(remaining_de, 1):
    print(f"{i:2d}. Row {d['row']:3d}: {d['company']:25s} | {d['email']:35s}")
