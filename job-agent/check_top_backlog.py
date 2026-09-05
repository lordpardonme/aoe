import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

# Check tabs
meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
sheets = [s['properties']['title'] for s in meta['sheets']]
print("Tabs in sheet:", sheets)

if 'Priority Outreach Backlog' in sheets:
    res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Priority Outreach Backlog'!A1:J15").execute()
    print("\n--- TOP 15 FROM PRIORITY OUTREACH BACKLOG ---")
    for row in res.get('values', []):
        print(row)
else:
    print("\nNo Priority Outreach Backlog tab found. Checking Master Job Tracker...")
    res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N15").execute()
    for row in res.get('values', []):
        print(row)
