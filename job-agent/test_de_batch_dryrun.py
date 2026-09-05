import subprocess
import sys

batch = [
    {
        'company': 'DeepL',
        'email': 'jobs@deepl.com',
        'subject': 'Product Designer (Enterprise AI & Communications UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/deepl-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
    {
        'company': 'Blinkist',
        'email': 'jobs@blinkist.com',
        'subject': 'Product Designer (Consumer Discovery & Microlearning UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/blinkist-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
    {
        'company': 'Personio',
        'email': 'careers@personio.de',
        'subject': 'Senior Product Designer (Workflow Automation & B2B SaaS) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/personio-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
    {
        'company': 'GetYourGuide',
        'email': 'jobs@getyourguide.com',
        'subject': 'Product Designer (Experience Booking & Marketplace UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/getyourguide-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
    {
        'company': 'Flix',
        'email': 'jobs@flixbus.com',
        'subject': 'Product Designer (Mobility Operations & Dispatch Systems) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/flix-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
    {
        'company': 'Contentful',
        'email': 'careers@contentful.com',
        'subject': 'Product Designer (Design Systems & Enterprise CMS UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/contentful-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
    {
        'company': 'Choco',
        'email': 'jobs@choco.com',
        'subject': 'Senior Product Designer (B2B FoodTech & Supply Ordering) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/choco-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
    {
        'company': 'Adjust',
        'email': 'jobs@adjust.com',
        'subject': 'Product Designer (Mobile Attribution & Data Dashboards) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/adjust-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
    {
        'company': 'SumUp',
        'email': 'jobs@sumup.com',
        'subject': 'Product Designer (Merchant Payments & Point-of-Sale UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/sumup-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
    {
        'company': 'Raisin',
        'email': 'jobs@raisin.com',
        'subject': 'Product Designer (FinTech & Cross-Border Banking UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/raisin-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
    {
        'company': 'Taxfix',
        'email': 'talentacquistion@taxfix.de',
        'subject': 'Product Designer (Conversational Filing & Mobile UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/taxfix-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
    {
        'company': 'Wolt Germany',
        'email': 'jobs@wolt.com',
        'subject': 'Product Designer (Quick Commerce & Courier Logistics UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/wolt-germany-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
    {
        'company': 'FINN',
        'email': 'jobs@finn.com',
        'subject': 'Product Designer (Car Subscription & Fleet Checkout UX) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/finn-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
    {
        'company': 'Solaris',
        'email': 'jobs@solarisgroup.com',
        'subject': 'Product Designer (Banking-as-a-Service & FinTech Platform) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/solaris-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
    {
        'company': 'Forto',
        'email': 'careers@forto.com',
        'subject': 'Senior Product Designer (Digital Freight & Logistics Visibility) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/forto-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
    {
        'company': 'Distribusion',
        'email': 'talent@distribusion.com',
        'subject': 'Product Designer (B2B Mobility Retail & Booking Systems) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/distribusion-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Germany.pdf',
    },
]

print(f"Testing dry run for {len(batch)} Germany scale-up targets...")

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
