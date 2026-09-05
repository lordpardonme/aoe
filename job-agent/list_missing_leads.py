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

missing_email_leads = []
for i, r in enumerate(rows, 2):
    row = r + [''] * (14 - len(r))
    country, comp, email, l_type, status, dt_app, dt_foll, notes, scan_st, role, url, conf, rec_act, dt_scan = row
    if status.strip().lower() == 'to contact':
        em = email.strip()
        if not em or any(k in em.lower() for k in ['find', 'linkedin', 'website', 'portal', 'n/a', 'none']) or '@' not in em:
            missing_email_leads.append({
                'row': i,
                'company': comp.strip(),
                'country': country.strip(),
                'type': l_type.strip(),
                'notes': notes.strip(),
                'url': url.strip()
            })

print(f"Total leads needing contact email discovery: {len(missing_email_leads)}")
print("\n--- FIRST 30 TARGETS ---")
for x in missing_email_leads[:30]:
    print(f"Row {x['row']:3d} | {x['company']:<35} | {x['country']:<15} | Type: {x['type']}")
