#!/usr/bin/env python3
"""
One-off: send the two reviewed job-application emails (Greenday, shresha) with
the correct tailored PDF attached, using the existing hayaat0806@gmail.com token.
Readable and auditable. Sends exactly what is defined below - nothing generated.
"""
import base64
import mimetypes
from email.message import EmailMessage
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN = Path(__file__).with_name("token.json")
RES = Path(r"C:\Users\mohdh\Desktop\Job Hunt\Job Hunt\resumes")
SENDER = "hayaat0806@gmail.com"

SENDS = [
    {
        "to": "HR@GREENDAY.CO",
        "subject": "Designer & Video Editor - Mohd Hayaat Ali",
        "attachment": RES / "Mohd_Hayaat_Ali_Designer_Video_Editor_Greenday.pdf",
        "body": """Hi team,

I saw that Better Nutrition is hiring across multiple roles, and I'd like to be considered. I'm a multi-disciplinary designer with 6+ years across product/brand design and video editing, which means I can cover more than one of those roles.

On the design side: I design responsive web and mobile products, brand identities, and design systems. I created Uncover's logo and brand foundation and carried it across web and app, and I built design systems from scratch at FuelBuddy and I-DOD.

On the video side: my current role at Crevia has me editing videos and podcasts, creating motion and social content, and producing brand and product imagery across multiple brands - so I can design the brand and also cut the content that markets it.

A few things you can open:
- Portfolio: https://workofhayaat.framer.website
- Showreel: https://drive.google.com/drive/folders/1maf7S6y-WwfE3cdVNO8SvmM7H6slgpZW
- Uncover (logo, brand and web): https://uncover.co.in/

I'm based in Delhi NCR and open to relocation and remote. Resume attached (it covers both the design and video sides). Happy to tell me which roles you're hiring for so I can point you to the most relevant work.

Best regards,
Mohd Hayaat Ali
+91-7905194153 | mohdhayaat1@outlook.com""",
    },
    {
        "to": "shresha@andhrsolutions.in",
        "subject": "Product / UI-UX Designer open to new roles - Mohd Hayaat Ali",
        "attachment": RES / "Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf",
        "body": """Hi Shresha,

I saw your post about connecting with people looking to switch roles - I'm one of them. I'm a Product and UI/UX designer with 6+ years across web and mobile products, design systems, and brand work, currently a Creative Designer at Crevia.

Quick snapshot of my experience:
- FuelBuddy: consumer, B2B, and operational products across India and the UAE; rebuilt a 20-22 step order flow to lift completion from 62% to 78%.
- Uncover by Meddo: cut booking from six steps to four (71% to 83%), ran a 5,000-user A/B test, and created the brand and identity.
- I-DOD: built a design system from scratch.

I'm open to Product Designer, UI/UX Designer, and Senior UI/UX roles, and I'm based in Delhi NCR (open to relocation and remote).

Portfolio: https://workofhayaat.framer.website

My resume is attached. Happy to share more on a call, and glad to know which company/role you're hiring for.

Best regards,
Mohd Hayaat Ali
+91-7905194153 | mohdhayaat1@outlook.com""",
    },
]


def main():
    creds = Credentials.from_authorized_user_file(str(TOKEN))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    svc = build("gmail", "v1", credentials=creds)

    for s in SENDS:
        att = s["attachment"]
        if not att.exists():
            print(f"SKIP {s['to']}: attachment missing {att}")
            continue
        msg = EmailMessage()
        msg["To"] = s["to"]
        msg["From"] = SENDER
        msg["Subject"] = s["subject"]
        msg.set_content(s["body"])
        ctype, _ = mimetypes.guess_type(str(att))
        maintype, subtype = (ctype or "application/pdf").split("/", 1)
        msg.add_attachment(att.read_bytes(), maintype=maintype, subtype=subtype, filename=att.name)
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        sent = svc.users().messages().send(userId="me", body={"raw": raw}).execute()
        print(f"SENT to {s['to']}: id={sent['id']} threadId={sent['threadId']} attached={att.name}")


if __name__ == "__main__":
    main()
