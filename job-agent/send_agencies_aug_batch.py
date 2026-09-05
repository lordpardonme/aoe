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
        'company': 'Acnovate Corporation',
        'email': 'chhavi.bhatnagar@acnovate.com',
        'contact': 'Chhavi Bhatnagar (Chief People Officer)',
        'subject': 'Senior Product Design & UI/UX Representation - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/acnovate-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 2,
        'pitch': 'Master Product Designer CV + enterprise B2B workflows, FuelBuddy dispatch ops & Meddo conversion'
    },
    {
        'company': 'Acuver Consulting',
        'email': 'umar.k@acuverconsulting.com',
        'contact': 'Umar Kizhuvapat (Director - HR & Operations)',
        'subject': 'Senior Product Design & Supply Chain UX Consultant - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/acuver-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 3,
        'pitch': 'Master Product Designer CV + supply chain & logistics UX, FuelBuddy fleet ops (62%→78%)'
    },
    {
        'company': 'Adecco India',
        'email': 'Rajorshee.Chatterjee@adecco.com',
        'contact': 'Rajorshee Chatterjee (Recruitment Specialist)',
        'subject': 'Senior Product Design & UI/UX Lead Mandates - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/adecco-india-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 4,
        'pitch': 'Master Product Designer CV + tech & enterprise scale, 100k+ active users & design systems'
    },
    {
        'company': 'Adept Solutions India',
        'email': 'rajani@adeptsolutionsindia.com',
        'contact': 'Rajani (Talent Acquisition)',
        'subject': 'Senior UI/UX Designer & Product Design Representation - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/adept-solutions-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 5,
        'pitch': 'Master Product Designer CV + enterprise SaaS & AI UX (Maximor AI, FuelBuddy & Meddo)'
    },
    {
        'company': 'Aditi Consulting (Venkat)',
        'email': 'cvenkat@aditiconsulting.com',
        'contact': 'Venkat Challa (Sr. Director - Recruitment)',
        'subject': 'Senior Product Designer & Lead UI/UX Representation - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/aditi-venkat-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 6,
        'pitch': 'Master Product Designer CV + enterprise digital technology practice, 0-day notice'
    },
    {
        'company': 'Aditi Consulting (Jyothendra)',
        'email': 'jyothendraar@aditiconsulting.com',
        'contact': 'Jyothendra Reddy (Senior Director - Recruitment & Operations)',
        'subject': 'Senior Product Designer & UI/UX Lead - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/aditi-jyothendra-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 7,
        'pitch': 'Master Product Designer CV + operational workflows & logistics software'
    },
    {
        'company': 'Aditi Consulting (Siji)',
        'email': 'sijimolj@aditiconsulting.com',
        'contact': 'Siji John (Senior Director Talent Management)',
        'subject': 'Senior Product Design & UI/UX Talent Representation - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/aditi-siji-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 8,
        'pitch': 'Master Product Designer CV + talent management practice, B2B workflow systems'
    },
    {
        'company': 'Aditi Consulting (Ravikumar)',
        'email': 'ravikumarm@aditiconsulting.com',
        'contact': 'Ravikumar M (Director - Recruitment)',
        'subject': 'Senior Product Designer & Lead UI/UX Mandates - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/aditi-ravikumar-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 9,
        'pitch': 'Master Product Designer CV + technical B2B platforms & growth funnels'
    },
    {
        'company': 'Aditi Consulting (Nayana)',
        'email': 'nayanam@aditiconsulting.com',
        'contact': 'Nayana Martin (Associate Director L&D)',
        'subject': 'Senior Product Design & Design Systems Specialist - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/aditi-nayana-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 10,
        'pitch': 'Master Product Designer CV + design systems architecture & scalable Figma tokens'
    },
    {
        'company': 'Aditi Consulting (Madhan)',
        'email': 'madhan.kumar@aditiconsulting.com',
        'contact': 'Madhan Kumar (Director of Talent Management & Operations)',
        'subject': 'Senior Product Designer & UI/UX Lead Representation - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/aditi-madhan-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 11,
        'pitch': 'Master Product Designer CV + operations & conversion-driven mobile UX'
    },
    {
        'company': 'Aditi Consulting (Kumar)',
        'email': 'kumara@aditiconsulting.com',
        'contact': 'Kumar Anchan (Director - Recruitment)',
        'subject': 'Senior Product Designer & UI/UX Consultant - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/aditi-kumar-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 12,
        'pitch': 'Master Product Designer CV + client recruitment mandates, 6+ yrs experience'
    },
    {
        'company': 'Ampcus Inc',
        'email': 'jyoti.kajale@ampcus.com',
        'contact': 'Jyoti Kajale (VP Talent Acquisition)',
        'subject': 'Senior Product Designer & UI/UX Lead Representation - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/ampcus-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 13,
        'pitch': 'Master Product Designer CV + enterprise technology TA accounts'
    },
    {
        'company': 'Antal International',
        'email': 'puja.sharma@antal.com',
        'contact': 'Puja Sharma (Recruitment Consultant)',
        'subject': 'Senior Product Design & UI/UX Specialist - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/antal-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 14,
        'pitch': 'Master Product Designer CV + executive search & tech talent representation'
    },
    {
        'company': 'Asta CRS Inc',
        'email': 'asta_onboarding@astacrs.com',
        'contact': 'Manoj Sahoo (Recruiter and Head of Onboarding)',
        'subject': 'Senior Product Designer & UI/UX Consultant - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/astacrs-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 15,
        'pitch': 'Master Product Designer CV + enterprise onboarding & consulting practice'
    },
    {
        'company': 'Black Turtle',
        'email': 'shalini.gupta@black-turtle.co',
        'contact': 'Shalini Gupta (Talent Partner)',
        'subject': 'Senior Product Design & UI/UX Lead Mandates - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/blackturtle-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 16,
        'pitch': 'Master Product Designer CV + boutique search & leadership talent representation'
    },
    {
        'company': 'Boss In iTech',
        'email': 'jithum@bossinitech.com',
        'contact': 'Jithu M (Recruitment Lead)',
        'subject': 'Senior UI/UX Designer & Product Design Representation - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/bossinitech-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 17,
        'pitch': 'Master Product Designer CV + technology staffing mandates, 0-day notice'
    },
    {
        'company': 'Boston Technology Corp',
        'email': 'malathip@boston-technology.com',
        'contact': 'Malathi Premkumar (Vice President - Human Resources)',
        'subject': 'Senior Product Designer & Lead UI/UX Opportunities - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/bostontechnology-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 18,
        'pitch': 'Master Product Designer CV + digital solutions & enterprise innovation practice'
    },
    {
        'company': 'Bourntec Solutions Inc',
        'email': 'naveen.s@bourntec.com',
        'contact': 'Naveen Sounderrajan (Head of TA - India, EMEA & US)',
        'subject': 'Senior Product Design & UI/UX Lead (India / EMEA / US) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/bourntec-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 19,
        'pitch': 'Master Product Designer CV + cross-border mandates across India, EMEA, US'
    },
    {
        'company': 'BPO Convergence (Ashok)',
        'email': 'ashok.tripathy@bpoconvergence.com',
        'contact': 'Ashok Tripathy (PRINCIPAL CONSULTANT & GROUP HEAD HR)',
        'subject': 'Senior Product Designer & UI/UX Lead Representation - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/bpoconvergence-ashok-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 20,
        'pitch': 'Master Product Designer CV + consulting & HR practice representation'
    },
    {
        'company': 'BPO Convergence (Anju)',
        'email': 'anju.tyagi@bpoconvergence.com',
        'contact': 'Anju Tyagi (Head of HR)',
        'subject': 'Senior Product Design & UI/UX Specialist Mandates - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/bpoconvergence-anju-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'row_aug': 21,
        'pitch': 'Master Product Designer CV + human resources & digital talent mandates'
    },
]

