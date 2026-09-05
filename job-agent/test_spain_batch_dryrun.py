import subprocess
import sys

batch = [
    {
        'company': 'Michael Page Spain',
        'email': 'info@michaelpage.es',
        'subject': 'Product & UI/UX Designer Representation (Madrid & Barcelona) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/michaelpage-spain-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Hays Spain (Madrid)',
        'email': 'madrid@hays.es',
        'subject': 'Product & UI/UX Designer Representation (Madrid & Tech Scale-ups) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/hays-madrid-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Hays Spain (Barcelona)',
        'email': 'barcelona@hays.es',
        'subject': 'Product & UI/UX Designer Representation (Barcelona Tech Hub) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/hays-barcelona-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Robert Walters Spain',
        'email': 'contacto@robertwalters.com',
        'subject': 'Senior Product & UI/UX Designer Representation (Spain Mandates) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/robertwalters-spain-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Talent Search People',
        'email': 'info@talentsearchpeople.com',
        'subject': 'Product & UI/UX Designer Representation (Barcelona & Madrid) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/talentsearchpeople-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Approach People Recruitment',
        'email': 'info@approachpeople.com',
        'subject': 'Product & UI/UX Designer Representation (Spain Tech Ecosystem) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/approachpeople-spain-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Blu Selection',
        'email': 'contact@bluselection.com',
        'subject': 'Product & UI/UX Designer Representation (Barcelona Digital Hub) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/bluselection-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Catenon Spain',
        'email': 'madrid@catenon.com',
        'subject': 'Senior Product & UI/UX Designer Representation (Madrid & Spain) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/catenon-spain-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Antal International Spain',
        'email': 'LHerran@antal.com',
        'subject': 'Product & UI/UX Designer Representation (Madrid Digital Practice) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/antal-spain-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Roberto Castano Studio',
        'email': 'thephotographer@robertocastano.com',
        'subject': 'Creative Collaboration & Art Direction / Visual Production - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/robertocastano-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
    }
]

print(f"Testing dry run for {len(batch)} Spain targets...")

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
