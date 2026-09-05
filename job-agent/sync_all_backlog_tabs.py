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
follow_up_str = "2026-09-01"

# 1. First, fetch Master Job Tracker applied companies and emails to build canonical map
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
        if c_clean:
            applied_companies[c_clean] = {'status': status.strip(), 'date': dt_applied.strip() or today_str, 'notes': notes.strip()}
        if e_clean:
            applied_emails[e_clean] = {'status': status.strip(), 'date': dt_applied.strip() or today_str, 'notes': notes.strip()}

print(f"Loaded {len(applied_companies)} applied companies and {len(applied_emails)} applied emails from Master Job Tracker.\n")

# 2. Now iterate through other backlog sheets
tabs_to_sync = ['Direct Employers', 'Agencies', 'LinkedIn Search', 'Priority Outreach Backlog', 'Agencies Aug 2026', 'YC Startups Aug 2026', 'IT Services Aug 2026']

for tab in tabs_to_sync:
    try:
        res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=f"'{tab}'!A1:N").execute()
        rows = res.get('values', [])
        if not rows or len(rows) < 2:
            continue
        
        headers = rows[0]
        # find Status column (usually index 4 / E), Date Applied (index 5 / F), Follow-up (index 6 / G)
        c_idx = 1 # Company
        e_idx = 2 # Email
        s_idx = 4 # Status
        d_idx = 5 # Date Applied
        f_idx = 6 # Follow-up Date
        n_idx = 7 # Notes
        
        updates = []
        for idx, r in enumerate(rows[1:], start=2):
            r_padded = r + [''] * (14 - len(r))
            comp = r_padded[c_idx].strip()
            em = r_padded[e_idx].strip()
            curr_st = r_padded[s_idx].strip()
            
            c_low = comp.lower()
            e_low = em.lower()
            
            match_data = None
            if e_low and e_low in applied_emails:
                match_data = applied_emails[e_low]
            elif c_low and c_low in applied_companies:
                match_data = applied_companies[c_low]
            else:
                # partial company match
                for ac, data in applied_companies.items():
                    if len(ac) > 4 and (ac in c_low or c_low in ac):
                        match_data = data
                        break
            
            if match_data and curr_st.lower() != match_data['status'].lower():
                # update status, date applied, follow-up date, notes
                update_status = match_data['status']
                update_date = match_data['date'] or today_str
                update_follow = follow_up_str if update_status == 'Applied' else ''
                update_notes = match_data['notes'] or r_padded[n_idx]
                
                cell_range = f"'{tab}'!E{idx}:H{idx}"
                body = {'values': [[update_status, update_date, update_follow, update_notes]]}
                service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=cell_range, valueInputOption='RAW', body=body).execute()
                print(f"[{tab}] Row {idx}: {comp} -> Updated Status: '{update_status}'")
    except Exception as ex:
        print(f"Error checking tab {tab}: {ex}")

print("\nALL BACKLOG TABS SYNCHRONIZED WITH APPLIED STATUS!")
