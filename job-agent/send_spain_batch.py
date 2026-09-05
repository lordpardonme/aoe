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
        'company': 'Michael Page Spain',
        'email': 'info@michaelpage.es',
        'subject': 'Product & UI/UX Designer Representation (Madrid & Barcelona) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/michaelpage-spain-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'type': 'Agency',
        'hub': 'Spain / Madrid & Barcelona',
        'notes': 'Master Product Designer CV + Spain HQP visa / remote contractor pitch',
        'is_new': True
    },
    {
        'company': 'Hays Spain (Madrid)',
        'email': 'madrid@hays.es',
        'subject': 'Product & UI/UX Designer Representation (Madrid & Tech Scale-ups) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/hays-madrid-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'type': 'Agency',
        'hub': 'Spain / Madrid',
        'notes': 'Master Product Designer CV + Madrid tech ecosystem & HQP visa pitch',
        'is_new': True
    },
    {
        'company': 'Hays Spain (Barcelona)',
        'email': 'barcelona@hays.es',
        'subject': 'Product & UI/UX Designer Representation (Barcelona Tech Hub) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/hays-barcelona-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'type': 'Agency',
        'hub': 'Spain / Barcelona',
        'notes': 'Master Product Designer CV + Barcelona tech hub & software SaaS pitch',
        'is_new': True
    },
    {
        'company': 'Robert Walters Spain',
        'email': 'contacto@robertwalters.com',
        'subject': 'Senior Product & UI/UX Designer Representation (Spain Mandates) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/robertwalters-spain-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'type': 'Agency',
        'hub': 'Spain / Madrid & Barcelona',
        'notes': 'Master Product Designer CV + FinTech & trading platforms representation in Spain',
        'is_new': True
    },
    {
        'company': 'Talent Search People',
        'email': 'info@talentsearchpeople.com',
        'subject': 'Product & UI/UX Designer Representation (Barcelona & Madrid) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/talentsearchpeople-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'type': 'Agency',
        'hub': 'Spain / Barcelona & Madrid',
        'notes': 'Master Product Designer CV + specialized UI/UX and digital creative divisions',
        'is_new': True
    },
    {
        'company': 'Approach People Recruitment',
        'email': 'info@approachpeople.com',
        'subject': 'Product & UI/UX Designer Representation (Spain Tech Ecosystem) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/approachpeople-spain-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'type': 'Agency',
        'hub': 'Spain / Madrid & Barcelona',
        'notes': 'Master Product Designer CV + multilingual tech & product design practice',
        'is_new': True
    },
    {
        'company': 'Blu Selection',
        'email': 'contact@bluselection.com',
        'subject': 'Product & UI/UX Designer Representation (Barcelona Digital Hub) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/bluselection-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'type': 'Agency',
        'hub': 'Spain / Barcelona',
        'notes': 'Master Product Designer CV + Barcelona international digital talent placement',
        'is_new': True
    },
    {
        'company': 'Catenon Spain',
        'email': 'madrid@catenon.com',
        'subject': 'Senior Product & UI/UX Designer Representation (Madrid & Spain) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/catenon-spain-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'type': 'Agency',
        'hub': 'Spain / Madrid',
        'notes': 'Master Product Designer CV + digital executive & senior product design search',
        'is_new': True
    },
    {
        'company': 'Antal International Spain',
        'email': 'LHerran@antal.com',
        'subject': 'Product & UI/UX Designer Representation (Madrid Digital Practice) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/antal-spain-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'type': 'Agency',
        'hub': 'Spain / Madrid',
        'notes': 'Master Product Designer CV + tech & creative digital practice in Madrid',
        'is_new': True
    },
    {
        'company': 'Roberto Castano Studio',
        'email': 'thephotographer@robertocastano.com',
        'subject': 'Creative Collaboration & Art Direction / Visual Production - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/robertocastano-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
        'type': 'Direct Employer',
        'hub': 'Spain',
        'notes': 'Master Creative CV + Art Direction, commercial product imagery, Showreel & color grading',
        'is_new': False,
        'master_row': 246
    }
]

print(f"Starting batch send for {len(batch)} Spain targets...")

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
    
    # 1. Update or Append to Master Job Tracker
    if not item['is_new']:
        r_idx = item['master_row']
        update_range = f"'Master Job Tracker'!E{r_idx}:H{r_idx}"
        note_val = f"{item['notes']} | Gmail ID: {gmail_id}"
        body = {'values': [['Applied', today_str, follow_up_str, note_val]]}
        service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body=body).execute()
        print(f"Updated Master Job Tracker Row {r_idx}")
    else:
        master_row = [
            item['hub'],
            item['company'],
            item['email'],
            item['type'],
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
        item['type'],
        "Applied",
        today_str,
        item['subject'],
        gmail_id,
        "Master Job Tracker",
        f"Follow up {follow_up_str}",
        f"Spain Sourcing ({item['hub']})",
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
    attach_name = Path(item['attach']).name
    staging_entries.append(
        f"| 2026-08-25 15:56 IST | {item['company']} ({item['hub']}) | Senior Product Designer / Creative | {item['email']} | SENT | `{gmail_id}` | `{attach_name}` | {item['subject']} | {item['notes']} |"
    )

# 3. Update Priority Outreach Backlog for Roberto Castano
try:
    res_p = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Priority Outreach Backlog'!A1:J").execute()
    p_rows = res_p.get('values', [])
    for p_idx, r in enumerate(p_rows[1:], start=2):
        if len(r) > 4 and 'thephotographer@robertocastano.com' in r[4].lower():
            gid = batch[-1].get('gmail_id', '')
            update_range_p = f"'Priority Outreach Backlog'!H{p_idx}:J{p_idx}"
            rec_pitch = r[8] if len(r) > 8 else ''
            nts = r[9] if len(r) > 9 else ''
            new_nts = (nts + " | " if nts else "") + f"Applied {today_str}, ID: {gid}"
            service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range_p, valueInputOption='RAW', body={'values': [['Applied', rec_pitch, new_nts]]}).execute()
            print(f"Updated Priority Backlog row {p_idx} for Roberto Castano.")
except Exception as e:
    print("Priority Backlog note:", e)

# 4. Append to local staging log
log_path = Path("Job Hunt/resumes/batch-staging-log.md")
current_log = log_path.read_text(encoding='utf-8')
new_log = current_log.rstrip() + "\n" + "\n".join(staging_entries) + "\n"
log_path.write_text(new_log, encoding='utf-8')
print("\nUpdated local batch-staging-log.md.")

print("\nBATCH SEND COMPLETED SUCCESSFULLY FOR ALL 10 SPAIN TARGETS!")
