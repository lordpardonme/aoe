import sys
from pathlib import Path

emails = {
    "acnovate-email.txt": """Hi Chhavi,

I'm reaching out to introduce myself for Senior Product Design and UI/UX Lead mandates across Acnovate’s enterprise and digital transformation clients.

I am a Senior Product Designer with 6+ years of experience designing complex B2B workflow platforms, data dashboards, and mobile digital products:
• Operational Platforms & SaaS: Designed enterprise fleet dispatch and operations tools at FuelBuddy, replacing manual spreadsheets with unified dispatch workflows and cutting support overhead by 43%.
• Measurable UX Gains: Streamlined multi-step user booking from 6 steps to 4 at Meddo (lifting conversion from 71% to 83%) and commercial ordering from 22 steps to 4 (62% to 78% completion).
• Design Systems: Full architecture of production Figma component libraries with tokenized variables, responsive variants, and zero-drift developer documentation.

Availability & Notice: Based in Delhi NCR, available immediately with 0-day notice (open to remote, hybrid, or on-site).

Portfolio: https://workofhayaat.framer.website (Master CV attached).

Would welcome representation for relevant senior design mandates across your client portfolio.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "acuver-email.txt": """Hi Umar,

I'm reaching out regarding Senior Product Design and UI/UX Consultant mandates within Acuver Consulting's digital commerce and supply chain practice.

I’m a Product & UI/UX Designer with 6+ years of experience shipping scalable B2B SaaS platforms, logistics systems, and omnichannel commerce flows:
• Supply & Dispatch UX: Designed enterprise telemetry, IoT fleet management, and driver dispatch systems at FuelBuddy, reducing operational escalations by 43%.
• Conversion-Focused UX: Redesigned commercial order placement from 22 steps to 4, lifting checkout conversion from 62% to 78%.
• Deep Figma Mastery: Architecting robust, scalable design systems with token variables and auto-layout variants for clean engineering handoff.

Location: Delhi NCR | Availability: Immediate (0-day notice).

Portfolio: https://workofhayaat.framer.website (Master CV attached).

I’d welcome a brief conversation to explore representation for upcoming senior product design placements.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "adecco-india-email.txt": """Hi Rajorshee,

I'm reaching out to submit my profile for Senior Product Design, UI/UX, and Lead Digital Designer mandates across Adecco India's tech and enterprise clients.

I am a Product Designer with 6+ years of experience delivering scalable web and mobile software:
• Shipped International Scale: Led UX design for platforms serving 100k+ active users across healthcare, logistics, fintech, and AI automation.
• Business Results: Streamlined patient booking journeys at Meddo (71% to 83% completion) and simplified complex B2B fuel ordering from 22 steps down to 4 (62% to 78% order conversion).
• Systems Architecture: Comprehensive Figma component libraries with strict tokens, responsive layouts, and seamless engineering documentation.

Availability: Immediate (0-day notice) | Location: Delhi NCR (open to Bangalore, Mumbai, NCR on-site/hybrid or remote).

Portfolio: https://workofhayaat.framer.website (Master CV attached).

Would love to be considered for active senior design requirements in your pipeline.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "adept-solutions-email.txt": """Hi Rajani,

I'm reaching out to introduce myself for Senior UI/UX Designer and Product Design Consultant roles across Adept Solutions' client network.

I bring 6+ years of hands-on experience designing high-scale digital platforms, enterprise SaaS dashboards, and consumer mobile apps:
• Enterprise SaaS & AI UX: Designed autonomous finance workflow interfaces at Maximor AI and real-time operational telemetry platforms at FuelBuddy.
• Conversion Optimization: Conducted usability testing across patients and clinicians at Meddo, reducing drop-offs and lifting appointment completion from 71% to 83%.
• Design Systems: Deep proficiency in building modular, reusable Figma design systems from scratch for rapid frontend implementation.

Status: Immediately available with zero notice period.

Portfolio: https://workofhayaat.framer.website (Master CV attached).

I would welcome representation for suitable senior product design mandates.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "aditi-venkat-email.txt": """Hi Venkat,

I'm reaching out regarding Senior Product Designer and Lead UI/UX opportunities within Aditi Consulting’s enterprise and digital technology practice.

I am a Senior Product Designer with 6+ years of experience designing complex enterprise platforms, B2B SaaS workflows, and mobile applications:
• Shipped Enterprise Scale: Led design from discovery to engineering delivery for platforms serving 100k+ users, cutting operational support overhead by 43% at FuelBuddy.
• Proven UX Performance: Lifted conversion rates from 62% to 78% on commercial ordering flows and improved booking completion from 71% to 83% at Meddo.
• Design Systems: Built scalable component architectures in Figma with tokenized variables and clear handoff specs.

I am based in Delhi NCR and available to start immediately (0-day notice).

Portfolio: https://workofhayaat.framer.website (Master CV attached).

I would welcome representation for senior design mandates across your client accounts.

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
