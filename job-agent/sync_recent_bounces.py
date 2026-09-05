import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

today_str = "2026-08-25"

updates = [
    {
        'row': 106,
        'company': 'Irwin & Dow',
        'status': 'Applied - Rejected',
        'note': 'Replied 2026-08-25: No sector expertise for design; recommended Hays & Michael Page. Gmail ID: 1a0386413cadf29a'
    },
    {
        'row': 145,
        'company': 'Blinkist',
        'status': 'Undeliverable / Bounced',
        'note': 'Auto-reply 2026-08-25: jobs@blinkist.com no longer active; portal only. Gmail ID: 1a038b6270d54ba1'
    },
    {
        'row': 153,
        'company': 'Choco',
        'status': 'Undeliverable / Bounced',
        'note': 'Bounced 2026-08-25: jobs@choco.com address not found. Gmail ID: 1a038b691123e15d'
    },
    {
        'row': 270,
        'company': 'Taxfix',
        'status': 'Undeliverable / Bounced',
        'note': 'Bounced 2026-08-25: talentacquistion@taxfix.de address not found. Gmail ID: 1a038b6e32860e0c'
    },
    {
        'row': 182,
        'company': 'FINN',
        'status': 'Undeliverable / Bounced',
        'note': 'Bounced 2026-08-25: jobs@finn.com address not found. Gmail ID: 1a038b709b466295'
    }
]

for u in updates:
    r_idx = u['row']
    update_range = f"'Master Job Tracker'!E{r_idx}:H{r_idx}"
    body = {'values': [[u['status'], today_str, '', u['note']]]}
    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body=body).execute()
    print(f"Updated Master Row {r_idx} ({u['company']}) -> {u['status']}")

print("\nRECONCILIATION COMPLETED!")
