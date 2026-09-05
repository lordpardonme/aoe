import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Priority Outreach Backlog'!A1:Z100").execute()
rows = res.get('values', [])

print(f"Total rows in 'Priority Outreach Backlog': {len(rows)}\n")

for idx, r in enumerate(rows, start=1):
    print(f"Row {idx:2d}: {r}")
