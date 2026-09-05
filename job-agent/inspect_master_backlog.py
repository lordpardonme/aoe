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

res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
rows = res.get('values', [])
headers = rows[0]
data = rows[1:]

print(f"Total data rows in Master Job Tracker: {len(data)}")

status_map = {}
for i, r in enumerate(data):
    st = r[4].strip() if len(r) > 4 and r[4] else '[Blank]'
    status_map[st] = status_map.get(st, 0) + 1

print("\n--- MASTER JOB TRACKER EXACT STATUS BREAKDOWN ---")
for st, cnt in sorted(status_map.items(), key=lambda x: x[1], reverse=True):
    print(f"  • {st}: {cnt} rows")

to_contact_rows = []
for idx, r in enumerate(data):
    row_num = idx + 2
    row = r + [''] * (14 - len(r))
    country, company, email, l_type, status, dt_applied, dt_follow, notes, scan_status, role, url, conf, rec_act, dt_scan = row
    if status.strip().lower() == 'to contact':
        to_contact_rows.append({
            'row': row_num,
            'country': country,
            'company': company,
            'email': email,
            'type': l_type,
            'role': role
        })

print(f"\nTotal 'To Contact' rows in Master Job Tracker: {len(to_contact_rows)}")

# Check duplicate emails or companies within To Contact
email_counts = {}
company_counts = {}
no_email_rows = []

for r in to_contact_rows:
    em = r['email'].strip().lower()
    comp = r['company'].strip().lower()
    if not em:
        no_email_rows.append(r)
    else:
        email_counts[em] = email_counts.get(em, 0) + 1
    company_counts[comp] = company_counts.get(comp, 0) + 1

duplicate_emails = {k: v for k, v in email_counts.items() if v > 1}
duplicate_companies = {k: v for k, v in company_counts.items() if v > 1}

print(f"Unique email addresses in To Contact: {len(email_counts)}")
print(f"Rows without email in To Contact: {len(no_email_rows)}")
print(f"Duplicate email instances: {len(duplicate_emails)}")
print(f"Duplicate company instances: {len(duplicate_companies)}")

if duplicate_emails:
    print("\nSample Duplicate Emails in Master To Contact:")
    for em, count in list(duplicate_emails.items())[:10]:
        print(f"  - {em}: {count} rows")

if no_email_rows:
    print(f"\nSample Rows without Email in Master To Contact ({len(no_email_rows)} rows):")
    for r in no_email_rows[:10]:
        print(f"  - Row {r['row']}: {r['company']} ({r['country']})")
