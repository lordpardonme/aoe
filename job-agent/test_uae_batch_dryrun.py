import subprocess
import sys

batch = [
    {
        'company': 'Irwin & Dow',
        'email': 'apply@irwinanddow.com',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 108
    },
    {
        'company': 'JVI Global',
        'email': 'jobseekers@jvi-global.com',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 109
    },
    {
        'company': 'Kershaw Leonard',
        'email': 'mike@kershawleonard.net',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 110
    },
    {
        'company': 'Lobo Management',
        'email': 'lobo@lobomanagement.com',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 111
    },
    {
        'company': 'Pact Employment',
        'email': 'info@pactemployment.ae',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 114
    },
    {
        'company': 'Rawafed',
        'email': 'careers@rawafed.ae',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 117
    },
    {
        'company': 'Receptionist PA',
        'email': 'info@receptionistpa.com',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 118
    },
    {
        'company': 'RTC-1 Employment Services',
        'email': 'info@rtc-1.com',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 119
    },
    {
        'company': 'Sawaeed',
        'email': 'info@sawaeed.ae',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 120
    },
    {
        'company': 'Spark',
        'email': 'sparkmos@spark.ae',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 122
    },
    {
        'company': 'SSA Ltd',
        'email': 'ian.mclean@ssaltd.com',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 123
    },
    {
        'company': 'Talascend',
        'email': 'talascend.marketing@talascend.com',
        'subject': 'Product & UI/UX Designer Representation (UAE & GCC Mandates) - Mohd Hayaat Ali',
        'master_row': 124
    }
]

print(f"Testing dry run for {len(batch)} UAE agencies with Gulf Master CV...")

for item in batch:
    cmd = [
        r'job-agent\.venv\Scripts\python.exe',
        r'Job Hunt\resumes\send_application.py',
        '--to', item['email'],
        '--subject', item['subject'],
        '--body-file', r'Job Hunt\resumes\dubai-agencies-email.txt',
        '--attachment', r'Job Hunt\resumes\Mohd_Hayaat_Ali_Master_Product_Designer_CV_Gulf.pdf',
        '--dry-run'
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[DRY-RUN OK] {item['company']} -> {item['email']}: {res.stdout.strip()}")
    else:
        print(f"[DRY-RUN FAILED] {item['company']}: {res.stderr.strip()}")
