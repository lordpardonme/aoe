import subprocess
import sys

batch = [
    {
        'company': 'Celonis',
        'email': 'careers@celonis.com',
        'subject': 'Senior Product Designer (Process Intelligence & Enterprise B2B SaaS) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/celonis-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'LearnTube.ai',
        'email': 'shronit@learntube.ai',
        'subject': 'Product Designer (AI Microlearning & Interactive Course UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/learntube-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'WebVeda',
        'email': 'divyam.chutani@webveda.com',
        'subject': 'Product Designer (EdTech Platform & Course Funnels UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/webveda-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Nikah Forever',
        'email': 'career@nikahforever.com',
        'subject': 'Product Designer (Matrimony App, KYC & Matching UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/nikahforever-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Merck India',
        'email': 'careers.india@merckgroup.com',
        'subject': 'Product Designer (Digital Healthcare & Clinical Informatics UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/merck-india-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Studio Murb',
        'email': 'hey@studiomurb.com',
        'subject': 'Senior Product & UI/UX Designer Collaboration - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/studiomurb-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'ShaperCult',
        'email': 'kajal@shapercult.com',
        'subject': 'Senior Product Designer (B2B SaaS & Design Systems) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/shapercult-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Social Watch',
        'email': 'hr@socialwatch.io',
        'subject': 'Product Designer (Analytics SaaS & Web Dashboard UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/socialwatch-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'OneGraphite',
        'email': 'krunal@onegraphite.in',
        'subject': 'Senior Product Designer (B2B SaaS & Product Systems) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/onegraphite-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'The Ombre',
        'email': 'careers@theombre.com',
        'subject': 'Product Designer (Visual Systems & Digital Brand Experiences) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/theombre-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'BSD (Bangalore School of Design)',
        'email': 'amlanjyotibharali@bsd.edu.in',
        'subject': 'UI/UX & Product Design Role - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/bsd-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Reslink',
        'email': 'team@reslink.org',
        'subject': 'Product Designer (Platform Architecture & UI/UX Systems) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/reslink-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
]

print(f"Testing dry run for {len(batch)} India targets...")

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
        print(f"[DRY-RUN OK] {item['company']} -> {item['email']}")
    else:
        print(f"[DRY-RUN FAILED] {item['company']}: {res.stderr}")
