import sys
import io
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

# Get metadata to find Master Job Tracker sheetId
meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
master_id = None
for s in meta['sheets']:
    if s['properties']['title'] == 'Master Job Tracker':
        master_id = s['properties']['sheetId']
        break

if master_id is None:
    print("Error: Master Job Tracker sheet not found!")
    sys.exit(1)

print(f"Master Job Tracker sheetId: {master_id}")

requests = []

# 1. Clear existing conditional formatting on Master Job Tracker if any
# We do this by clearing conditional format rules on the sheet
requests.append({
    'clearBasicFilter': {
        'sheetId': master_id
    }
})

# 2. Add Basic Filter across A1:N1000 on Master Job Tracker
# This adds dropdown filter arrows to every column including Location (A), Status (E), Date Applied (F), etc.
requests.append({
    'setBasicFilter': {
        'filter': {
            'range': {
                'sheetId': master_id,
                'startRowIndex': 0,
                'endRowIndex': 1000,
                'startColumnIndex': 0,
                'endColumnIndex': 14
            }
        }
    }
})

# 3. Add Conditional Formatting Rules for Row Colors based on Status ($E2)
# Range: A2:N1000

# Rule A: Reply Received / In Conversation / Interviewing -> Soft Emerald Green
requests.append({
    'addConditionalFormatRule': {
        'rule': {
            'ranges': [{
                'sheetId': master_id,
                'startRowIndex': 1,
                'endRowIndex': 1000,
                'startColumnIndex': 0,
                'endColumnIndex': 14
            }],
            'booleanRule': {
                'condition': {
                    'type': 'CUSTOM_FORMULA',
                    'values': [{'userEnteredValue': '=REGEXMATCH($E2, "(?i)reply|conversation|interview")'}]
                },
                'format': {
                    'backgroundColor': {'red': 0.85, 'green': 0.95, 'blue': 0.88}, # #D9F2E0
                    'textFormat': {'bold': False, 'foregroundColor': {'red': 0.05, 'green': 0.35, 'blue': 0.15}}
                }
            }
        },
        'index': 0
    }
})

# Rule B: Applied (Active) -> Soft Blue tint
requests.append({
    'addConditionalFormatRule': {
        'rule': {
            'ranges': [{
                'sheetId': master_id,
                'startRowIndex': 1,
                'endRowIndex': 1000,
                'startColumnIndex': 0,
                'endColumnIndex': 14
            }],
            'booleanRule': {
                'condition': {
                    'type': 'CUSTOM_FORMULA',
                    'values': [{'userEnteredValue': '=REGEXMATCH($E2, "(?i)^applied")'}]
                },
                'format': {
                    'backgroundColor': {'red': 0.91, 'green': 0.94, 'blue': 0.99}, # #E8F0FC
                    'textFormat': {'bold': False, 'foregroundColor': {'red': 0.10, 'green': 0.20, 'blue': 0.40}}
                }
            }
        },
        'index': 1
    }
})

# Rule C: Undeliverable / Bounced -> Soft Coral / Rose Red tint
requests.append({
    'addConditionalFormatRule': {
        'rule': {
            'ranges': [{
                'sheetId': master_id,
                'startRowIndex': 1,
                'endRowIndex': 1000,
                'startColumnIndex': 0,
                'endColumnIndex': 14
            }],
            'booleanRule': {
                'condition': {
                    'type': 'CUSTOM_FORMULA',
                    'values': [{'userEnteredValue': '=REGEXMATCH($E2, "(?i)undeliverable|bounced|bad email|bad domain")'}]
                },
                'format': {
                    'backgroundColor': {'red': 0.98, 'green': 0.88, 'blue': 0.87}, # #FAECEB
                    'textFormat': {'bold': False, 'foregroundColor': {'red': 0.50, 'green': 0.10, 'blue': 0.10}}
                }
            }
        },
        'index': 2
    }
})

# Rule D: Rejected -> Muted Gray / Neutral Slate tint
requests.append({
    'addConditionalFormatRule': {
        'rule': {
            'ranges': [{
                'sheetId': master_id,
                'startRowIndex': 1,
                'endRowIndex': 1000,
                'startColumnIndex': 0,
                'endColumnIndex': 14
            }],
            'booleanRule': {
                'condition': {
                    'type': 'CUSTOM_FORMULA',
                    'values': [{'userEnteredValue': '=REGEXMATCH($E2, "(?i)reject|do not pursue")'}]
                },
                'format': {
                    'backgroundColor': {'red': 0.93, 'green': 0.93, 'blue': 0.93}, # #EEEEEE
                    'textFormat': {'bold': False, 'foregroundColor': {'red': 0.40, 'green': 0.40, 'blue': 0.40}}
                }
            }
        },
        'index': 3
    }
})

# Rule E: To Contact -> Crisp Clean White / Very subtle tint
requests.append({
    'addConditionalFormatRule': {
        'rule': {
            'ranges': [{
                'sheetId': master_id,
                'startRowIndex': 1,
                'endRowIndex': 1000,
                'startColumnIndex': 0,
                'endColumnIndex': 14
            }],
            'booleanRule': {
                'condition': {
                    'type': 'CUSTOM_FORMULA',
                    'values': [{'userEnteredValue': '=REGEXMATCH($E2, "(?i)to contact")'}]
                },
                'format': {
                    'backgroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0},
                    'textFormat': {'bold': False, 'foregroundColor': {'red': 0.15, 'green': 0.15, 'blue': 0.15}}
                }
            }
        },
        'index': 4
    }
})

# Execute batchUpdate
try:
    res = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': requests}).execute()
    print("Successfully added Filter views and Color Conditional Formatting to Master Job Tracker!")
except Exception as e:
    # If clearBasicFilter failed because no filter was present, try without it
    print("Note on first batch:", e)
    clean_requests = [r for r in requests if 'clearBasicFilter' not in r]
    res = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': clean_requests}).execute()
    print("Successfully executed formatting rules without filter clear.")

print("Done.")
