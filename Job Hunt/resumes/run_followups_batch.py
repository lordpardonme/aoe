import os
import sys
import subprocess
from pathlib import Path

python_exe = sys.executable
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"

followups = [
    {
        "target": "digitup",
        "to": "nikita.dahiya1@digitup.in",
        "subject": "Re: Application – UI/UX Designer – Mohd Hayaat Ali",
        "thread_id": "19ef0b38c1e18115",
        "in_reply_to": "<CAJqzktLhuJgFt-+S=Grq_YsbZyREBRw2kT4pdVP8bjpharn9Sw@mail.gmail.com>",
        "body_file": "Job Hunt/resumes/followups/june/digitup-followup.txt",
        "attachment": "Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf"
    },
    {
        "target": "godrej",
        "to": "rominder.sapra@godrejinds.com",
        "subject": "Re: UI & Interaction Designer - Mohd Hayaat Ali",
        "thread_id": "19ebbbd1041508a9",
        "in_reply_to": "<CAJqzkt+eYxjENm2QY_ATnykW8MU_CXsm_+ep0zmZ+OssNX2GGA@mail.gmail.com>",
        "body_file": "Job Hunt/resumes/followups/june/godrej-followup.txt",
        "attachment": "Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf"
    },
    {
        "target": "houseofedtech",
        "to": "megha.gedam@houseofedtech.in",
        "subject": "Re: Application - UI/UX Designer - Mohd Hayaat Ali - 6+ Years - Gurugram/India",
        "thread_id": "19ef0b53a15c4ee3",
        "in_reply_to": "<CAJqzktJcecVFaahL6-9Q=XFbzihP05QnN5EPiJfaUJH4yo4hTw@mail.gmail.com>",
        "body_file": "Job Hunt/resumes/followups/june/houseofedtech-followup.txt",
        "attachment": "Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf"
    },
    {
        "target": "mewurk",
        "to": "kiran.pathak@mewurk.com",
        "subject": "Re: UI/UX Designer application - Mohd Hayaat Ali",
        "thread_id": "19ef3bf3cd1e56eb",
        "in_reply_to": "<CAJqzktLCvVtOVB8HueW71+8MmnJ4mR3DPsjOufkckt07bjnWrA@mail.gmail.com>",
        "body_file": "Job Hunt/resumes/followups/june/mewurk-followup.txt",
        "attachment": "Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf"
    },
    {
        "target": "monotype",
        "to": "nidhi.gupta@monotype.com",
        "subject": "Re: Product Designer - Interest in Monotype's Lead Product Designer Role",
        "thread_id": "19ebbd921ed10d29",
        "in_reply_to": "<CAJqzktKvEF4+4zeJUR3L1p4Yg+qp7AqUHtu8zwPOWDRb7d5UWw@mail.gmail.com>",
        "body_file": "Job Hunt/resumes/followups/june/monotype-followup.txt",
        "attachment": "Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf"
    },
    {
        "target": "stanify",
        "to": "ifrah@stanify.ai",
        "subject": "Re: Mid-Senior Product Designer — Mohd Hayaat Ali",
        "thread_id": "19ef6a2ac71521ec",
        "in_reply_to": "<CAJqzkt+4ZVuZd7ZeY4LPFPd8ghuh2cMz896v04-e439xsu8m3w@mail.gmail.com>",
        "body_file": "Job Hunt/resumes/followups/june/stanify-followup.txt",
        "attachment": "Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf"
    },
    {
        "target": "theartcurry",
        "to": "hellu@theartcurry.in",
        "subject": "Re: Cinematographer + Editor Application — Delhi | Showreel and Resume",
        "thread_id": "19f08fd76eb3ecda",
        "in_reply_to": "<CAJqzktLABec7S2K5NdQz5dXQp_DO5RByx1fopHpkaT5=Zf0L8A@mail.gmail.com>",
        "body_file": "Job Hunt/resumes/followups/june/theartcurry-followup.txt",
        "attachment": "Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Creative_CV.pdf"
    },
    {
        "target": "ziina",
        "to": "anton.badashov@ziina.com, jocelyn.meyer@ziina.com",
        "subject": "Re: Senior Product Designer - wallet/payment UX",
        "thread_id": "19e898b575624043",
        "in_reply_to": "<CAJqzktK5jb9N0wu1gXcpbDfsr4kCsC+d1R2ObmOEReRJjYJruw@mail.gmail.com>",
        "body_file": "Job Hunt/resumes/followups/june/ziina-followup.txt",
        "attachment": "Job Hunt/resumes/Mohd_Hayaat_Ali_Master_Product_Designer_CV_Gulf.pdf"
    }
]

dry_run = "--dry-run" in sys.argv

print(f"=== RUNNING JUNE FOLLOWUPS BATCH (Dry-run: {dry_run}) ===\n")

for f in followups:
    cmd = [
        python_exe,
        "Job Hunt/resumes/send_followup.py",
        "--to", f["to"],
        "--subject", f["subject"],
        "--body-file", f["body_file"],
        "--thread-id", f["thread_id"],
        "--in-reply-to", f["in_reply_to"]
    ]
    if Path(f["attachment"]).exists():
        cmd.extend(["--attachment", f["attachment"]])
    if dry_run:
        cmd.append("--dry-run")
    
    print(f"--> Target: {f['target']} ({f['to']})")
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    if res.returncode == 0:
        print(res.stdout.strip())
    else:
        print("ERROR:", res.stderr.strip())
    print()
