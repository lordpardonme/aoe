import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

res_m = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
rows = res_m.get('values', [])[1:]

for idx, r in enumerate(rows, start=2):
    company = r[1].strip() if len(r) > 1 else ''
    if 'undutchables' in company.lower():
        update_range = f"'Master Job Tracker'!E{idx}:H{idx}"
        body = {'values': [['Applied - Rejected', '2026-08-25', '', 'Replied 2026-08-25: Requires existing valid Dutch work permit; cannot sponsor non-EU. Gmail ID: 1a0395a669988b7f']]}
        service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body=body).execute()
        print(f"Updated Undutchables at Master Row {idx} to Applied - Rejected.")
        break
