import subprocess
import sys

batch = [
    {'company': 'Acnovate Corporation', 'email': 'chhavi.bhatnagar@acnovate.com', 'subject': 'Senior Product Design & UI/UX Representation - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/acnovate-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Acuver Consulting', 'email': 'umar.k@acuverconsulting.com', 'subject': 'Senior Product Design & Supply Chain UX Consultant - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/acuver-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Adecco India', 'email': 'Rajorshee.Chatterjee@adecco.com', 'subject': 'Senior Product Design & UI/UX Lead Mandates - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/adecco-india-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Adept Solutions India', 'email': 'rajani@adeptsolutionsindia.com', 'subject': 'Senior UI/UX Designer & Product Design Representation - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/adept-solutions-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Aditi Consulting (Venkat)', 'email': 'cvenkat@aditiconsulting.com', 'subject': 'Senior Product Designer & Lead UI/UX Representation - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/aditi-venkat-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Aditi Consulting (Jyothendra)', 'email': 'jyothendraar@aditiconsulting.com', 'subject': 'Senior Product Designer & UI/UX Lead - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/aditi-jyothendra-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Aditi Consulting (Siji)', 'email': 'sijimolj@aditiconsulting.com', 'subject': 'Senior Product Design & UI/UX Talent Representation - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/aditi-siji-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Aditi Consulting (Ravikumar)', 'email': 'ravikumarm@aditiconsulting.com', 'subject': 'Senior Product Designer & Lead UI/UX Mandates - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/aditi-ravikumar-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Aditi Consulting (Nayana)', 'email': 'nayanam@aditiconsulting.com', 'subject': 'Senior Product Design & Design Systems Specialist - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/aditi-nayana-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Aditi Consulting (Madhan)', 'email': 'madhan.kumar@aditiconsulting.com', 'subject': 'Senior Product Designer & UI/UX Lead Representation - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/aditi-madhan-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Aditi Consulting (Kumar)', 'email': 'kumara@aditiconsulting.com', 'subject': 'Senior Product Designer & UI/UX Consultant - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/aditi-kumar-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Ampcus Inc', 'email': 'jyoti.kajale@ampcus.com', 'subject': 'Senior Product Designer & UI/UX Lead Representation - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/ampcus-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Antal International', 'email': 'puja.sharma@antal.com', 'subject': 'Senior Product Design & UI/UX Specialist - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/antal-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Asta CRS Inc', 'email': 'asta_onboarding@astacrs.com', 'subject': 'Senior Product Designer & UI/UX Consultant - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/astacrs-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Black Turtle', 'email': 'shalini.gupta@black-turtle.co', 'subject': 'Senior Product Design & UI/UX Lead Mandates - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/blackturtle-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Boss In iTech', 'email': 'jithum@bossinitech.com', 'subject': 'Senior UI/UX Designer & Product Design Representation - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/bossinitech-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Boston Technology Corp', 'email': 'malathip@boston-technology.com', 'subject': 'Senior Product Designer & Lead UI/UX Opportunities - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/bostontechnology-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'Bourntec Solutions', 'email': 'naveen.s@bourntec.com', 'subject': 'Senior Product Design & UI/UX Lead (India / EMEA / US) - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/bourntec-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'BPO Convergence (Ashok)', 'email': 'ashok.tripathy@bpoconvergence.com', 'subject': 'Senior Product Designer & UI/UX Lead Representation - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/bpoconvergence-ashok-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
    {'company': 'BPO Convergence (Anju)', 'email': 'anju.tyagi@bpoconvergence.com', 'subject': 'Senior Product Design & UI/UX Specialist Mandates - Mohd Hayaat Ali', 'body': 'Job Hunt/resumes/bpoconvergence-anju-email.txt', 'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf'},
]

print(f"Testing dry run for {len(batch)} Agencies Aug 2026 targets...")

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
