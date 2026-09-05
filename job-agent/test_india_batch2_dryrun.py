import subprocess
import sys

batch = [
    {
        'company': 'Artgripper Studio',
        'email': 'hello@artgripper.studio',
        'subject': 'Creative Direction & Visual Design Collaboration - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/artgripper-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
    },
    {
        'company': 'Artium Academy',
        'email': 'priya@artiumacademy.com',
        'subject': 'Creative Producer & Video Content Lead - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/artiumacademy-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
    },
    {
        'company': 'ASAP Media',
        'email': 'contact@asapmedia.co.in',
        'subject': 'Video Director, Editor & Creative Lead - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/asapmedia-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
    },
    {
        'company': 'Byond Studio',
        'email': 'team@wearebyond.com',
        'subject': 'Creative Lead & Visual Designer Collaboration - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/byondstudio-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
    },
    {
        'company': "Jaani's Cafe",
        'email': 'jaaniscafe@gmail.com',
        'subject': "Creative Direction, Reels & Visual Content for Jaani's Cafe - Mohd Hayaat Ali",
        'body': 'Job Hunt/resumes/jaaniscafe-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
    },
    {
        'company': 'Little Green Studio',
        'email': 'hr@littlegreenstudio.in',
        'subject': 'Visual Designer & Storytelling Collaboration - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/littlegreenstudio-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
    },
    {
        'company': 'Lovedwell',
        'email': 'info@lovedwell.com',
        'subject': 'Visual Designer & Brand Creative Lead - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/lovedwell-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
    },
    {
        'company': 'Museo Camera',
        'email': 'contact@museocamera.org',
        'subject': 'Photographer, Filmmaker & Visual Media Collaboration - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/museocamera-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
    },
    {
        'company': 'RAD LVNG',
        'email': 'talent@radlvng.com',
        'subject': 'Creative Lead & Visual Content Collaboration - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/radlvng-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
    },
    {
        'company': 'Remotehub Talent',
        'email': 'design.talent@remotehub.io',
        'subject': 'Senior Product Designer & Creative Lead (Remote Network) - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/remotehub-talent-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Neeraj / Hiring Lead',
        'email': 'neerajiwtwrs@gmail.com',
        'subject': 'Senior Product & UI/UX Designer Application - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/neeraj-lead-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Mushroom Studios',
        'email': 'work@mushroomstudios.in',
        'subject': 'Freelance / Full-Time Video Editor & Motion Designer - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/mushroomstudios-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf',
    },
    {
        'company': 'Orange Corporate Solutions',
        'email': 'jobs.orange001@gmail.com',
        'subject': 'Product & UI/UX Designer Representation - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/orange-agency-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
    {
        'company': 'Shell Consultancy',
        'email': 'careers@shellconsultancy.com',
        'subject': 'Senior Product Designer & UI/UX Representation - Mohd Hayaat Ali',
        'body': 'Job Hunt/resumes/shell-consultancy-email.txt',
        'attach': 'Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf',
    },
]

print(f"Testing dry run for {len(batch)} India Batch 2 targets...")

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
