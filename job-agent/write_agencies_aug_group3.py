import sys
from pathlib import Path

emails = {
    "aditi-kumar-email.txt": """Hi Kumar,

I'm reaching out to introduce myself for Senior Product Designer and Lead UI/UX Consultant mandates in your recruitment portfolio at Aditi Consulting.

I am a Senior Product Designer with 6+ years of experience shipping scalable B2B SaaS platforms, complex logistics tools, and consumer digital products:
• Operational UX: Simplified 22-step commercial ordering to 4 steps at FuelBuddy (62% to 78% completion); lifted patient booking conversion from 71% to 83% at Meddo.
• Systems Architecture: Deep Figma mastery—architecting tokenized component libraries, interactive prototypes, and developer-friendly documentation.
• Multi-Domain Range: Deep experience across logistics operations, healthcare workflows, consumer fintech, and AI automation.

Status: Immediately available (0-day notice) | Location: Delhi NCR.

Portfolio: https://workofhayaat.framer.website (Master CV attached).

I would welcome representation for relevant client roles.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "ampcus-email.txt": """Hi Jyoti,

I'm reaching out regarding Senior Product Designer and UI/UX Lead opportunities within Ampcus Inc’s talent acquisition network for enterprise technology clients.

I bring 6+ years of experience designing scalable enterprise software, technical dashboards, and mobile digital platforms:
• Shipped International Scale: Led UX design for platforms serving 100k+ active users; improved clinical appointment conversion from 71% to 83% at Meddo and commercial ordering from 62% to 78% at FuelBuddy.
• Enterprise SaaS & AI UX: Designed autonomous finance workflow interfaces at Maximor AI and real-time operational telemetry platforms at FuelBuddy.
• Design Systems Architecture: Advanced mastery in Figma—tokenized variables, responsive component libraries, and clean developer handoff pipelines.

Availability: Immediate (0-day notice) | Location: Delhi NCR.

Portfolio: https://workofhayaat.framer.website (Master Product Designer CV attached).

I would welcome the opportunity to discuss open senior design openings within your client portfolio.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "antal-email.txt": """Hi Puja,

I'm reaching out to submit my profile for Senior Product Design and UI/UX Designer mandates across Antal International’s executive and tech search accounts.

I am a Product Designer with 6+ years of experience delivering scalable web and mobile software:
• Shipped Scale: Led UX design for platforms serving 100k+ active users; lifted patient booking conversion from 71% to 83% at Meddo and commercial ordering from 62% to 78% at FuelBuddy.
• Enterprise & Operational Systems: Replaced manual spreadsheets with unified dispatch and live telemetry at FuelBuddy, cutting operational support by 43%.
• Design Systems Architecture: Advanced mastery in Figma—tokenized variables, responsive component libraries, and clean developer handoff pipelines.

Location: Delhi NCR (Available for immediate start / 0-day notice).

Portfolio: https://workofhayaat.framer.website (Master CV attached).

I would welcome representation for relevant senior design roles across your client portfolio.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "astacrs-email.txt": """Hi Manoj,

I'm reaching out to introduce myself for Senior Product Designer, UI/UX, and Design Systems Consultant opportunities with Asta CRS Inc’s enterprise client network.

I bring 6+ years of hands-on experience designing high-scale digital platforms, enterprise SaaS dashboards, and consumer mobile apps:
• Proven UX Results: Simplified 22-step commercial ordering to 4 steps at FuelBuddy (62% to 78% completion); lifted patient booking conversion from 71% to 83% at Meddo.
• Complex Workflow Simplification: Replaced manual operational spreadsheets at FuelBuddy with structured dispatch, asset tracking, and role-based permissions, cutting support overhead by 43%.
• Design Systems Architecture: Deep Figma mastery—architecting tokenized component libraries, interactive prototypes, and developer-friendly documentation.

Status: Immediately available with zero notice period.

Portfolio: https://workofhayaat.framer.website (Master CV attached).

I would welcome representation for suitable senior product design mandates.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "blackturtle-email.txt": """Hi Shalini,

I'm reaching out regarding Senior Product Design and UI/UX Lead opportunities within Black Turtle’s boutique executive and technology search practice.

I am a Senior Product Designer with 6+ years of experience designing complex enterprise platforms, B2B SaaS workflows, and mobile applications:
• Shipped Scale: Led UX design for platforms serving 100k+ active users; improved clinical appointment conversion from 71% to 83% at Meddo and commercial ordering from 62% to 78% at FuelBuddy.
• Enterprise Dashboards: Designed autonomous finance workflows at Maximor AI structuring complex calculations into clean, reviewable states.
• Design Systems Architecture: Built comprehensive Figma component libraries with token variables, auto-layout variants, and engineering documentation.

Availability: Immediate (0-day notice) | Location: Delhi NCR.

Portfolio: https://workofhayaat.framer.website (Master CV attached).

Would love to be represented for upcoming senior design talent mandates.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
"""
}

base_path = Path("Job Hunt/resumes")
for fname, content in emails.items():
    (base_path / fname).write_text(content.strip(), encoding='utf-8')
    print(f"Wrote {fname}")
