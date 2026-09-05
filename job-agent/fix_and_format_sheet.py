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

print("=== 1. UPDATING MASTER JOB TRACKER DISCREPANCIES & STATUSES ===")

# Target cell updates
updates = [
    # Row 104: byPeople Technologies
    {'range': "'Master Job Tracker'!E104", 'values': [['Applied']]},
    {'range': "'Master Job Tracker'!F104", 'values': [['2026-05-24']]},
    {'range': "'Master Job Tracker'!H104", 'values': [['Application for UX Designer sent via Gmail (ID: 19e5b0731165b973)']]},

    # Row 105: Derby Group
    {'range': "'Master Job Tracker'!E105", 'values': [['Applied']]},
    {'range': "'Master Job Tracker'!F105", 'values': [['2026-06-02']]},
    {'range': "'Master Job Tracker'!G105", 'values': [['2026-07-01']]},
    {'range': "'Master Job Tracker'!H105", 'values': [['Application sent 2026-06-02 + follow-up sent 2026-07-01 (Gmail IDs: 19e89e85944d0089, 19f1de3801efaf52)']]},

    # Row 106: iKonsult Recruitment Solutions
    {'range': "'Master Job Tracker'!E106", 'values': [['Applied']]},
    {'range': "'Master Job Tracker'!F106", 'values': [['2026-06-23']]},
    {'range': "'Master Job Tracker'!H106", 'values': [['Application sent via Gmail (ID: 19ef699f206bd016)']]},

    # Row 107: Inspire Selection
    {'range': "'Master Job Tracker'!E107", 'values': [['Applied']]},
    {'range': "'Master Job Tracker'!F107", 'values': [['2026-06-12']]},
    {'range': "'Master Job Tracker'!H107", 'values': [['Application sent via Gmail (ID: 19ebcb58036e1ca4)']]},

    # Row 234: Onething Design
    {'range': "'Master Job Tracker'!E234", 'values': [['Applied']]},
    {'range': "'Master Job Tracker'!F234", 'values': [['2026-08-18']]},
    {'range': "'Master Job Tracker'!H234", 'values': [['Application sent 2026-07-04 + updated sent 2026-08-18 (Gmail IDs: 19f2ea16a25cf8f1, 1a013dfbfb0d4248)']]},

    # Row 275: Muhammed Mujitaba
    {'range': "'Master Job Tracker'!E275", 'values': [['In Conversation — Awaiting Reply']]},
    {'range': "'Master Job Tracker'!F275", 'values': [['2026-05-24']]},
    {'range': "'Master Job Tracker'!H275", 'values': [['Active thread with 7 back-and-forth messages (Gmail ID: 19eebaf10f3eda61)']]},

    # Row 367: The Minimalist
    {'range': "'Master Job Tracker'!E367", 'values': [['Applied - Reply Received']]},
    {'range': "'Master Job Tracker'!H367", 'values': [['Application sent 2026-08-24. Inbound response received from careers@theminimalist.in 2026-08-24.']]},

    # Row 369: Loudlabs
    {'range': "'Master Job Tracker'!E369", 'values': [['Undeliverable / Bounced']]},
    {'range': "'Master Job Tracker'!H369", 'values': [['careers@loudlabs.co.in mailbox delivery failure / full']]},

    # Row 394: Reach Group (Abu Dhabi)
    {'range': "'Master Job Tracker'!E394", 'values': [['Undeliverable / Bounced']]},
    {'range': "'Master Job Tracker'!H394", 'values': [['shaik.wahab@reachgroup.ae 550 User unknown / address not found']]},
]

for upd in updates:
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=upd['range'],
        valueInputOption='RAW',
        body={'values': upd['values']}
    ).execute()

print(f"Applied {len(updates)} cell updates to Master Job Tracker.")

print("\n=== 2. APPLYING BEAUTIFUL FORMATTING ACROSS ALL TABS ===")

# Fetch spreadsheet metadata to get sheet IDs
meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
sheet_map = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}

requests = []

# Format header for all sheets
for title, sid in sheet_map.items():
    if title == 'Dashboard':
        continue
    
    # 1. Freeze top row
    requests.append({
        'updateSheetProperties': {
            'properties': {
                'sheetId': sid,
                'gridProperties': {
                    'frozenRowCount': 1
                }
            },
            'fields': 'gridProperties.frozenRowCount'
        }
    })
    
    # 2. Header Style (Deep Slate Blue background, White Bold text)
    requests.append({
        'repeatCell': {
            'range': {
                'sheetId': sid,
                'startRowIndex': 0,
                'endRowIndex': 1,
                'startColumnIndex': 0,
                'endColumnIndex': 20
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': {'red': 0.12, 'green': 0.18, 'blue': 0.26},
                    'textFormat': {
                        'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0},
                        'bold': True,
                        'fontSize': 10
                    },
                    'horizontalAlignment': 'CENTER',
                    'verticalAlignment': 'MIDDLE',
                    'wrapStrategy': 'WRAP'
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)'
        }
    })
    
    # 3. Auto-resize columns for clean viewing
    requests.append({
        'autoResizeDimensions': {
            'dimensions': {
                'sheetId': sid,
                'dimension': 'COLUMNS',
                'startIndex': 0,
                'endIndex': 15
            }
        }
    })

# Format Dashboard specifically
if 'Dashboard' in sheet_map:
    dash_id = sheet_map['Dashboard']
    
    # Main Dashboard Title formatting (Row 1)
    requests.append({
        'repeatCell': {
            'range': {
                'sheetId': dash_id,
                'startRowIndex': 0,
                'endRowIndex': 1,
                'startColumnIndex': 0,
                'endColumnIndex': 3
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': {'red': 0.08, 'green': 0.12, 'blue': 0.20},
                    'textFormat': {
                        'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0},
                        'bold': True,
                        'fontSize': 14
                    },
                    'horizontalAlignment': 'LEFT',
                    'verticalAlignment': 'MIDDLE'
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)'
        }
    })
    
    # Section Header rows on Dashboard: Row 3 (idx 2), Row 12 (idx 11), Row 17 (idx 16), Row 23 (idx 22)
    section_rows = [2, 11, 16, 22]
    for sr in section_rows:
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': dash_id,
                    'startRowIndex': sr,
                    'endRowIndex': sr + 1,
                    'startColumnIndex': 0,
                    'endColumnIndex': 3
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {'red': 0.20, 'green': 0.28, 'blue': 0.38},
                        'textFormat': {
                            'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0},
                            'bold': True,
                            'fontSize': 11
                        }
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        })

    # Auto resize Dashboard columns
    requests.append({
        'autoResizeDimensions': {
            'dimensions': {
                'sheetId': dash_id,
                'dimension': 'COLUMNS',
                'startIndex': 0,
                'endIndex': 3
            }
        }
    })

# Execute all batch formatting requests
res_batch = service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={'requests': requests}
).execute()

print(f"Successfully applied {len(requests)} formatting & styling operations.")

# Re-run dashboard sync to ensure all formula counts are perfectly current
from sync_tracker import dashboard_data
service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='Dashboard!A1:C28',
    valueInputOption='USER_ENTERED',
    body={'values': dashboard_data}
).execute()

print("Google Sheet is completely fixed, reconciled, and formatted!")
