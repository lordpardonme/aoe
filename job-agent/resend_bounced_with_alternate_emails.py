import sys
import io
import re
import subprocess
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

alternate_batch = [
    {
        'company': 'Blinkist',
        'email': 'hello@blinkist.com',
        'subject': 'Product Designer (Consumer Discovery & Microlearning UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/blinkist-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 145,
        'pitch': 'Resent to verified alternate contact hello@blinkist.com'
    },
    {
        'company': 'Choco',
        'email': 'contact@choco.com',
        'subject': 'Senior Product Designer (B2B FoodTech & Supply Ordering) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/choco-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 153,
        'pitch': 'Resent to verified alternate contact contact@choco.com'
    },
    {
        'company': 'exmox',
        'email': 'info@exmox.com',
        'subject': 'Product Designer (Rewarded Gaming & AdTech Mobile UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/exmox-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 179,
        'pitch': 'Resent to verified Impressum contact info@exmox.com'
    },
    {
        'company': 'Sawaeed Holding',
        'email': 'info@sawaeedholding.com',
        'subject': 'Product & UI/UX Designer Representation (Abu Dhabi & UAE Mandates) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/sawaeed-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Gulf.pdf',
        'master_row': 114,
        'pitch': 'Resent to verified holding contact info@sawaeedholding.com'
    },
]

print(f"Sending to {len(alternate_batch)} verified alternate emails...")

for item in alternate_batch:
    print(f"\nSending to {item['company']} ({item['email']})...")
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
    
    match = re.search(r'id=([a-f0-9]+)', out)
    if not match:
        print(f"FAILED sending to {item['company']}: {res.stderr}")
        continue
    
    gmail_id = match.group(1)
    print(f"Captured Gmail Message ID: {gmail_id}")
    
    # Update Master Job Tracker
    r_idx = item['master_row']
    update_range = f"'Master Job Tracker'!C{r_idx}:H{r_idx}"
    note_val = f"{item['pitch']} | Gmail ID: {gmail_id}"
    body = {'values': [[item['email'], 'Direct Employer' if 'sawaeed' not in item['email'] else 'Agency', 'Applied', today_str, follow_up_str, note_val]]}
    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body=body).execute()
    print(f"Updated Master Job Tracker Row {r_idx}")
    
    # Append to Sent By Me
    sent_row = [
        item['company'],
        item['email'],
        "Direct Employer" if 'sawaeed' not in item['email'] else "Agency",
        "Applied",
        today_str,
        item['subject'],
        gmail_id,
        "Master Job Tracker",
        f"Follow up {follow_up_str}",
        "Bounced Lead Alternate Email Resolution",
        item['pitch']
    ]
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="'Sent By Me'!A1",
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': [sent_row]}
    ).execute()
    print("Appended to Sent By Me")

print("\nALTERNATE EMAIL SENDS COMPLETED CLEANLY!")
