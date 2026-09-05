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
        'company': 'Artgripper Studio',
        'email': 'hello@artgripper.studio',
        'subject': 'Creative Direction & Visual Design Collaboration - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/artgripper-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
        'master_row': 139,
        'type': 'Direct Employer',
        'pitch': 'Master Creative CV + visual brand systems, art direction & 200+ campaign assets'
    },
    {
        'company': 'Artium Academy',
        'email': 'priya@artiumacademy.com',
        'subject': 'Creative Producer & Video Content Lead - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/artiumacademy-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
        'master_row': 140,
        'type': 'Direct Employer',
        'pitch': 'Master Creative CV + music edtech video production, 50+ commercial films & AcadPlaza discovery'
    },
    {
        'company': 'ASAP Media',
        'email': 'contact@asapmedia.co.in',
        'subject': 'Video Director, Editor & Creative Lead - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/asapmedia-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
        'master_row': 141,
        'type': 'Direct Employer',
        'pitch': 'Master Creative CV + commercial video direction, DaVinci color grading & high-velocity reels'
    },
    {
        'company': 'Byond Studio',
        'email': 'team@wearebyond.com',
        'subject': 'Creative Lead & Visual Designer Collaboration - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/byondstudio-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
        'master_row': 148,
        'type': 'Direct Employer',
        'pitch': 'Master Creative CV + 3D visual storytelling, brand motion & After Effects systems'
    },
    {
        'company': "Jaani's Cafe",
        'email': 'jaaniscafe@gmail.com',
        'subject': "Creative Direction, Reels & Visual Content for Jaani's Cafe - Mohd Hayaat Ali",
        'body': 'Job Hunt/resumes/jaaniscafe-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
        'master_row': 199,
        'type': 'Direct Employer',
        'pitch': "Master Creative CV + bespoke offer to shoot 3 high-craft reels & photography for Jaani's Cafe"
    },
    {
        'company': 'Little Green Studio',
        'email': 'hr@littlegreenstudio.in',
        'subject': 'Visual Designer & Storytelling Collaboration - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/littlegreenstudio-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
        'master_row': 209,
        'type': 'Direct Employer',
        'pitch': 'Master Creative CV + organic visual storytelling, brand identity & typography craft'
    },
    {
        'company': 'Lovedwell',
        'email': 'info@lovedwell.com',
        'subject': 'Visual Designer & Brand Creative Lead - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/lovedwell-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
        'master_row': 211,
        'type': 'Direct Employer',
        'pitch': 'Master Creative CV + D2C brand visuals, lifestyle reels & e-commerce conversion design'
    },
    {
        'company': 'Museo Camera',
        'email': 'contact@museocamera.org',
        'subject': 'Photographer, Filmmaker & Visual Media Collaboration - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/museocamera-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
        'master_row': 225,
        'type': 'Direct Employer',
        'pitch': 'Master Creative CV + photographic craft, exhibition media curation & documentary filmmaking'
    },
    {
        'company': 'RAD LVNG',
        'email': 'talent@radlvng.com',
        'subject': 'Creative Lead & Visual Content Collaboration - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/radlvng-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
        'master_row': 242,
        'type': 'Direct Employer',
        'pitch': 'Master Creative CV + lifestyle media direction, editorial typography & culture-driven reels'
    },
    {
        'company': 'Remotehub Talent',
        'email': 'design.talent@remotehub.io',
        'subject': 'Senior Product Designer & Creative Lead (Remote Network) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/remotehub-talent-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 244,
        'type': 'Direct Employer',
        'pitch': 'Master Product Designer CV + remote design talent pool, 100k+ user platforms & design systems'
    },
    {
        'company': 'Neeraj / Hiring Lead',
        'email': 'neerajiwtwrs@gmail.com',
        'subject': 'Senior Product & UI/UX Designer Application - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/neeraj-lead-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 297,
        'type': 'LinkedIn Search',
        'pitch': 'Master Product Designer CV + multi-domain UX results (FuelBuddy 62%→78%, Meddo 71%→83%)'
    },
    {
        'company': 'Mushroom Studios',
        'email': 'work@mushroomstudios.in',
        'subject': 'Freelance / Full-Time Video Editor & Motion Designer - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/mushroomstudios-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
        'master_row': 306,
        'type': 'Phone WhatsApp',
        'pitch': 'Master Creative CV + post-production lead, DaVinci grading & After Effects kinetic motion'
    },
    {
        'company': 'Orange Corporate Solutions',
        'email': 'jobs.orange001@gmail.com',
        'subject': 'Product & UI/UX Designer Representation - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/orange-agency-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 113,
        'type': 'Agency',
        'pitch': 'Master Product Designer CV + recruitment representation for corporate/startup mandates'
    },
    {
        'company': 'Shell Consultancy',
        'email': 'careers@shellconsultancy.com',
        'subject': 'Senior Product Designer & UI/UX Representation - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/shell-consultancy-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 121,
        'type': 'Agency',
        'pitch': 'Master Product Designer CV + recruitment representation for senior enterprise/tech mandates'
    },
]

print(f"Starting batch dispatch for {len(batch)} India Batch 2 targets...")

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
    body = {'values': [[item['email'], item['type'], 'Applied', today_str, follow_up_str, note_val]]}
    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body=body).execute()
    print(f"Updated Master Job Tracker Row {r_idx}")
    
    # 2. Append to Sent By Me
    sent_row = [
        item['company'],
        item['email'],
        item['type'],
        "Applied",
        today_str,
        item['subject'],
        gmail_id,
        "Master Job Tracker",
        f"Follow up {follow_up_str}",
        "India Creative & Brand Sourcing",
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
        f"| 2026-08-26 01:42 IST | {item['company']} (India) | Creative / Media / Product | {item['email']} | SENT | `{gmail_id}` | `{attach_name}` | {item['subject']} | {item['pitch']} |"
    )

# 4. Append to local staging log
log_path = Path("Job Hunt/resumes/batch-staging-log.md")
current_log = log_path.read_text(encoding='utf-8')
new_log = current_log.rstrip() + "\n" + "\n".join(staging_entries) + "\n"
log_path.write_text(new_log, encoding='utf-8')
print("\nUpdated local batch-staging-log.md.")

print("\nINDIA BATCH 2 SENDS COMPLETED SUCCESSFULLY!")
