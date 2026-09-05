import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

# Check all sheets to see if any formula or tab has 306
meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
print("Sheets in workbook:")
for s in meta['sheets']:
    title = s['properties']['title']
    res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=f"'{title}'!A1:N").execute()
    data = res.get('values', [])
    print(f"  • Sheet: '{title}' -> Total rows: {len(data)}")

# Deep dive into Master Job Tracker
res_m = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
m_rows = res_m.get('values', [])
print(f"\nMaster Job Tracker total rows (including header): {len(m_rows)}")

status_counts = {}
for i, r in enumerate(m_rows[1:], 2):
    status = r[4] if len(r) > 4 else '[Blank]'
    status_counts[status] = status_counts.get(status, 0) + 1

print("\nMaster Job Tracker Column E (Status) exact breakdown:")
for st, cnt in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  '{st}': {cnt}")

# Check Dashboard formulas and values
res_d = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="Dashboard!A1:C28", valueRenderOption='FORMATTED_VALUE').execute()
print("\nDashboard live values:")
for row in res_d.get('values', []):
    print(f"  {row}")
