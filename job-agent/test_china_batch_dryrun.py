import subprocess
import sys

batch = [
    {
        'company': 'Michael Page China',
        'email': 'enquiries@michaelpage.com.cn',
        'subject': 'Product & UI/UX Designer Representation (China & Tech Enterprises) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/michaelpage-china-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Michael Page Hong Kong',
        'email': 'enquiries@michaelpage.com.hk',
        'subject': 'Product & UI/UX Designer Representation (Hong Kong & FinTech) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/michaelpage-hk-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Morgan McKinley Shanghai',
        'email': 'shanghai@morganmckinley.com',
        'subject': 'Senior Product & UI/UX Designer Representation (Tech & SaaS) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/morganmckinley-china-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Morgan McKinley Hong Kong',
        'email': 'hk@morganmckinley.com',
        'subject': 'Product & UI/UX Designer Representation (Hong Kong Tech & FinTech) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/morganmckinley-hk-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Randstad Hong Kong',
        'email': 'hongkong@randstad.com.hk',
        'subject': 'Product & UI/UX Designer Representation (Hong Kong & Greater China) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/randstad-hk-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    }
]

print(f"Testing dry run for {len(batch)} China / HK agencies...")

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
