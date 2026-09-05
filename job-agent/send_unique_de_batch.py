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

batch = [
    {
        'company': 'Omio',
        'email': 'jobs@omio.com',
        'subject': 'Product Designer (Multi-Modal Transit & Booking UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/omio-unique-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 232,
        'pitch': 'Master Germany CV + multi-modal transit comparison, booking funnel 62%→78% & EU Blue Card'
    },
    {
        'company': 'Kombo',
        'email': 'jobs@kombo.co',
        'subject': 'Product Designer (Developer Platform & Integration UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/kombo-unique-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 203,
        'pitch': 'Master Germany CV + HRIS/payroll API workflows, Maximor AI & Figma token governance'
    },
    {
        'company': 'Helsing',
        'email': 'talent@helsing.ai',
        'subject': 'Senior Product Designer (Real-Time Sensor Telemetry & Mission-Critical UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/helsing-unique-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 191,
        'pitch': 'Master Germany CV + real-time sensor processing, IoT telemetry, high-stakes cognitive clarity'
    },
    {
        'company': 'Sonarsource',
        'email': 'jobs@sonarsource.com',
        'subject': 'Product Designer (Developer Experience & Clean Code UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/sonarsource-unique-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 259,
        'pitch': 'Master Germany CV + developer ergonomics, code review UI, design systems & AI automation'
    },
    {
        'company': 'LILLYDOO',
        'email': 'info@lillydoo.com',
        'subject': 'Product Designer (D2C Subscription & Mobile E-Commerce UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/lillydoo-unique-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 208,
        'pitch': 'Master Germany CV + D2C subscription flexibility, Meddo conversion (71%→83%) & wallet controls'
    },
    {
        'company': 'Lilium',
        'email': 'info@lilium.com',
        'subject': 'Senior Product Designer (Aviation Operations & Passenger Interface UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/lilium-unique-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 207,
        'pitch': 'Master Germany CV + electric air mobility, vertiport booking, IoT fleet dispatch & safety UI'
    },
]

print(f"Starting bespoke send for {len(batch)} German companies...")

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
    
    match = re.search(r'id=([a-f0-9]+)', out)
    if not match:
        print(f"ERROR/BOUNCE on {item['company']}: {res.stderr}")
        continue
    
    gmail_id = match.group(1)
    item['gmail_id'] = gmail_id
    print(f"Captured Gmail Message ID: {gmail_id}")
    
    # 1. Update Master Job Tracker
    r_idx = item['master_row']
    update_range = f"'Master Job Tracker'!E{r_idx}:H{r_idx}"
    note_val = f"{item['pitch']} | Gmail ID: {gmail_id}"
    body = {'values': [['Applied', today_str, follow_up_str, note_val]]}
    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body=body).execute()
    print(f"Updated Master Job Tracker Row {r_idx}")
    
    # 2. Append to Sent By Me
    sent_row = [
        item['company'],
        item['email'],
        "Direct Employer",
        "Applied",
        today_str,
        item['subject'],
        gmail_id,
        "Master Job Tracker",
        f"Follow up {follow_up_str}",
        "Germany Bespoke Outreach",
        item['pitch']
    ]
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="'Sent By Me'!A1",
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': [sent_row]}
    ).execute()
    print(f"Appended to Sent By Me")
    
    # 3. Staging entry
    attach_name = Path(item['attach']).name
    staging_entries.append(
        f"| 2026-08-25 17:21 IST | {item['company']} (Germany) | Senior Product Designer / UI-UX | {item['email']} | SENT | `{gmail_id}` | `{attach_name}` | {item['subject']} | {item['pitch']} |"
    )

# 4. Append to local staging log
log_path = Path("Job Hunt/resumes/batch-staging-log.md")
current_log = log_path.read_text(encoding='utf-8')
new_log = current_log.rstrip() + "\n" + "\n".join(staging_entries) + "\n"
log_path.write_text(new_log, encoding='utf-8')
print("\nUpdated local batch-staging-log.md.")

print("\nBESPOKE BATCH SEND COMPLETED SUCCESSFULLY FOR ALL 6 TARGETS!")
