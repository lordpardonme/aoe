import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

# Read Master Job Tracker
res_m = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
master_data = res_m.get('values', [])[1:]

to_contact_master = []
for i, r in enumerate(master_data, 2):
    row = r + [''] * (14 - len(r))
    country, comp, email, l_type, status, dt_app, dt_foll, notes, scan_st, role, url, conf, rec_act, dt_scan = row
    if status.strip().lower() == 'to contact':
        to_contact_master.append({'row': i, 'country': country, 'company': comp, 'email': email.strip(), 'type': l_type, 'notes': notes})

print(f"Total 'To Contact' in Master Job Tracker: {len(to_contact_master)}")

has_direct_email = []
has_placeholder = []
has_no_email = []

for item in to_contact_master:
    em = item['email']
    if not em:
        has_no_email.append(item)
    elif any(k in em.lower() for k in ['find', 'linkedin', 'website', 'portal', 'n/a', 'none']):
        has_placeholder.append(item)
    elif '@' in em:
        has_direct_email.append(item)
    else:
        has_no_email.append(item)

print(f"  • Direct Valid Email: {len(has_direct_email)}")
print(f"  • Placeholder Text (e.g. 'find via linkedin'): {len(has_placeholder)}")
print(f"  • Completely Blank Email Cell: {len(has_no_email)}")
print(f"  -> Total without ready email in Master: {len(has_placeholder) + len(has_no_email)}")

# Check August batches (Agencies, YC Startups, IT Services)
res_aug_ag = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Agencies Aug 2026'!A1:J").execute()
aug_ag_rows = res_aug_ag.get('values', [])[1:]
aug_ag_no_email = [r for r in aug_ag_rows if len(r) < 3 or not r[2].strip() or '@' not in r[2]]

res_aug_yc = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'YC Startups Aug 2026'!A1:J").execute()
aug_yc_rows = res_aug_yc.get('values', [])[1:]
aug_yc_no_email = [r for r in aug_yc_rows if len(r) < 3 or not r[2].strip() or '@' not in r[2]]

res_aug_it = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'IT Services Aug 2026'!A1:J").execute()
aug_it_rows = res_aug_it.get('values', [])[1:]
aug_it_no_email = [r for r in aug_it_rows if len(r) < 3 or not r[2].strip() or '@' not in r[2]]

print("\nAugust Batches No-Email Check:")
print(f"  • Agencies Aug 2026 missing emails: {len(aug_ag_no_email)} of {len(aug_ag_rows)}")
print(f"  • YC Startups Aug 2026 missing emails: {len(aug_yc_no_email)} of {len(aug_yc_rows)}")
print(f"  • IT Services Aug 2026 missing emails: {len(aug_it_no_email)} of {len(aug_it_rows)}")

print("\n--- SAMPLE MASTER LEADS MISSING CONTACT EMAIL (First 15) ---")
for x in (has_placeholder + has_no_email)[:15]:
    print(f"Row {x['row']:3d} | {x['company']:<30} | Region: {x['country']:<15} | Current Email Field: '{x['email']}'")
