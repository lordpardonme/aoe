import subprocess
import sys

batch = [
    {
        'company': 'Creative Niche',
        'email': 'info@creativeniche.com',
        'subject': 'Product & UI/UX Designer Representation (Toronto & Canada) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/creativeniche-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Ward Technology Talent',
        'email': 'info@wardtechtalent.com',
        'subject': 'Senior Product & UI/UX Designer Representation (Tech & SaaS) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/wardtech-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Eagle Professional Resources',
        'email': 'nesst@eagleonline.com',
        'subject': 'Product & UI/UX Designer Representation (Toronto & Ottawa) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/eagle-canada-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Ignite Technical Resources',
        'email': 'info@ignitetechnical.com',
        'subject': 'Product & UI/UX Designer Representation (Vancouver & BC) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/ignite-canada-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Randstad Canada',
        'email': 'info@randstadsourceright.ca',
        'subject': 'Product & UI/UX Designer Representation (Canada) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/randstad-ca-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    }
]

print(f"Testing dry run for {len(batch)} Canadian agencies...")

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
