import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

# Get sheet metadata to find Agencies Aug 2026 sheetId
sheet_meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
sheet_id = None
for s in sheet_meta['sheets']:
    if s['properties']['title'] == 'Agencies Aug 2026':
        sheet_id = s['properties']['sheetId']
        break

print(f"Agencies Aug 2026 sheetId: {sheet_id}")

if sheet_id is not None:
    # Add conditional formatting rules for Applied (Soft Blue), Reply (Green), Bounced (Red), Rejected (Gray)
    rules = [
        # Applied (Soft Lavender-Blue)
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": sheet_id, "startRowIndex": 1, "endRowIndex": 50, "startColumnIndex": 0, "endColumnIndex": 10}],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [{"userEnteredValue": '=REGEXMATCH(LOWER($F2), "^applied")'}]
                        },
                        "format": {
                            "backgroundColor": {"red": 0.9098, "green": 0.9333, "blue": 0.9843},
                            "textFormat": {"foregroundColor": {"red": 0.098, "green": 0.200, "blue": 0.400}, "bold": False}
                        }
                    }
                },
                "index": 0
            }
        },
        # Reply (Green)
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": sheet_id, "startRowIndex": 1, "endRowIndex": 50, "startColumnIndex": 0, "endColumnIndex": 10}],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [{"userEnteredValue": '=REGEXMATCH(LOWER($F2), "reply|interview")'}]
                        },
                        "format": {
                            "backgroundColor": {"red": 0.847, "green": 0.949, "blue": 0.878},
                            "textFormat": {"foregroundColor": {"red": 0.047, "green": 0.349, "blue": 0.149}, "bold": True}
                        }
                    }
                },
                "index": 1
            }
        },
        # Undeliverable / Bounced (Red)
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": sheet_id, "startRowIndex": 1, "endRowIndex": 50, "startColumnIndex": 0, "endColumnIndex": 10}],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [{"userEnteredValue": '=REGEXMATCH(LOWER($F2), "undeliverable|bounce")'}]
                        },
                        "format": {
                            "backgroundColor": {"red": 0.976, "green": 0.878, "blue": 0.867},
                            "textFormat": {"foregroundColor": {"red": 0.498, "green": 0.098, "blue": 0.098}, "bold": False}
                        }
                    }
                },
                "index": 2
            }
        }
    ]
    
    body = {"requests": rules}
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
    print("Conditional formatting added to 'Agencies Aug 2026' tab successfully!")
