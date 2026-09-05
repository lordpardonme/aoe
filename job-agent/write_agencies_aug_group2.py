import sys
from pathlib import Path

emails = {
    "aditi-jyothendra-email.txt": """Hi Jyothendra,

I'm reaching out regarding Senior Product Designer and UI/UX Lead requirements across Aditi Consulting’s enterprise and technology client operations.

I bring 6+ years of experience designing high-scale digital platforms, logistics systems, and enterprise workflow software:
• Operational & B2B UX: Replaced manual operational spreadsheets at FuelBuddy with structured dispatch, asset tracking, and role-based permissions, cutting support overhead by 43%.
• Shipped Scale & Conversion: Redesigned multi-step checkout flows at FuelBuddy (62% to 78% conversion) and clinical appointment booking at Meddo (71% to 83% completion).
• Systems & Delivery: Comprehensive mastery in Figma—modular component libraries, design tokens, and seamless engineering handoff.

I am based in Delhi NCR, immediately available with zero notice period (open to remote or on-site).

Portfolio: https://workofhayaat.framer.website (Master CV attached).

I would welcome the opportunity to discuss open senior design openings within your recruitment pipeline.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "aditi-siji-email.txt": """Hi Siji,

I'm reaching out to introduce myself for Senior Product Design and UI/UX Talent placements across Aditi Consulting’s technology accounts.

I am a Senior Product Designer with 6+ years specializing in complex B2B workflow software, data-dense dashboards, and modular design systems:
• Proven Track Record: Shipped end-to-end UX for platforms serving 100k+ active users; improved clinical appointment conversion from 71% to 83% at Meddo and commercial ordering from 62% to 78% at FuelBuddy.
• Enterprise Dashboards: Designed autonomous finance workflows at Maximor AI structuring complex calculations into clean, reviewable states.
• Design Systems Architecture: Built comprehensive Figma component libraries with token variables, auto-layout variants, and engineering documentation.

Availability: Immediate (0-day notice) | Location: Delhi NCR.

Portfolio: https://workofhayaat.framer.website (Master CV attached).

Would love to be represented for upcoming senior design talent mandates.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "aditi-ravikumar-email.txt": """Hi Ravikumar,

I'm reaching out to submit my profile for Senior Product Designer and Lead UI/UX Consultant mandates in your recruitment pipeline.

I bring 6+ years of product design experience spanning technical B2B platforms, enterprise dashboards, and mobile consumer apps:
• Enterprise Impact: Designed dispatch and asset management tools at FuelBuddy, cutting manual support input by 43%.
• Growth & Funnels: Redesigned course discovery and enrollment flows at AcadPlaza, lifting course purchases by 18% QoQ.
• Design Systems: Full architecture of production Figma component libraries with strict token variables and zero-drift developer handoff.

Status: Immediately available with zero notice period.

Portfolio: https://workofhayaat.framer.website (Master Product Designer CV attached).

I’d welcome a brief conversation to explore representation for relevant client roles.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "aditi-nayana-email.txt": """Hi Nayana,

I'm reaching out to introduce myself for Senior Product Design, Design Systems, and UI/UX Specialist mandates across Aditi Consulting’s network.

I am a Senior Product Designer with 6+ years of experience delivering scalable web and mobile software:
• Shipped International Scale: Led UX design for platforms serving 100k+ active users; improved clinical appointment conversion from 71% to 83% at Meddo.
• Complex B2B & AI Dashboards: Designed multi-tenant operations at FuelBuddy (IoT fleet tracking, dispatch) and AI financial automation workflows at Maximor AI.
• Figma Systems Mastery: Built comprehensive component architectures, tokenized variables, and clean developer handoff pipelines.

Location: Delhi NCR | Notice Period: 0 days (immediate joiner).

Portfolio: https://workofhayaat.framer.website (Master CV attached).

Would welcome representation for active senior design requirements.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "aditi-madhan-email.txt": """Hi Madhan,

I'm reaching out regarding Senior Product Designer and UI/UX Lead opportunities within Aditi Consulting’s talent management and operations practice.

I bring 6+ years of experience designing high-scale digital platforms, enterprise SaaS tools, and high-conversion mobile applications:
• Measurable UX Gains: Redesigned multi-step checkout flows at FuelBuddy (62% to 78% conversion) and clinical appointment booking at Meddo (71% to 83% completion).
• Operational Systems: Replaced manual spreadsheets with unified dispatch and live telemetry at FuelBuddy, cutting operational support by 43%.
• Design Systems: Architected production Figma libraries with tokenized variables, responsive auto-layout variants, and tight engineering documentation.

Availability: Immediate (0-day notice).

Portfolio: https://workofhayaat.framer.website (Master CV attached).

I would welcome representation for relevant senior design roles across your client portfolio.

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
