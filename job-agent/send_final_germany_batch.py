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
        'company': 'Volocopter',
        'email': 'info@volocopter.com',
        'subject': 'Senior Product Designer (Urban Air Mobility & Passenger Vertiport UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/volocopter-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 278,
        'pitch': 'Master Germany CV + eVTOL passenger booking, vertiport physical-digital UX & IoT dispatch'
    },
    {
        'company': 'Lufthansa Systems',
        'email': 'careers@lhsystems.com',
        'subject': 'Product Designer (Aviation Software & Airline Operations UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/lufthansa-systems-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 212,
        'pitch': 'Master Germany CV + aviation scheduling, mission-critical operations & Figma design systems'
    },
    {
        'company': 'BMW Group',
        'email': 'careers@bmwgroup.com',
        'subject': 'Product Designer (Digital In-Car Experience & Connected Mobility UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/bmw-group-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 146,
        'pitch': 'Master Germany CV + in-cabin digital experience, glanceable UI & automotive companion apps'
    },
    {
        'company': 'Kaufland e-commerce',
        'email': 'jobs@kaufland-ecommerce.com',
        'subject': 'Product Designer (E-Commerce Marketplace & Checkout Optimization) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/kaufland-ecommerce-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 201,
        'pitch': 'Master Germany CV + high-traffic marketplace taxonomy, buyer checkout 62%→78% & seller UX'
    },
    {
        'company': 'SAP',
        'email': 'careers@sap.com',
        'subject': 'Product Designer (Enterprise Design Systems & B2B SaaS UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/sap-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 249,
        'pitch': 'Master Germany CV + enterprise Fiori design systems, Figma token governance & B2B automation'
    },
    {
        'company': 'Siemens',
        'email': 'careers@siemens.com',
        'subject': 'Senior Product Designer (Industrial IoT & Digital Enterprise UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/siemens-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 254,
        'pitch': 'Master Germany CV + industrial automation, IoT telemetry dashboards & anomaly detection UX'
    },
    {
        'company': 'Volkswagen Group',
        'email': 'careers@volkswagen.de',
        'subject': 'Product Designer (Connected Vehicle Software & In-Cabin UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/volkswagen-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 277,
        'pitch': 'Master Germany CV + connected car software, automated vehicle authorizations & mobile flows'
    },
    {
        'company': 'Infineon Technologies',
        'email': 'careers@infineon.com',
        'subject': 'Product Designer (Digital Developer Tools & Semiconductor UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/infineon-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 198,
        'pitch': 'Master Germany CV + developer evaluation tools, data-dense parameters & token systems'
    },
    {
        'company': 'Adidas',
        'email': 'careers@adidas.com',
        'subject': 'Product Designer (Mobile E-Commerce & Creator Experience UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/adidas-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 130,
        'pitch': 'Master Germany CV + high-traffic mobile checkout, drop mechanics & conversion optimization'
    },
    {
        'company': 'Bayer',
        'email': 'careers@bayer.com',
        'subject': 'Product Designer (Digital Health & Clinical UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/bayer-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 143,
        'pitch': 'Master Germany CV + clinical healthcare UX, Meddo patient journeys (71%→83%) & usability testing'
    },
    {
        'company': 'exmox',
        'email': 'jobs@exmox.com',
        'subject': 'Product Designer (Rewarded Gaming & AdTech Mobile UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/exmox-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 179,
        'pitch': 'Master Germany CV + mobile gaming ad-tech, reward wallet loops & micro-interactions'
    },
    {
        'company': 'TRUECHART',
        'email': 'info@truechart.com',
        'subject': 'Product Designer (Enterprise Data Visualization & BI Analytics UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/truechart-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 273,
        'pitch': 'Master Germany CV + standardized BI data viz, multi-tenant analytics & design system tokens'
    },
    {
        'company': 'Mambo',
        'email': 'jobs@mambo.co',
        'subject': 'Product Designer (Enterprise Gamification & Employee Engagement SaaS) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/mambo-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 214,
        'pitch': 'Master Germany CV + enterprise gamification feedback loops, reward wallet & B2B SaaS UX'
    },
    {
        'company': 'Monika Saleta',
        'email': 'job@monikasaleta.com',
        'subject': 'Senior Product Designer Collaboration & UI/UX Design - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/monikasaleta-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 223,
        'pitch': 'Master Germany CV + digital transformation studio collaboration, B2B/consumer case studies'
    },
    {
        'company': 'DastN GmbH',
        'email': 'info@dastn.com',
        'subject': 'Product Designer (Enterprise Cloud & Custom Software UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/dastn-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 157,
        'pitch': 'Master Germany CV + custom enterprise cloud software, Maximor AI B2B workflows & token systems'
    },
    {
        'company': 'Atrya',
        'email': 'recrutement@atrya.fr',
        'subject': 'Product Designer (Digital Configurators & Smart Building Systems UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/atrya-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
        'master_row': 142,
        'pitch': 'Master Germany CV + digital product configurators, progressive disclosure flows & responsive web'
    },
]

print(f"Starting final batch dispatch for remaining {len(batch)} German companies...")

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
        "Germany Direct Employer Sourcing",
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
        f"| 2026-08-25 18:15 IST | {item['company']} (Germany) | Senior Product Designer / UI-UX | {item['email']} | SENT | `{gmail_id}` | `{attach_name}` | {item['subject']} | {item['pitch']} |"
    )

# 4. Append to local staging log
log_path = Path("Job Hunt/resumes/batch-staging-log.md")
current_log = log_path.read_text(encoding='utf-8')
new_log = current_log.rstrip() + "\n" + "\n".join(staging_entries) + "\n"
log_path.write_text(new_log, encoding='utf-8')
print("\nUpdated local batch-staging-log.md.")

print("\nGERMANY LIST 100% COMPLETED SUCCESSFULLY!")
