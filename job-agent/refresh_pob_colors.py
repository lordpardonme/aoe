import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

# Priority Outreach Backlog sheetId is 2019939738
pob_sheet_id = 2019939738

# Define standard clean conditional formatting rules for Priority Outreach Backlog
# Range A2:J300
rules = [
    # 1. Replies / Interviews (Green)
    {
        'rule': {
            'ranges': [{'sheetId': pob_sheet_id, 'startRowIndex': 1, 'endRowIndex': 350, 'startColumnIndex': 0, 'endColumnIndex': 10}],
            'booleanRule': {
                'condition': {
                    'type': 'CUSTOM_FORMULA',
                    'values': [{'userEnteredValue': '=REGEXMATCH($H2, "(?i)reply|conversation|interview|accepted")'}]
                },
                'format': {
                    'backgroundColor': {'red': 0.847, 'green': 0.949, 'blue': 0.878},
                    'textFormat': {'foregroundColor': {'red': 0.047, 'green': 0.349, 'blue': 0.149}, 'bold': False}
                }
            }
        },
        'index': 0
    },
    # 2. Bounced / Undeliverable (Red)
    {
        'rule': {
            'ranges': [{'sheetId': pob_sheet_id, 'startRowIndex': 1, 'endRowIndex': 350, 'startColumnIndex': 0, 'endColumnIndex': 10}],
            'booleanRule': {
                'condition': {
                    'type': 'CUSTOM_FORMULA',
                    'values': [{'userEnteredValue': '=REGEXMATCH($H2, "(?i)undeliverable|bounced|bad email|scam")'}]
                },
                'format': {
                    'backgroundColor': {'red': 0.976, 'green': 0.878, 'blue': 0.867},
                    'textFormat': {'foregroundColor': {'red': 0.498, 'green': 0.098, 'blue': 0.098}, 'bold': False}
                }
            }
        },
        'index': 1
    },
    # 3. Rejected / Do Not Pursue (Gray)
    {
        'rule': {
            'ranges': [{'sheetId': pob_sheet_id, 'startRowIndex': 1, 'endRowIndex': 350, 'startColumnIndex': 0, 'endColumnIndex': 10}],
            'booleanRule': {
                'condition': {
                    'type': 'CUSTOM_FORMULA',
                    'values': [{'userEnteredValue': '=REGEXMATCH($H2, "(?i)reject|do not pursue|skip|hold")'}]
                },
                'format': {
                    'backgroundColor': {'red': 0.929, 'green': 0.929, 'blue': 0.929},
                    'textFormat': {'foregroundColor': {'red': 0.4, 'green': 0.4, 'blue': 0.4}, 'bold': False}
                }
            }
        },
        'index': 2
    },
    # 4. Applied / Sent (Soft Lavender-Blue)
    {
        'rule': {
            'ranges': [{'sheetId': pob_sheet_id, 'startRowIndex': 1, 'endRowIndex': 350, 'startColumnIndex': 0, 'endColumnIndex': 10}],
            'booleanRule': {
                'condition': {
                    'type': 'CUSTOM_FORMULA',
                    'values': [{'userEnteredValue': '=REGEXMATCH($H2, "(?i)^applied|sent|form required")'}]
                },
                'format': {
                    'backgroundColor': {'red': 0.910, 'green': 0.937, 'blue': 0.988},
                    'textFormat': {'foregroundColor': {'red': 0.098, 'green': 0.200, 'blue': 0.400}, 'bold': False}
                }
            }
        },
        'index': 3
    },
    # 5. To Contact (White)
    {
        'rule': {
            'ranges': [{'sheetId': pob_sheet_id, 'startRowIndex': 1, 'endRowIndex': 350, 'startColumnIndex': 0, 'endColumnIndex': 10}],
            'booleanRule': {
                'condition': {
                    'type': 'CUSTOM_FORMULA',
                    'values': [{'userEnteredValue': '=REGEXMATCH($H2, "(?i)to contact|apply")'}]
                },
                'format': {
                    'backgroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0},
                    'textFormat': {'foregroundColor': {'red': 0.149, 'green': 0.149, 'blue': 0.149}, 'bold': False}
                }
            }
        },
        'index': 4
    }
]

# Get current rules to clear/replace
meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id, fields="sheets(properties,conditionalFormats)").execute()
curr_rules = []
for s in meta.get('sheets', []):
    if s['properties']['sheetId'] == pob_sheet_id:
        curr_rules = s.get('conditionalFormats', [])
        break

requests = []
# Delete existing conditional format rules in reverse index order
for i in range(len(curr_rules) - 1, -1, -1):
    requests.append({
        'deleteConditionalFormatRule': {
            'sheetId': pob_sheet_id,
            'index': i
        }
    })

# Add new rules
for r in rules:
    requests.append({
        'addConditionalFormatRule': r
    })

body = {'requests': requests}
service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
print("Priority Outreach Backlog conditional formatting rules 100% updated and refreshed across all rows A2:J350!")
