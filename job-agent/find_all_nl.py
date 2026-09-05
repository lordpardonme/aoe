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

print("Checking tabs for Netherlands leads...")

all_nl = []

for s in sheets:
    res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=f"'{s}'!A1:N").execute()
    rows = res.get('values', [])
    for idx, r in enumerate(rows[1:], start=2):
        row_str = " ".join([str(c) for c in r]).lower()
        if 'netherlands' in row_str or '.nl' in row_str or 'amsterdam' in row_str:
            all_nl.append({'tab': s, 'row': idx, 'data': r})

print(f"Total matching rows across all tabs: {len(all_nl)}")
for item in all_nl:
    print(f"Tab: {item['tab']} | Row {item['row']}: {item['data'][:6]}")
