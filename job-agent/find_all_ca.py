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

meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
sheets = [s['properties']['title'] for s in meta['sheets']]

print("Scanning for Canada leads across all tabs...")

ca_leads = []

for s in sheets:
    res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=f"'{s}'!A1:N").execute()
    rows = res.get('values', [])
    for idx, r in enumerate(rows[1:], start=2):
        row_str = " ".join([str(c) for c in r]).lower()
        if 'canada' in row_str or 'toronto' in row_str or 'vancouver' in row_str or 'montreal' in row_str or 'calgary' in row_str or 'ottawa' in row_str:
            ca_leads.append({'tab': s, 'row': idx, 'data': r})

print(f"Total matching Canada rows found: {len(ca_leads)}")
for item in ca_leads:
    print(f"Tab: {item['tab']} | Row {item['row']}: {item['data'][:7]}")