print(f"Starting batch dispatch for {len(batch)} Agencies Aug 2026 targets...")

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
    
    # 1. Update Agencies Aug 2026 tab
    r_aug = item['row_aug']
    update_range_aug = f"'Agencies Aug 2026'!F{r_aug}:I{r_aug}"
    note_val = f"{item['pitch']} | Gmail ID: {gmail_id}"
    body_aug = {'values': [['Applied', today_str, today_str, gmail_id]]}
    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range_aug, valueInputOption='RAW', body=body_aug).execute()
    print(f"Updated Agencies Aug 2026 Row {r_aug}")
    
    # 2. Append to Sent By Me
    sent_row = [
        item['company'],
        item['email'],
        "Agency",
        "Applied",
        today_str,
        item['subject'],
        gmail_id,
        "Agencies Aug 2026",
        f"Follow up {follow_up_str}",
        "Staffing & Boutique Agencies Outreach",
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
        f"| 2026-08-26 02:05 IST | {item['company']} | Staffing & Recruitment Agency | {item['email']} | SENT | `{gmail_id}` | `{attach_name}` | {item['subject']} | {item['pitch']} |"
    )

# 4. Append to local staging log
log_path = Path("Job Hunt/resumes/batch-staging-log.md")
current_log = log_path.read_text(encoding='utf-8')
new_log = current_log.rstrip() + "\n" + "\n".join(staging_entries) + "\n"
log_path.write_text(new_log, encoding='utf-8')
print("\nUpdated local batch-staging-log.md.")

print("\nAGENCIES AUG 2026 BATCH SENDS COMPLETED SUCCESSFULLY!")
