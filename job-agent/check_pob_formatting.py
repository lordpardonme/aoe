import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

res = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    ranges=["'Priority Outreach Backlog'!A1:J10"],
    fields="sheets(data(rowData(values(userEnteredFormat,effectiveFormat,formattedValue))))"
).execute()

rows = res.get('sheets', [])[0]['data'][0].get('rowData', [])
for idx, r in enumerate(rows, start=1):
    vals = r.get('values', [])
    txts = [v.get('formattedValue', '') for v in vals]
    bg_h = vals[7].get('userEnteredFormat', {}).get('backgroundColor') if len(vals) > 7 else None
    eff_h = vals[7].get('effectiveFormat', {}).get('backgroundColor') if len(vals) > 7 else None
    print(f"Row {idx:2d} | Status: {txts[7] if len(txts)>7 else ''} | userEnteredBG: {bg_h} | effectiveBG: {eff_h}")
