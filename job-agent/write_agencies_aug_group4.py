import sys
from pathlib import Path

emails = {
    "bossinitech-email.txt": """Hi Jithu,

I'm reaching out to introduce myself for Senior UI/UX Designer and Product Design Consultant mandates across Boss In iTech’s technology and enterprise client accounts.

I am a Senior Product Designer with 6+ years of experience delivering scalable web and mobile software:
• Measurable UX Gains: Redesigned multi-step checkout flows at FuelBuddy (62% to 78% conversion) and clinical appointment booking at Meddo (71% to 83% completion).
• Systems & Delivery: Comprehensive mastery in Figma—modular component libraries, design tokens, and seamless engineering handoff.
• Operational Efficiency: Designed B2B dispatch and asset management tools that cut manual support overhead by 43%.

I am based in Delhi NCR and available to join immediately with zero notice period.

Portfolio: https://workofhayaat.framer.website (Master CV attached).

I would welcome the opportunity to discuss open senior design openings within your network.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "bostontechnology-email.txt": """Hi Malathi,

I'm reaching out regarding Senior Product Designer and Lead UI/UX opportunities within Boston Technology Corporation’s digital and enterprise solutions practice.

I bring 6+ years of hands-on experience designing high-scale digital platforms, enterprise SaaS dashboards, and consumer mobile apps:
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

    "bourntec-email.txt": """Hi Naveen,

I'm reaching out to submit my profile for Senior Product Design and UI/UX Lead mandates across Bourntec Solutions’ client portfolio spanning India, EMEA, and US markets.

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

    "bpoconvergence-ashok-email.txt": """Hi Ashok,

I'm reaching out regarding Senior Product Designer and UI/UX Lead opportunities within BPO Convergence’s human resources and consulting practice.

I bring 6+ years of experience designing high-scale digital platforms, enterprise SaaS tools, and high-conversion mobile applications:
• Measurable UX Gains: Redesigned multi-step checkout flows at FuelBuddy (62% to 78% conversion) and clinical appointment booking at Meddo (71% to 83% completion).
• Operational Systems: Replaced manual spreadsheets with unified dispatch and live telemetry at FuelBuddy, cutting operational support by 43%.
• Design Systems: Architected production Figma libraries with tokenized variables, responsive auto-layout variants, and tight engineering documentation.

Availability: Immediate (0-day notice).

Portfolio: https://workofhayaat.framer.website (Master CV attached).

I would welcome representation for relevant senior design roles across your client accounts.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "bpoconvergence-anju-email.txt": """Hi Anju,

I'm reaching out to introduce myself for Senior Product Design and UI/UX Specialist mandates across BPO Convergence’s client mandates.

I am a Senior Product Designer with 6+ years of experience shipping scalable B2B SaaS platforms, complex logistics tools, and consumer digital products:
• Operational UX: Simplified 22-step commercial ordering to 4 steps at FuelBuddy (62% to 78% completion); lifted patient booking conversion from 71% to 83% at Meddo.
• Systems Architecture: Deep Figma mastery—architecting tokenized component libraries, interactive prototypes, and developer-friendly documentation.
• Multi-Domain Range: Deep experience across logistics operations, healthcare workflows, consumer fintech, and AI automation.

Status: Immediately available (0-day notice) | Location: Delhi NCR.

Portfolio: https://workofhayaat.framer.website (Master CV attached).

I would welcome representation for relevant senior product design roles.

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
