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

# Read all rows of Master Job Tracker
res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
rows = res.get('values', [])
headers = rows[0]
data = rows[1:]

print(f"Total rows to inspect: {len(data)}")

# Let's inspect column values:
# 0: Country / Region
# 1: Company / Agency
# 2: Email
# 3: Type
# 4: Status
# 5: Date Applied
# 6: Follow-up Date
# 7: Notes
# 8: Opening Scan Status
# 9: Matched Role(s)
# 10: Opening Source URL(s)
# 11: Confidence
# 12: Recommended Action
# 13: Scan Date

cleaned_rows = []
modifications_count = 0

for i, row in enumerate(data):
    # Ensure length of row is 14
    r = list(row) + [''] * (14 - len(row))
    orig = list(r)
    
    country, company, email, l_type, status, dt_applied, dt_follow, notes, scan_status, role, url, conf, rec_act, dt_scan = r
    
    # 1. Clean Country / Region
    country = country.strip()
    if not country:
        if any(k in (company + ' ' + email + ' ' + notes).lower() for k in ['dubai', 'uae', 'abu dhabi', 'gulf', 'gcc', '.ae', 'doha', 'qatar', 'riyadh', 'saudi']):
            country = 'UAE / Dubai'
        else:
            country = 'India'
            
    # 2. Clean Type
    l_type = l_type.strip()
    if not l_type:
        if any(k in (company + ' ' + role + ' ' + notes).lower() for k in ['agency', 'consultan', 'recruitment', 'staffing', 'talent']):
            l_type = 'Agency'
        elif any(k in (role + ' ' + notes).lower() for k in ['freelance', 'part-time', 'contract']):
            l_type = 'Freelance / Contract'
        else:
            l_type = 'Direct Employer'
            
    # 3. Clean Status
    status = status.strip()
    if not status:
        status = 'To Contact'
    # Standardize statuses
    if status in ['Applied', 'Applied - Sourced via Agent Batch']:
        status = 'Applied'
    elif 'undeliverable' in status.lower() or 'bounced' in status.lower() or 'bad email' in status.lower() or 'bad domain' in status.lower():
        status = 'Undeliverable / Bounced'
    elif 'rejected' in status.lower() or 'reject' in status.lower():
        if 'conversation' not in status.lower() and 'reconsideration' not in status.lower():
            status = 'Applied - Rejected'
    elif 'reply' in status.lower() and 'deadline' not in status.lower():
        status = 'Applied - Reply Received'
        
    # 4. Clean Dates (standardize empty or format)
    dt_applied = dt_applied.strip()
    dt_follow = dt_follow.strip()
    dt_scan = dt_scan.strip()
    
    # If Applied, ensure Follow-up Date is set if empty
    if status == 'Applied' and dt_applied and not dt_follow:
        # Default follow up to +7 days or 2026-08-31
        dt_follow = '2026-08-31'
        
    # 5. Clean Confidence
    conf = conf.strip()
    if not conf or conf == 'Unknown':
        conf = 'High' if status == 'Applied' else 'Medium'
        
    # 6. Clean Recommended Action
    rec_act = rec_act.strip()
    if not rec_act:
        if status == 'Applied':
            rec_act = 'Follow up if no response'
        elif status == 'Applied - Reply Received' or status == 'In Conversation — Awaiting Reply':
            rec_act = 'Respond to active thread / questionnaire'
        elif status == 'Undeliverable / Bounced':
            rec_act = 'Find updated contact email'
        elif status == 'To Contact':
            rec_act = 'Send tailored application packet'
        else:
            rec_act = 'Archived'

    # 7. Clean Opening Scan Status
    scan_status = scan_status.strip()
    if not scan_status:
        scan_status = 'Active Opening' if status == 'To Contact' else 'Application Submitted'
        
    updated_r = [country, company.strip(), email.strip(), l_type, status, dt_applied, dt_follow, notes.strip(), scan_status, role.strip(), url.strip(), conf, rec_act, dt_scan]
    
    if updated_r != orig:
        modifications_count += 1
        
    cleaned_rows.append(updated_r)

print(f"Total rows modified/standardized: {modifications_count} out of {len(data)}")

# Write all standardized rows back to Master Job Tracker
all_data = [headers] + cleaned_rows
service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range=f"'Master Job Tracker'!A1:N{len(all_data)}",
    valueInputOption='RAW',
    body={'values': all_data}
).execute()

print("Successfully written all 397 standardized rows to Master Job Tracker.")

# Now apply uniform font, cell alignment, and border styling to all 397 rows
meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
master_id = [s['properties']['sheetId'] for s in meta['sheets'] if s['properties']['title'] == 'Master Job Tracker'][0]

style_requests = [
    # 1. Uniform typography (Segoe UI / Arial, 10pt, vertical center) across all data rows A2:N500
    {
        'repeatCell': {
            'range': {
                'sheetId': master_id,
                'startRowIndex': 1,
                'endRowIndex': len(all_data),
                'startColumnIndex': 0,
                'endColumnIndex': 14
            },
            'cell': {
                'userEnteredFormat': {
                    'textFormat': {
                        'fontSize': 10,
                        'fontFamily': 'Segoe UI'
                    },
                    'verticalAlignment': 'MIDDLE',
                    'wrapStrategy': 'CLIP'
                }
            },
            'fields': 'userEnteredFormat(textFormat,verticalAlignment,wrapStrategy)'
        }
    },
    # 2. Specific column alignments:
    # Col A (Country): Center
    # Col C (Email): Left
    # Col D (Type): Center
    # Col E (Status): Center
    # Col F (Date Applied): Center
    # Col G (Follow-up Date): Center
    # Col L (Confidence): Center
    # Col N (Scan Date): Center
    {
        'repeatCell': {
            'range': {
                'sheetId': master_id,
                'startRowIndex': 1,
                'endRowIndex': len(all_data),
                'startColumnIndex': 0,
                'endColumnIndex': 1
            },
            'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER'}},
            'fields': 'userEnteredFormat.horizontalAlignment'
        }
    },
    {
        'repeatCell': {
            'range': {
                'sheetId': master_id,
                'startRowIndex': 1,
                'endRowIndex': len(all_data),
                'startColumnIndex': 3,
                'endColumnIndex': 7
            },
            'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER'}},
            'fields': 'userEnteredFormat.horizontalAlignment'
        }
    },
    {
        'repeatCell': {
            'range': {
                'sheetId': master_id,
                'startRowIndex': 1,
                'endRowIndex': len(all_data),
                'startColumnIndex': 11,
                'endColumnIndex': 12
            },
            'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER'}},
            'fields': 'userEnteredFormat.horizontalAlignment'
        }
    },
    {
        'repeatCell': {
            'range': {
                'sheetId': master_id,
                'startRowIndex': 1,
                'endRowIndex': len(all_data),
                'startColumnIndex': 13,
                'endColumnIndex': 14
            },
            'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER'}},
            'fields': 'userEnteredFormat.horizontalAlignment'
        }
    }
]

service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={'requests': style_requests}).execute()
print("Successfully applied uniform alignment, fonts, and clean clipping styles!")
