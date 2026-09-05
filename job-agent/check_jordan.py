import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A255:N255").execute()
row = res.get('values', [[]])[0]
headers = ['Country', 'Company', 'Email', 'Type', 'Status', 'Date Applied', 'Follow-up Date', 'Notes', 'Scan Status', 'Role', 'URL', 'Confidence', 'Recommended Action', 'Scan Date']
for h, val in zip(headers, row):
    print(f"{h}: {val}")
