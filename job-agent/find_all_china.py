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

meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
sheets = [s['properties']['title'] for s in meta['sheets']]

print("Scanning for China leads across all tabs...")

china_leads = []

for s in sheets:
    res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=f"'{s}'!A1:N").execute()
    rows = res.get('values', [])
    for idx, r in enumerate(rows[1:], start=2):
        row_str = " ".join([str(c) for c in r]).lower()
        if 'china' in row_str or 'shanghai' in row_str or 'beijing' in row_str or 'shenzhen' in row_str or 'hong kong' in row_str:
            china_leads.append({'tab': s, 'row': idx, 'data': r})

print(f"Total matching China rows found: {len(china_leads)}")
for item in china_leads:
    print(f"Tab: {item['tab']} | Row {item['row']}: {item['data']}")
