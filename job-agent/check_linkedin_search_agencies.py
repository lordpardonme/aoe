import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'LinkedIn Search'!A1:N30").execute()
rows = res.get('values', [])

print(f"Total rows in 'LinkedIn Search': {len(rows)}")
for idx, r in enumerate(rows, start=1):
    r_pad = r + [''] * (14 - len(r))
    print(f"Row {idx:2d} | {r_pad[1]:25s} | {r_pad[4]:15s} | {r_pad[2]:30s} | {r_pad[7]}")
