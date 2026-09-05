import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

print("Waiting 40 seconds to guarantee fresh Google Sheets 60s quota window...")
time.sleep(40)

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

today_str = "2026-08-25"
follow_up_str = "2026-09-01"

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
    
    if 'applied' in st_clean:
        data = {'status': status.strip(), 'date': dt_applied.strip() or today_str, 'notes': notes.strip()}
        if c_clean:
            applied_companies[c_clean] = data
        if e_clean:
            applied_emails[e_clean] = data

res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Agencies'!A1:N").execute()
rows = res.get('values', [])

batch_data = []
for idx, r in enumerate(rows[1:], start=2):
    r_padded = r + [''] * (14 - len(r))
    comp = r_padded[1].strip()
    em = r_padded[2].strip()
    curr_st = r_padded[4].strip()
    
    c_low = comp.lower()
    e_low = em.lower()
    
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
        update_status = match_data['status']
        update_date = match_data['date'] or today_str
        update_follow = follow_up_str if update_status == 'Applied' else ''
        update_notes = match_data['notes'] or r_padded[7]
        
        batch_data.append({
            'range': f"'Agencies'!E{idx}:H{idx}",
            'values': [[update_status, update_date, update_follow, update_notes]]
        })

if batch_data:
    print(f"Updating {len(batch_data)} rows in Agencies...")
    body = {'valueInputOption': 'RAW', 'data': batch_data}
    service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
    print("Agencies tab 100% updated!")
else:
    print("Agencies tab already 100% in sync.")
