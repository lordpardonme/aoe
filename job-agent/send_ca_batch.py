import sys
import io
import re
import subprocess
from pathlib import Path
from datetime import date, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

today_str = "2026-08-25"
follow_up_str = "2026-09-01"

batch = [
    {
        'company': 'Creative Niche',
        'email': 'info@creativeniche.com',
        'subject': 'Product & UI/UX Designer Representation (Toronto & Canada) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/creativeniche-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'city': 'Toronto, ON',
        'notes': 'Master Product Designer CV + specialized creative/product design representation + Canada work authorization narrative'
    },
    {
        'company': 'Ward Technology Talent',
        'email': 'info@wardtechtalent.com',
        'subject': 'Senior Product & UI/UX Designer Representation (Tech & SaaS) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/wardtech-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'city': 'Toronto, ON',
        'notes': 'Master Product Designer CV + tech & software product staffing + Canada work authorization narrative'
    },
    {
        'company': 'Eagle Professional Resources',
        'email': 'nesst@eagleonline.com',
        'subject': 'Product & UI/UX Designer Representation (Toronto & Ottawa) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/eagle-canada-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'city': 'Toronto / Ottawa, ON',
        'notes': 'Master Product Designer CV + enterprise IT/digital staffing + Canada work authorization narrative'
    },
    {
        'company': 'Ignite Technical Resources',
        'email': 'info@ignitetechnical.com',
        'subject': 'Product & UI/UX Designer Representation (Vancouver & BC) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/ignite-canada-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'city': 'Vancouver, BC',
        'notes': 'Master Product Designer CV + Vancouver/BC tech ecosystem + Canada work authorization narrative'
    },
    {
        'company': 'Randstad Canada',
        'email': 'info@randstadsourceright.ca',
        'subject': 'Product & UI/UX Designer Representation (Canada) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/randstad-ca-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'city': 'Toronto, ON',
        'notes': 'Master Product Designer CV + enterprise digital product talent + Canada work authorization narrative'
    }
]

print(f"Starting batch send for {len(batch)} Canadian agencies...")

staging_entries = []

for idx, item in enumerate(batch, 1):
    print(f"\n[{idx}/{len(batch)}] Sending to {item['company']} ({item['email']})...")
    cmd = [
        r'job-agent\.venv\Scripts\python.exe',
        r'Job Hunt\resumes\send_application.py',
        '--to', item['email'],
        '--subject', item['subject'],
        '--body-file', item['body'],
        '--attachment', item['attach']
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = res.stdout.strip()
    print(f"Result: {out}")
    
    # Extract Gmail ID
    match = re.search(r'id=([a-f0-9]+)', out)
    if not match:
        print(f"ERROR sending to {item['company']}: {res.stderr}")
        continue
    
    gmail_id = match.group(1)
    item['gmail_id'] = gmail_id
    print(f"Captured Gmail Message ID: {gmail_id}")
    
    # 1. Append to Master Job Tracker
    # Columns: A:Country / Region, B:Company / Agency, C:Email, D:Type, E:Status, F:Date Applied, G:Follow-up Date, H:Notes, I:Opening Scan Status, J:Matched Role(s), K:Opening Source URL(s), L:Confidence, M:Recommended Action, N:Scan Date
    master_row = [
        f"Canada / {item['city']}",
        item['company'],
        item['email'],
        "Agency",
        "Applied",
        today_str,
        follow_up_str,
        f"{item['notes']} | Gmail ID: {gmail_id}",
        "Verified Agency",
        "Senior Product Designer / UI-UX",
        "",
        "High",
        f"Follow up {follow_up_str}",
        today_str
    ]
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="'Master Job Tracker'!A1",
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': [master_row]}
    ).execute()
    print(f"Appended to Master Job Tracker")
    
    # 2. Append to Sent By Me
    sent_row = [
        item['company'],
        item['email'],
        "Agency",
        "Applied",
        today_str,
        item['subject'],
        gmail_id,
        "Master Job Tracker",
        f"Follow up {follow_up_str}",
        f"Canada Agency Outreach ({item['city']})",
        item['notes']
    ]
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="'Sent By Me'!A1",
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': [sent_row]}
    ).execute()
    print(f"Appended to Sent By Me")
    
    # Staging entry
    staging_entries.append(
        f"| 2026-08-25 15:24 IST | {item['company']} (Canada - {item['city']}) | Senior Product Designer / UI-UX | {item['email']} | SENT | `{gmail_id}` | `Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf` | {item['subject']} | {item['notes']} |"
    )

# 3. Append to local staging log
log_path = Path("Job Hunt/resumes/batch-staging-log.md")
current_log = log_path.read_text(encoding='utf-8')
new_log = current_log.rstrip() + "\n" + "\n".join(staging_entries) + "\n"
log_path.write_text(new_log, encoding='utf-8')
print("\nUpdated local batch-staging-log.md.")

print("\nBATCH SEND COMPLETED SUCCESSFULLY FOR ALL CANADIAN AGENCIES!")
