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
        'company': 'Airswift',
        'email': 'talentacquisition@airswift.com',
        'subject': 'Product & UI/UX Designer Representation (Netherlands & Europe) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/airswift-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'notes': 'Master Product Designer CV + operations/enterprise SaaS focus + visa sponsorship & NL availability',
        'master_row': 102
    },
    {
        'company': 'Blue Lynx',
        'email': 'amsterdam@bluelynx.com',
        'subject': 'Product & UI/UX Designer Representation (Amsterdam & Netherlands) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/bluelynx-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'notes': 'Master Product Designer CV + international digital product focus + visa sponsorship & NL availability',
        'master_row': 103
    },
    {
        'company': 'Octagon Professionals',
        'email': 'info@octagon.nl',
        'subject': 'Product & UI/UX Designer Representation (Netherlands) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/octagon-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'notes': 'Master Product Designer CV + business impact & SaaS metrics + visa sponsorship & NL availability',
        'master_row': 112
    },
    {
        'company': 'Randstad Netherlands',
        'email': 'info@nl.randstad.com',
        'subject': 'Product & UI/UX Designer Representation (Amsterdam & Netherlands) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/randstad-nl-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'notes': 'Master Product Designer CV + enterprise systems & scale + visa sponsorship & NL availability',
        'master_row': 115
    },
    {
        'company': 'Ravecruitment',
        'email': 'info@ravecruitment.com',
        'subject': 'Senior Product & UI/UX Designer Representation (Tech & SaaS) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/ravecruitment-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'notes': 'Master Product Designer CV + tech/software & complex dashboards + visa sponsorship & NL availability',
        'master_row': 116
    },
    {
        'company': 'Undutchables',
        'email': 'hq@undutchables.nl',
        'subject': 'Product & UI/UX Designer Representation (Netherlands Multilingual Talent) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/undutchables-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'notes': 'Master Product Designer CV + multilingual international talent representation + visa sponsorship & NL availability',
        'master_row': 126
    }
]

print(f"Starting batch send for {len(batch)} Netherlands agencies...")

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
    
    # 1. Update Master Job Tracker
    r_idx = item['master_row']
    update_range = f"'Master Job Tracker'!E{r_idx}:H{r_idx}"
    note_val = f"{item['notes']} | Gmail ID: {gmail_id}"
    body = {'values': [['Applied', today_str, follow_up_str, note_val]]}
    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body=body).execute()
    print(f"Updated Master Job Tracker Row {r_idx}")
    
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
        "Amsterdam sponsor-list lead / Agency",
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
        f"| 2026-08-25 15:17 IST | {item['company']} (Netherlands) | Senior Product Designer / UI-UX | {item['email']} | SENT | `{gmail_id}` | `Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf` | {item['subject']} | {item['notes']} |"
    )

# 3. Update Priority Outreach Backlog
try:
    res_p = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Priority Outreach Backlog'!A1:J").execute()
    p_rows = res_p.get('values', [])
    for p_idx, r in enumerate(p_rows[1:], start=2):
        r_padded = r + [''] * (10 - len(r))
        prio, src, ctry, comp, em, typ, role, stat, rec_pitch, nts = r_padded
        for it in batch:
            if it['email'].lower() in em.lower() or it['company'].lower() in comp.lower():
                gid = it.get('gmail_id', '')
                if gid:
                    update_range = f"'Priority Outreach Backlog'!H{p_idx}:J{p_idx}"
                    new_nts = (nts + " | " if nts else "") + f"Applied {today_str}, ID: {gid}"
                    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body={'values': [['Applied', rec_pitch, new_nts]]}).execute()
                    print(f"Updated Priority Backlog Row {p_idx} for {comp}")
except Exception as e:
    print("Priority Backlog update error:", e)

# 4. Append to local staging log
log_path = Path("Job Hunt/resumes/batch-staging-log.md")
current_log = log_path.read_text(encoding='utf-8')
new_log = current_log.rstrip() + "\n" + "\n".join(staging_entries) + "\n"
log_path.write_text(new_log, encoding='utf-8')
print("\nUpdated local batch-staging-log.md.")

print("\nBATCH SEND COMPLETED SUCCESSFULLY FOR ALL NETHERLANDS AGENCIES!")
