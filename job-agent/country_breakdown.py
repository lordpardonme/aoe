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

res_m = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
rows = res_m.get('values', [])[1:]

country_status = {}
for r in rows:
    r_padded = r + [''] * (14 - len(r))
    country, company, email, l_type, status = r_padded[:5]
    ctry = country.strip() or 'Unknown'
    stat = status.strip() or 'Blank'
    if ctry not in country_status:
        country_status[ctry] = {}
    country_status[ctry][stat] = country_status[ctry].get(stat, 0) + 1

print("--- MASTER JOB TRACKER BREAKDOWN BY COUNTRY ---")
for ctry, stats in sorted(country_status.items(), key=lambda x: sum(x[1].values()), reverse=True):
    total = sum(stats.values())
    to_contact = stats.get('To Contact', 0)
    applied = stats.get('Applied', 0)
    print(f"• {ctry} (Total: {total} | To Contact: {to_contact} | Applied: {applied})")
    for s, cnt in stats.items():
        if s not in ['To Contact', 'Applied']:
            print(f"    - {s}: {cnt}")
