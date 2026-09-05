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

# Get metadata to find sheetId
meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
sid = [s['properties']['sheetId'] for s in meta['sheets'] if s['properties']['title'] == sheet_title][0]

# 1. Extract all 197 'To Contact' rows from Master Job Tracker
res_master = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
master_data = res_master.get('values', [])[1:]

backlog_rows = []
priority_counter = 1

# Master Job Tracker To Contact rows (ALL 197)
for r in master_data:
    row = r + [''] * (14 - len(r))
    country, company, email, l_type, status, dt_applied, dt_follow, notes, scan_status, role, url, conf, rec_act, dt_scan = row
    if status.strip().lower() == 'to contact':
        # Classify recommended action
        clean_email = email.strip()
        if not clean_email or 'find' in clean_email.lower() or 'linkedin' in clean_email.lower():
            recommended_pitch = 'Find Recruiter on LinkedIn / Portal Apply'
            email_display = clean_email if clean_email else '[Needs Recruiter Email]'
        else:
            recommended_pitch = 'Direct Email Outreach (Product Designer CV)'
            email_display = clean_email
            
        backlog_rows.append([
            priority_counter,
            'Master Tracker Backlog',
            country or 'India',
            company,
            email_display,
            l_type or 'Direct Employer',
            role or 'Product / UI-UX Designer',
            'To Contact',
            recommended_pitch,
            notes
        ])
        priority_counter += 1

print(f"Added all {len(backlog_rows)} Master Tracker To Contact rows.")

# 2. Add Agencies Aug 2026 (20 rows)
res_agencies = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Agencies Aug 2026'!A1:J").execute()
agency_data = res_agencies.get('values', [])[1:]
for r in agency_data:
    row = r + [''] * (10 - len(r))
    company, category, email, hiring_mgr, linkedin, status, dt_add, dt_cont, msg_id, notes = row
    if status.strip().lower() == 'to contact':
        backlog_rows.append([
            priority_counter,
            'Agencies Aug 2026',
            'India / Global',
            company,
            email.strip(),
            category or 'Staffing Agency',
            hiring_mgr or 'Head of Recruitment',
            'To Contact',
            'Agency Talent Representation (Master CV)',
            notes
        ])
        priority_counter += 1

# 3. Add YC Startups Aug 2026 (20 rows)
res_yc = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'YC Startups Aug 2026'!A1:J").execute()
yc_data = res_yc.get('values', [])[1:]
for r in yc_data:
    row = r + [''] * (10 - len(r))
    company, category, email, hiring_mgr, linkedin, status, dt_add, dt_cont, msg_id, notes = row
    if status.strip().lower() == 'to contact':
        backlog_rows.append([
            priority_counter,
            'YC Startups Aug 2026',
            'US / Global (Remote)',
            company,
            email.strip(),
            'YC Tech Startup',
            hiring_mgr or 'Founders Team',
            'To Contact',
            '0-to-1 Product Design & Velocity Pitch',
            notes
        ])
        priority_counter += 1

# 4. Add IT Services Aug 2026 (15 rows)
res_it = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'IT Services Aug 2026'!A1:J").execute()
it_data = res_it.get('values', [])[1:]
for r in it_data:
    row = r + [''] * (10 - len(r))
    company, category, email, hiring_mgr, linkedin, status, dt_add, dt_cont, msg_id, notes = row
    if status.strip().lower() == 'to contact':
        backlog_rows.append([
            priority_counter,
            'IT Services Aug 2026',
            'India',
            company,
            email.strip(),
            'IT Services & Software',
            hiring_mgr or 'Head of Talent Acquisition',
            'To Contact',
            'Enterprise UI/UX & Design Systems Pitch',
            notes
        ])
        priority_counter += 1

print(f"Total rows in Priority Outreach Backlog: {len(backlog_rows)}")

headers = ['# Priority', 'Source Queue', 'Country / Region', 'Company / Target', 'Email Address', 'Type / Category', 'Contact Person / Role', 'Status', 'Recommended Pitch', 'Notes']
all_values = [headers] + backlog_rows

# Clear and write all 253 rows
service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=f"'{sheet_title}'!A1:Z2000").execute()
service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range=f"'{sheet_title}'!A1",
    valueInputOption='RAW',
    body={'values': all_values}
).execute()

print(f"Successfully updated Priority Outreach Backlog with all {len(backlog_rows)} records.")
