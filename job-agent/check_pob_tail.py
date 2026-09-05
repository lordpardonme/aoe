import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Priority Outreach Backlog'!A100:J300").execute()
rows = res.get('values', [])

print(f"Total rows starting from row 100: {len(rows)}")
for idx, r in enumerate(rows, start=100):
    r_pad = r + [''] * (10 - len(r))
    p_num, source, country, company, email, cat, contact_role, status, pitch, notes = r_pad
    print(f"Row {idx:3d}: {company:30s} | {status:20s} | {email}")
