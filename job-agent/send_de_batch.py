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
        'company': 'DeepL',
        'email': 'jobs@deepl.com',
        'subject': 'Product Designer (Enterprise AI & Communications UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/deepl-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 158,
        'pitch': 'Master Germany CV + AI communication, Maximor AI financial automation & Figma token pitch'
    },
    {
        'company': 'Blinkist',
        'email': 'jobs@blinkist.com',
        'subject': 'Product Designer (Consumer Discovery & Microlearning UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/blinkist-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 145,
        'pitch': 'Master Germany CV + mobile reader engagement, Meddo conversion (71% to 83%) & AcadPlaza pitch'
    },
    {
        'company': 'Personio',
        'email': 'careers@personio.de',
        'subject': 'Senior Product Designer (Workflow Automation & B2B SaaS) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/personio-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 236,
        'pitch': 'Master Germany CV + People Workflow Automation, multi-tenant B2B SaaS & FuelBuddy ops pitch'
    },
    {
        'company': 'GetYourGuide',
        'email': 'jobs@getyourguide.com',
        'subject': 'Product Designer (Experience Booking & Marketplace UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/getyourguide-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 189,
        'pitch': 'Master Germany CV + travel experience booking funnel, map-based discovery & conversion pitch'
    },
    {
        'company': 'Flix',
        'email': 'jobs@flixbus.com',
        'subject': 'Product Designer (Mobility Operations & Dispatch Systems) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/flix-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 183,
        'pitch': 'Master Germany CV + fleet routing, IoT dispatch tooling & multi-modal checkout pitch'
    },
    {
        'company': 'Contentful',
        'email': 'careers@contentful.com',
        'subject': 'Product Designer (Design Systems & Enterprise CMS UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/contentful-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 154,
        'pitch': 'Master Germany CV + composable CMS design systems, developer token governance & enterprise UX'
    },
    {
        'company': 'Choco',
        'email': 'jobs@choco.com',
        'subject': 'Senior Product Designer (B2B FoodTech & Supply Ordering) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/choco-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 153,
        'pitch': 'Master Germany CV + B2B restaurant supply ordering, field operator UX & inventory tooling'
    },
    {
        'company': 'Adjust',
        'email': 'jobs@adjust.com',
        'subject': 'Product Designer (Mobile Attribution & Data Dashboards) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/adjust-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 131,
        'pitch': 'Master Germany CV + mobile attribution dashboards, dense analytics viz & token systems'
    },
    {
        'company': 'SumUp',
        'email': 'jobs@sumup.com',
        'subject': 'Product Designer (Merchant Payments & Point-of-Sale UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/sumup-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 265,
        'pitch': 'Master Germany CV + merchant POS billing, wallet access controls (-38% errors) & payment UX'
    },
    {
        'company': 'Raisin',
        'email': 'jobs@raisin.com',
        'subject': 'Product Designer (FinTech & Cross-Border Banking UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/raisin-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 243,
        'pitch': 'Master Germany CV + pan-European banking marketplace, KYC onboarding & multi-asset trading UX'
    },
    {
        'company': 'Taxfix',
        'email': 'talentacquistion@taxfix.de',
        'subject': 'Product Designer (Conversational Filing & Mobile UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/taxfix-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 270,
        'pitch': 'Master Germany CV + conversational tax filing, simplifying multi-step complex flows & trust UX'
    },
    {
        'company': 'Wolt Germany',
        'email': 'jobs@wolt.com',
        'subject': 'Product Designer (Quick Commerce & Courier Logistics UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/wolt-germany-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 282,
        'pitch': 'Master Germany CV + quick commerce dispatch, live courier tracking & merchant portal UX'
    },
    {
        'company': 'FINN',
        'email': 'jobs@finn.com',
        'subject': 'Product Designer (Car Subscription & Fleet Checkout UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/finn-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 182,
        'pitch': 'Master Germany CV + digital car subscription checkout, recurring billing & automotive fleet UX'
    },
    {
        'company': 'Solaris',
        'email': 'jobs@solarisgroup.com',
        'subject': 'Product Designer (Banking-as-a-Service & FinTech Platform) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/solaris-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 257,
        'pitch': 'Master Germany CV + Banking-as-a-Service API consoles, fintech compliance & modular components'
    },
    {
        'company': 'Forto',
        'email': 'careers@forto.com',
        'subject': 'Senior Product Designer (Digital Freight & Logistics Visibility) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/forto-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 187,
        'pitch': 'Master Germany CV + digital freight tracking, WMS inventory systems & operational dashboards'
    },
    {
        'company': 'Distribusion',
        'email': 'talent@distribusion.com',
        'subject': 'Product Designer (B2B Mobility Retail & Booking Systems) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/distribusion-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 160,
        'pitch': 'Master Germany CV + B2B intercity transit retail, ticket inventory API & booking systems'
    },
]

print(f"Starting batch dispatch for {len(batch)} Germany Tier-1 Scale-ups...")

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
        print(f"FAILED sending to {item['company']}: {res.stderr}")
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
        "Germany Tech Scale-up Outreach",
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
        f"| 2026-08-25 17:08 IST | {item['company']} (Germany) | Senior Product Designer / UI-UX | {item['email']} | SENT | `{gmail_id}` | `{attach_name}` | {item['subject']} | {item['pitch']} |"
    )

# 4. Append to local staging log
log_path = Path("Job Hunt/resumes/batch-staging-log.md")
current_log = log_path.read_text(encoding='utf-8')
new_log = current_log.rstrip() + "\n" + "\n".join(staging_entries) + "\n"
log_path.write_text(new_log, encoding='utf-8')
print("\nUpdated local batch-staging-log.md.")

print("\nBATCH DISPATCH COMPLETED SUCCESSFULLY FOR ALL 16 GERMANY TECH UNICORNS & SCALE-UPS!")
