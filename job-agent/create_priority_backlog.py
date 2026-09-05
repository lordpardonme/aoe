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
sheet_title = 'Priority Outreach Backlog'

print(f"Creating / Resetting fresh queue tab: '{sheet_title}'...")

# 1. Check if sheet exists; create or clear
meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
existing_sheets = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}

if sheet_title in existing_sheets:
    sid = existing_sheets[sheet_title]
    service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=f"'{sheet_title}'!A1:Z2000").execute()
    print("Cleared existing tab.")
else:
    req = [{'addSheet': {'properties': {'title': sheet_title}}}]
    res_add = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': req}).execute()
    sid = res_add['replies'][0]['addSheet']['properties']['sheetId']
    print(f"Created new tab with sheetId: {sid}")

# 2. Extract all 'To Contact' rows from Master Job Tracker
res_master = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
master_data = res_master.get('values', [])[1:]

backlog_rows = []
seen_emails = set()

# Headers: ['Priority', 'Source Queue', 'Country / Region', 'Company / Target', 'Email Address', 'Type / Domain', 'Contact Person / Role', 'Status', 'Recommended Pitch', 'Notes']
priority_counter = 1

# Master Job Tracker To Contact rows
for r in master_data:
    row = r + [''] * (14 - len(r))
    country, company, email, l_type, status, dt_applied, dt_follow, notes, scan_status, role, url, conf, rec_act, dt_scan = row
    if status.strip().lower() == 'to contact' and email.strip():
        clean_email = email.strip().lower()
        if clean_email not in seen_emails:
            seen_emails.add(clean_email)
            backlog_rows.append([
                priority_counter,
                'Master Tracker Backlog',
                country or 'India',
                company,
                email,
                l_type or 'Direct Employer',
                role or 'Product / UI-UX Designer',
                'To Contact',
                'Tailored Pitch (Product Designer CV)',
                notes
            ])
            priority_counter += 1

# Agencies Aug 2026 To Contact rows
res_agencies = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Agencies Aug 2026'!A1:J").execute()
agency_data = res_agencies.get('values', [])[1:]
for r in agency_data:
    row = r + [''] * (10 - len(r))
    company, category, email, hiring_mgr, linkedin, status, dt_add, dt_cont, msg_id, notes = row
    if status.strip().lower() == 'to contact' and email.strip():
        clean_email = email.strip().lower()
        if clean_email not in seen_emails:
            seen_emails.add(clean_email)
            backlog_rows.append([
                priority_counter,
                'Agencies Aug 2026',
                'India / Global',
                company,
                email,
                category or 'Staffing Agency',
                hiring_mgr or 'Head of Recruitment',
                'To Contact',
                'Agency Representation (Master Product Designer CV)',
                notes
            ])
            priority_counter += 1

# YC Startups Aug 2026 To Contact rows
res_yc = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'YC Startups Aug 2026'!A1:J").execute()
yc_data = res_yc.get('values', [])[1:]
for r in yc_data:
    row = r + [''] * (10 - len(r))
    company, category, email, hiring_mgr, linkedin, status, dt_add, dt_cont, msg_id, notes = row
    if status.strip().lower() == 'to contact' and email.strip():
        clean_email = email.strip().lower()
        if clean_email not in seen_emails:
            seen_emails.add(clean_email)
            backlog_rows.append([
                priority_counter,
                'YC Startups Aug 2026',
                'US / Global (Remote)',
                company,
                email,
                'YC Tech Startup',
                hiring_mgr or 'Founders Team',
                'To Contact',
                '0-to-1 Product Design & Velocity Pitch',
                notes
            ])
            priority_counter += 1

