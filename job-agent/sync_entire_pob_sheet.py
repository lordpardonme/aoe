import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

today_str = "2026-08-25"

# 1. Fetch Master Job Tracker canonical data
res_m = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
m_rows = res_m.get('values', [])[1:]

applied_companies = {}
applied_emails = {}

for r in m_rows:
    r_padded = r + [''] * (14 - len(r))
    country, company, email, l_type, status, dt_applied, dt_follow, notes, scan_status, role, url, conf, rec_act, dt_scan = r_padded
    c_clean = company.strip().lower()
    e_clean = email.strip().lower()
    st_clean = status.strip().lower()
    
    if 'applied' in st_clean or 'rejected' in st_clean or 'form required' in st_clean or 'bounced' in st_clean:
        data = {'status': status.strip(), 'date': dt_applied.strip() or today_str, 'notes': notes.strip()}
        if c_clean:
            applied_companies[c_clean] = data
        if e_clean:
            applied_emails[e_clean] = data

# 2. Read ENTIRE Priority Outreach Backlog sheet
res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Priority Outreach Backlog'!A1:J1000").execute()
rows = res.get('values', [])
print(f"Total rows in Priority Outreach Backlog: {len(rows)}")

batch_data = []
updated_count = 0

for idx, r in enumerate(rows[1:], start=2):
    r_padded = r + [''] * (10 - len(r))
    p_num, source, country, company, email, cat, contact_role, status, pitch, notes = r_padded
    
    c_low = company.strip().lower()
    e_low = email.strip().lower()
    curr_st = status.strip()
    
    match_data = None
    if e_low and e_low in applied_emails:
        match_data = applied_emails[e_low]
    elif c_low and c_low in applied_companies:
        match_data = applied_companies[c_low]
    else:
        for ac, data in applied_companies.items():
            if len(ac) > 4 and (ac in c_low or c_low in ac):
                match_data = data
                break
    
    if match_data and curr_st.lower() != match_data['status'].lower():
        up_st = match_data['status']
        up_note = f"{notes.strip()} | Applied: {match_data['notes']}".strip(" | ")
        
        batch_data.append({
            'range': f"'Priority Outreach Backlog'!H{idx}",
            'values': [[up_st]]
        })
        batch_data.append({
            'range': f"'Priority Outreach Backlog'!J{idx}",
            'values': [[up_note]]
        })
        updated_count += 1
        print(f"Row {idx:3d}: {company:30s} -> Status: '{up_st}'")

if batch_data:
    print(f"\nExecuting batch update for {updated_count} rows across Priority Outreach Backlog...")
    body = {'valueInputOption': 'RAW', 'data': batch_data}
    service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
    print(f"Successfully updated all {updated_count} rows in Priority Outreach Backlog!")
else:
    print("Priority Outreach Backlog is 100% in sync.")
