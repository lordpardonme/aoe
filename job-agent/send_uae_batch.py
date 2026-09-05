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
        'company': 'Irwin & Dow',
        'email': 'apply@irwinanddow.com',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 108,
        'notes': 'Master Gulf CV (with photo & visa status) + FuelBuddy UAE / FinTech pitch'
    },
    {
        'company': 'JVI Global',
        'email': 'jobseekers@jvi-global.com',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 109,
        'notes': 'Master Gulf CV (with photo & visa status) + FuelBuddy UAE / enterprise systems pitch'
    },
    {
        'company': 'Kershaw Leonard',
        'email': 'mike@kershawleonard.net',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 110,
        'notes': 'Master Gulf CV (with photo & visa status) + UAE digital product representation'
    },
    {
        'company': 'Lobo Management',
        'email': 'lobo@lobomanagement.com',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 111,
        'notes': 'Master Gulf CV (with photo & visa status) + FuelBuddy UAE / senior UX pitch'
    },
    {
        'company': 'Pact Employment',
        'email': 'info@pactemployment.ae',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 114,
        'notes': 'Master Gulf CV (with photo & visa status) + UAE digital staffing pitch'
    },
    {
        'company': 'Rawafed',
        'email': 'careers@rawafed.ae',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 117,
        'notes': 'Master Gulf CV (with photo & visa status) + Abu Dhabi / UAE digital talent pitch'
    },
    {
        'company': 'Receptionist PA',
        'email': 'info@receptionistpa.com',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 118,
        'notes': 'Master Gulf CV (with photo & visa status) + professional digital design representation'
    },
    {
        'company': 'RTC-1 Employment Services',
        'email': 'info@rtc-1.com',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 119,
        'notes': 'Master Gulf CV (with photo & visa status) + Dubai / GCC executive recruitment'
    },
    {
        'company': 'Sawaeed',
        'email': 'info@sawaeed.ae',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 120,
        'notes': 'Master Gulf CV (with photo & visa status) + UAE professional workforce solutions'
    },
    {
        'company': 'Spark',
        'email': 'sparkmos@spark.ae',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 122,
        'notes': 'Master Gulf CV (with photo & visa status) + UAE digital transformation & creative UX'
    },
    {
        'company': 'SSA Ltd',
        'email': 'ian.mclean@ssaltd.com',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 123,
        'notes': 'Master Gulf CV (with photo & visa status) + middle east tech & digital search'
    },
    {
        'company': 'Talascend',
        'email': 'talascend.marketing@talascend.com',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 124,
        'notes': 'Master Gulf CV (with photo & visa status) + global & UAE technical workforce staffing'
    }
]

print(f"Starting batch send for {len(batch)} UAE agencies with Gulf Master CV...")

staging_entries = []

for idx, item in enumerate(batch, 1):
    print(f"\n[{idx}/{len(batch)}] Sending to {item['company']} ({item['email']})...")
    cmd = [
        r'job-agent\.venv\Scripts\python.exe',
        r'Job Hunt\resumes\send_application.py',
        '--to', item['email'],
        '--subject', item['subject'],
        '--body-file', r'Job Hunt\resumes\dubai-agencies-email.txt',
        '--attachment', r'Job Hunt\resumes\Mohd_Hayaat_Ali_Master_Product_Designer_CV_Gulf.pdf'
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
        "UAE Agency Sourcing (Dubai / Abu Dhabi)",
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
        f"| 2026-08-25 15:38 IST | {item['company']} (UAE / Dubai) | Senior Product Designer / UI-UX | {item['email']} | SENT | `{gmail_id}` | `Mohd_Hayaat_Ali_Master_Product_Designer_CV_Gulf.pdf` | {item['subject']} | {item['notes']} |"
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

print("\nBATCH SEND COMPLETED SUCCESSFULLY FOR ALL 12 UAE AGENCIES!")