# IT Services Aug 2026 To Contact rows
res_it = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'IT Services Aug 2026'!A1:J").execute()
it_data = res_it.get('values', [])[1:]
for r in it_data:
    row = r + [''] * (10 - len(r))
    company, category, email, hiring_mgr, linkedin, status, dt_add, dt_cont, msg_id, notes = row
    if status.strip().lower() == 'to contact' and email.strip():
        clean_email = email.strip().lower()
        if clean_email not in seen_emails:
            seen_emails.add(clean_email)
            backlog_rows.append([
                priority_counter,
                'IT Services Aug 2026',
                'India',
                company,
                email,
                'IT Services & Software',
                hiring_mgr or 'Head of Talent Acquisition',
                'To Contact',
                'Enterprise UI/UX & Design Systems Pitch',
                notes
            ])
            priority_counter += 1

print(f"Total unique consolidated backlog rows: {len(backlog_rows)}")

headers = ['# Priority', 'Source Queue', 'Country / Region', 'Company / Target', 'Email Address', 'Type / Category', 'Contact Person / Role', 'Status', 'Recommended Pitch', 'Notes']
all_values = [headers] + backlog_rows

# 3. Write data to Priority Outreach Backlog sheet
service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range=f"'{sheet_title}'!A1",
    valueInputOption='RAW',
    body={'values': all_values}
).execute()

print(f"Wrote {len(all_values)} rows to '{sheet_title}'.")

# 4. Apply formatting, filters, and freeze row
style_requests = [
    # Freeze row 1
    {
        'updateSheetProperties': {
            'properties': {
                'sheetId': sid,
                'gridProperties': {'frozenRowCount': 1}
            },
            'fields': 'gridProperties.frozenRowCount'
        }
    },
    # Header format: Navy background, bold white text
    {
        'repeatCell': {
            'range': {
                'sheetId': sid,
                'startRowIndex': 0,
                'endRowIndex': 1,
                'startColumnIndex': 0,
                'endColumnIndex': 10
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
                    'verticalAlignment': 'MIDDLE'
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)'
        }
    },
    # Data row formatting: Segoe UI, 10pt
    {
        'repeatCell': {
            'range': {
                'sheetId': sid,
                'startRowIndex': 1,
                'endRowIndex': len(all_values),
                'startColumnIndex': 0,
                'endColumnIndex': 10
            },
            'cell': {
                'userEnteredFormat': {
                    'textFormat': {
                        'fontSize': 10,
                        'fontFamily': 'Segoe UI'
                    },
                    'verticalAlignment': 'MIDDLE'
                }
            },
            'fields': 'userEnteredFormat(textFormat,verticalAlignment)'
        }
    },
    # Center align: Priority (#), Source Queue, Country, Type, Status
    {
        'repeatCell': {
            'range': {
                'sheetId': sid,
                'startRowIndex': 1,
                'endRowIndex': len(all_values),
                'startColumnIndex': 0,
                'endColumnIndex': 3
            },
            'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER'}},
            'fields': 'userEnteredFormat.horizontalAlignment'
        }
    },
    {
        'repeatCell': {
            'range': {
                'sheetId': sid,
                'startRowIndex': 1,
                'endRowIndex': len(all_values),
                'startColumnIndex': 5,
                'endColumnIndex': 6
            },
            'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER'}},
            'fields': 'userEnteredFormat.horizontalAlignment'
        }
    },
    {
        'repeatCell': {
            'range': {
                'sheetId': sid,
                'startRowIndex': 1,
                'endRowIndex': len(all_values),
                'startColumnIndex': 7,
                'endColumnIndex': 8
            },
            'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER'}},
            'fields': 'userEnteredFormat.horizontalAlignment'
        }
    },
    # Set basic filter across all columns
    {
        'setBasicFilter': {
            'filter': {
                'range': {
                    'sheetId': sid,
                    'startRowIndex': 0,
                    'endRowIndex': len(all_values),
                    'startColumnIndex': 0,
                    'endColumnIndex': 10
                }
            }
        }
    },
    # Auto-resize columns
    {
        'autoResizeDimensions': {
            'dimensions': {
                'sheetId': sid,
                'dimension': 'COLUMNS',
                'startIndex': 0,
                'endIndex': 10
            }
        }
    }
]

service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': style_requests}).execute()
print("Formatting and filters successfully applied to fresh queue!")
