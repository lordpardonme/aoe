import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

for tab in ['YC Startups Aug 2026', 'IT Services Aug 2026']:
    res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=f"'{tab}'!A1:Z50").execute()
    rows = res.get('values', [])
    print(f"=== {tab} (Total rows: {len(rows)}) ===")
    for idx, r in enumerate(rows, start=1):
        if idx <= 15:
            print(f"Row {idx:2d}: {r}")
    print()
