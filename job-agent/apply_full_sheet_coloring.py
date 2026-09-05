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

# Get metadata to find all sheets and their IDs
meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
sheet_map = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}

print("Found tabs:", list(sheet_map.keys()))

# Configuration for tabs where full-row status coloring should be applied
# Format: (tab_name, status_column_letter, num_columns)
tab_configs = [
    ('Master Job Tracker', 'E', 14),
    ('Priority Outreach Backlog', 'H', 10),
    ('Agencies Aug 2026', 'F', 10),
    ('YC Startups Aug 2026', 'F', 10),
    ('IT Services Aug 2026', 'F', 10),
    ('Sent By Me', 'D', 11),
    ('Social Leads Jul 2026', 'G', 10),
]

requests = []

for tab_name, status_col, num_cols in tab_configs:
    if tab_name not in sheet_map:
        print(f"Skipping {tab_name} (not found in workbook)")
        continue
    
    sid = sheet_map[tab_name]
    print(f"Configuring conditional formatting for '{tab_name}' (sheetId: {sid}, Status Col: ${status_col}2, Width: {num_cols} cols)...")
    
    # Range covering all rows from row 2 to 2000
    target_range = {
        'sheetId': sid,
        'startRowIndex': 1,
        'endRowIndex': 2000,
        'startColumnIndex': 0,
        'endColumnIndex': num_cols
    }
    
    # 1. Reply / Interview / Conversation -> Emerald Green
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [target_range],
                'booleanRule': {
                    'condition': {
                        'type': 'CUSTOM_FORMULA',
                        'values': [{'userEnteredValue': f'=REGEXMATCH(${status_col}2, "(?i)reply|conversation|interview|accepted")'}]
                    },
                    'format': {
                        'backgroundColor': {'red': 0.85, 'green': 0.95, 'blue': 0.88}, # Soft Emerald Green #D9F2E0
                        'textFormat': {'bold': False, 'foregroundColor': {'red': 0.05, 'green': 0.35, 'blue': 0.15}}
                    }
                }
            },
            'index': 0
        }
    })
    
    # 2. Applied / Sent -> Soft Ice Blue
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [target_range],
                'booleanRule': {
                    'condition': {
                        'type': 'CUSTOM_FORMULA',
                        'values': [{'userEnteredValue': f'=REGEXMATCH(${status_col}2, "(?i)^applied|sent")'}]
                    },
                    'format': {
                        'backgroundColor': {'red': 0.91, 'green': 0.94, 'blue': 0.99}, # Soft Blue #E8F0FC
                        'textFormat': {'bold': False, 'foregroundColor': {'red': 0.10, 'green': 0.20, 'blue': 0.40}}
                    }
                }
            },
            'index': 1
        }
    })
    
    # 3. Undeliverable / Bounced / Scam -> Soft Rose / Coral
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [target_range],
                'booleanRule': {
                    'condition': {
                        'type': 'CUSTOM_FORMULA',
                        'values': [{'userEnteredValue': f'=REGEXMATCH(${status_col}2, "(?i)undeliverable|bounced|bad email|scam")'}]
                    },
                    'format': {
                        'backgroundColor': {'red': 0.98, 'green': 0.88, 'blue': 0.87}, # Soft Coral #FAECEB
                        'textFormat': {'bold': False, 'foregroundColor': {'red': 0.50, 'green': 0.10, 'blue': 0.10}}
                    }
                }
            },
            'index': 2
        }
    })
    
    # 4. Rejected / Do Not Pursue / Skip -> Muted Slate Gray
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [target_range],
                'booleanRule': {
                    'condition': {
                        'type': 'CUSTOM_FORMULA',
                        'values': [{'userEnteredValue': f'=REGEXMATCH(${status_col}2, "(?i)reject|do not pursue|skip|hold")'}]
                    },
                    'format': {
                        'backgroundColor': {'red': 0.93, 'green': 0.93, 'blue': 0.93}, # Muted Gray #EEEEEE
                        'textFormat': {'bold': False, 'foregroundColor': {'red': 0.40, 'green': 0.40, 'blue': 0.40}}
                    }
                }
            },
            'index': 3
        }
    })
    
    # 5. To Contact -> Clean White
    requests.append({
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [target_range],
                'booleanRule': {
                    'condition': {
                        'type': 'CUSTOM_FORMULA',
                        'values': [{'userEnteredValue': f'=REGEXMATCH(${status_col}2, "(?i)to contact|apply")'}]
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

print(f"Total conditional formatting rules to apply: {len(requests)}")

# Execute batch
res = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': requests}).execute()
print("SUCCESS: Full-row status conditional formatting rules successfully applied across all active tracker tabs!")
