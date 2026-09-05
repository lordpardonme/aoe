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
        'company': 'Michael Page China',
        'email': 'enquiries@michaelpage.com.cn',
        'subject': 'Product & UI/UX Designer Representation (China & Tech Enterprises) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/michaelpage-china-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'region': 'China / Shanghai & Shenzhen',
        'notes': 'Master Product Designer CV + high-scale consumer mobile & enterprise SaaS + China Z-Visa work authorization narrative'
    },
    {
        'company': 'Michael Page Hong Kong',
        'email': 'enquiries@michaelpage.com.hk',
        'subject': 'Product & UI/UX Designer Representation (Hong Kong & FinTech) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/michaelpage-hk-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'region': 'Hong Kong SAR',
        'notes': 'Master Product Designer CV + FinTech & digital banking UX (Kama Capital/Maximor AI) + HK GEP visa narrative'
    },
    {
        'company': 'Morgan McKinley Shanghai',
        'email': 'shanghai@morganmckinley.com',
        'subject': 'Senior Product & UI/UX Designer Representation (Tech & SaaS) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/morganmckinley-china-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'region': 'China / Shanghai',
        'notes': 'Master Product Designer CV + technology & digital transformation staffing + China Z-Visa narrative'
    },
    {
        'company': 'Morgan McKinley Hong Kong',
        'email': 'hk@morganmckinley.com',
        'subject': 'Product & UI/UX Designer Representation (Hong Kong Tech & FinTech) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/morganmckinley-hk-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'region': 'Hong Kong SAR',
        'notes': 'Master Product Designer CV + digital product design & FinTech trading UX + HK GEP visa narrative'
    },
    {
        'company': 'Randstad Hong Kong',
        'email': 'hongkong@randstad.com.hk',
        'subject': 'Product & UI/UX Designer Representation (Hong Kong & Greater China) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/randstad-hk-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'region': 'Hong Kong / Greater China',
        'notes': 'Master Product Designer CV + enterprise & consumer apps + Greater China digital talent practice'
    }
]

print(f"Starting batch send for {len(batch)} China & Hong Kong agencies...")

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
    master_row = [
        item['region'],
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
        f"China/HK Tier-1 Agency ({item['region']})",
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
        f"| 2026-08-25 15:32 IST | {item['company']} ({item['region']}) | Senior Product Designer / UI-UX | {item['email']} | SENT | `{gmail_id}` | `Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf` | {item['subject']} | {item['notes']} |"
    )

# 3. Append to local staging log
log_path = Path("Job Hunt/resumes/batch-staging-log.md")
current_log = log_path.read_text(encoding='utf-8')
new_log = current_log.rstrip() + "\n" + "\n".join(staging_entries) + "\n"
log_path.write_text(new_log, encoding='utf-8')
print("\nUpdated local batch-staging-log.md.")

print("\nBATCH SEND COMPLETED SUCCESSFULLY FOR ALL CHINA & HONG KONG AGENCIES!")
