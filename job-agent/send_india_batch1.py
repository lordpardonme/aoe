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
        'company': 'Celonis',
        'email': 'careers@celonis.com',
        'subject': 'Senior Product Designer (Process Intelligence & Enterprise B2B SaaS) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/celonis-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 151,
        'pitch': 'Master Product Designer CV + process intelligence, Maximor AI B2B workflows & FuelBuddy ops'
    },
    {
        'company': 'LearnTube.ai',
        'email': 'shronit@learntube.ai',
        'subject': 'Product Designer (AI Microlearning & Interactive Course UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/learntube-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 206,
        'pitch': 'Master Product Designer CV + AI microlearning UX, AcadPlaza course discovery (+18% QoQ) & Meddo'
    },
    {
        'company': 'WebVeda',
        'email': 'divyam.chutani@webveda.com',
        'subject': 'Product Designer (EdTech Platform & Course Funnels UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/webveda-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 280,
        'pitch': 'Master Product Designer CV + EdTech learning journeys, AcadPlaza (+18% QoQ) & booking conversion'
    },
    {
        'company': 'Nikah Forever',
        'email': 'career@nikahforever.com',
        'subject': 'Product Designer (Matrimony App, KYC & Matching UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/nikahforever-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 228,
        'pitch': 'Master Product Designer CV + matchmaking UX, I-DOD onboarding & KYC verification flows'
    },
    {
        'company': 'Merck India',
        'email': 'careers.india@merckgroup.com',
        'subject': 'Product Designer (Digital Healthcare & Clinical Informatics UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/merck-india-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 221,
        'pitch': 'Master Product Designer CV + digital health UX, Meddo patient/doctor clinical records (71%→83%)'
    },
    {
        'company': 'Studio Murb',
        'email': 'hey@studiomurb.com',
        'subject': 'Senior Product & UI/UX Designer Collaboration - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/studiomurb-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 263,
        'pitch': 'Master Product Designer CV + digital studio collaboration, end-to-end mobile/web case studies'
    },
    {
        'company': 'ShaperCult',
        'email': 'kajal@shapercult.com',
        'subject': 'Senior Product Designer (B2B SaaS & Design Systems) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/shapercult-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 253,
        'pitch': 'Master Product Designer CV + B2B SaaS product design, Maximor AI & FuelBuddy operational tools'
    },
    {
        'company': 'Social Watch',
        'email': 'hr@socialwatch.io',
        'subject': 'Product Designer (Analytics SaaS & Web Dashboard UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/socialwatch-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 256,
        'pitch': 'Master Product Designer CV + social analytics SaaS, data-dense dashboard viz & token systems'
    },
    {
        'company': 'OneGraphite',
        'email': 'krunal@onegraphite.in',
        'subject': 'Senior Product Designer (B2B SaaS & Product Systems) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/onegraphite-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 233,
        'pitch': 'Master Product Designer CV + product design studio, Figma token variables & enterprise SaaS'
    },
    {
        'company': 'The Ombre',
        'email': 'careers@theombre.com',
        'subject': 'Product Designer (Visual Systems & Digital Brand Experiences) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/theombre-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 271,
        'pitch': 'Master Product Designer CV + brand visual systems, Uncover design system & responsive web craft'
    },
    {
        'company': 'BSD (Bangalore School of Design)',
        'email': 'amlanjyotibharali@bsd.edu.in',
        'subject': 'UI/UX & Product Design Role - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/bsd-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 305,
        'pitch': 'Master Product Designer CV + UI/UX design mandate, multi-domain case studies & Figma systems'
    },
    {
        'company': 'Reslink',
        'email': 'team@reslink.org',
        'subject': 'Product Designer (Platform Architecture & UI/UX Systems) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/reslink-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 307,
        'pitch': 'Master Product Designer CV + digital platform architecture, role-based workflows & mobile UX'
    },
]

print(f"Starting batch dispatch for {len(batch)} India Product/Tech targets...")

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
    update_range = f"'Master Job Tracker'!C{r_idx}:H{r_idx}"
    note_val = f"{item['pitch']} | Gmail ID: {gmail_id}"
    body = {'values': [[item['email'], 'Direct Employer', 'Applied', today_str, follow_up_str, note_val]]}
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
        "India Tech Startups & Studios Sourcing",
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
    
    # 3. Staging entry
    attach_name = Path(item['attach']).name
    staging_entries.append(
        f"| 2026-08-25 22:36 IST | {item['company']} (India) | Product Designer / UI-UX | {item['email']} | SENT | `{gmail_id}` | `{attach_name}` | {item['subject']} | {item['pitch']} |"
    )

# 4. Append to local staging log
log_path = Path("Job Hunt/resumes/batch-staging-log.md")
current_log = log_path.read_text(encoding='utf-8')
new_log = current_log.rstrip() + "\n" + "\n".join(staging_entries) + "\n"
log_path.write_text(new_log, encoding='utf-8')
print("\nUpdated local batch-staging-log.md.")

print("\nINDIA BATCH 1 SENDS COMPLETED SUCCESSFULLY!")
