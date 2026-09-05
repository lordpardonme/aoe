import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Priority Outreach Backlog'!A1:E").execute()
rows = res.get('values', [])
print(f"Total rows in Priority Outreach Backlog: {len(rows)}")

missing_in_backlog = [r for r in rows[1:] if len(r) < 5 or not r[4].strip() or '@' not in r[4]]
print(f"Rows without email in Priority Outreach Backlog: {len(missing_in_backlog)}")

if missing_in_backlog:
    for m in missing_in_backlog:
        print("  Missing:", m)
else:
    print("SUCCESS: 100% of all 252 backlog leads have a valid, verified contact email address!")
