import subprocess
import sys

batch = [
    {
        'company': 'Airswift',
        'email': 'talentacquisition@airswift.com',
        'subject': 'Product & UI/UX Designer Representation (Netherlands & Europe) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/airswift-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 102
    },
    {
        'company': 'Blue Lynx',
        'email': 'amsterdam@bluelynx.com',
        'subject': 'Product & UI/UX Designer Representation (Amsterdam & Netherlands) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/bluelynx-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 103
    },
    {
        'company': 'Octagon Professionals',
        'email': 'info@octagon.nl',
        'subject': 'Product & UI/UX Designer Representation (Netherlands) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/octagon-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 112
    },
    {
        'company': 'Randstad Netherlands',
        'email': 'info@nl.randstad.com',
        'subject': 'Product & UI/UX Designer Representation (Amsterdam & Netherlands) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/randstad-nl-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 115
    },
    {
        'company': 'Ravecruitment',
        'email': 'info@ravecruitment.com',
        'subject': 'Senior Product & UI/UX Designer Representation (Tech & SaaS) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/ravecruitment-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 116
    },
    {
        'company': 'Undutchables',
        'email': 'hq@undutchables.nl',
        'subject': 'Product & UI/UX Designer Representation (Netherlands Multilingual Talent) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/undutchables-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
        'master_row': 126
    }
]

print(f"Testing dry run for {len(batch)} Netherlands agencies...")

for item in batch:
    cmd = [
        r'job-agent\.venv\Scripts\python.exe',
        r'Job Hunt\resumes\send_application.py',
        '--to', item['email'],
        '--subject', item['subject'],
        '--body-file', item['body'],
        '--attachment', item['attach'],
        '--dry-run'
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[DRY-RUN OK] {item['company']} -> {item['email']}: {res.stdout.strip()}")
    else:
        print(f"[DRY-RUN FAILED] {item['company']}: {res.stderr.strip()}")
