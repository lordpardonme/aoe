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
found = False
for s in meta['sheets']:
    t = s['properties']['title']
    res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=f"'{t}'!A1:Z500").execute()
    for row_idx, r in enumerate(res.get('values', []), 1):
        for col_idx, cell in enumerate(r, 1):
            if '306' in str(cell):
                print(f"Found '306' in Tab '{t}' at Row {row_idx}, Col {col_idx}: {cell}")
                found = True

if not found:
    print("No cell containing '306' was found anywhere in the entire spreadsheet.")
