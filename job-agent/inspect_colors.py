import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

# Get sheet metadata including conditional format rules and sheet IDs
meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id, fields="sheets(properties,conditionalFormats)").execute()

for s in meta.get('sheets', []):
    title = s['properties']['title']
    sheet_id = s['properties']['sheetId']
    formats = s.get('conditionalFormats', [])
    print(f"Sheet '{title}' (ID: {sheet_id}): {len(formats)} conditional format rules")
    for f in formats:
        print(f)

# Also let's inspect the actual background colors in Master Job Tracker
res = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    ranges=["'Master Job Tracker'!E2:E10"],
    fields="sheets(data(rowData(values(userEnteredFormat,effectiveFormat))))"
).execute()

print("\n--- SAMPLE FORMATTING IN MASTER JOB TRACKER ---")
for r in res.get('sheets', [])[0]['data'][0].get('rowData', []):
    for v in r.get('values', []):
        print(v.get('effectiveFormat', {}).get('backgroundColor'))
