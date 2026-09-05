import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

today_str = "2026-08-25"
follow_up_str = "2026-09-01"

updates = [
    {
        'row': 143,
        'email': 'recruiting@bayer.com',
        'status': 'Applied',
        'note': 'Resent to verified recruiting@bayer.com (Gmail ID: 1a0391cb9ee31c01)'
    },
    {
        'row': 223,
        'email': 'job@monikasaleta.com',
        'status': 'Applied - Form Required',
        'note': 'Replied 2026-08-25: Submit via Google Form https://forms.gle/djoqLn9KWkqqPMFc8'
    },
    {
        'row': 201,
        'email': 'jobs@kaufland-ecommerce.com',
        'status': 'Undeliverable / Bounced',
        'note': 'Remote mail server misconfigured; apply via kaufland-ecommerce.com/careers'
    },
    {
        'row': 146,
        'email': 'careers@bmwgroup.com',
        'status': 'Undeliverable / Bounced',
        'note': 'Inbox closed per GDPR; apply via bmwgroup.jobs'
    },
    {
        'row': 277,
        'email': 'careers@volkswagen.de',
        'status': 'Undeliverable / Bounced',
        'note': 'Inbox closed per GDPR; apply via volkswagen-group.com/careers'
    },
    {
        'row': 179,
        'email': 'jobs@exmox.com',
        'status': 'Undeliverable / Bounced',
        'note': 'Inbox closed; apply via exmox.com/careers'
    },
    {
        'row': 154,
        'email': 'careers@contentful.com',
        'status': 'Undeliverable / Bounced',
        'note': 'Inbox closed; apply via contentful.com/careers'
    },
]

for u in updates:
    r_idx = u['row']
    update_range = f"'Master Job Tracker'!C{r_idx}:H{r_idx}"
    body = {'values': [[u['email'], 'Direct Employer', u['status'], today_str, follow_up_str if u['status'] == 'Applied' else '', u['note']]]}
    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body=body).execute()
    print(f"Updated Master Job Tracker Row {r_idx} -> {u['status']}")

print("\nRECONCILIATION OF BOUNCES AND ALTERNATIVE EMAILS COMPLETED!")
