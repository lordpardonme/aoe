import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
sheets = [s['properties']['title'] for s in meta['sheets']]
print(f"Spreadsheet tabs: {sheets}\n")

# Let's inspect the headers and sample rows of Direct Employers, Agencies, LinkedIn Search, Phone WhatsApp, Social Leads Jul 2026
for tab in ['Direct Employers', 'Agencies', 'LinkedIn Search', 'Phone WhatsApp', 'Social Leads Jul 2026']:
    if tab in sheets:
        res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=f"'{tab}'!A1:Z5").execute()
        rows = res.get('values', [])
        print(f"=== TAB: {tab} ===")
        for r in rows:
            print(r)
        print()
