import sys
from pathlib import Path

emails = {
    "merck-india-email.txt": """Hi Merck India talent acquisition team,

Digital healthcare tools, lab informatics, and clinical life science platforms require extreme scientific clarity and human-centered design—ensuring researchers and clinicians can manage mission-critical data without friction.

I’m a Product Designer with 6+ years of experience specializing in healthcare workflows, digital diagnostics, and B2B SaaS interfaces. At Uncover by Meddo, I designed end-to-end patient, doctor, and back-office experiences across digital health records, diagnostic lab tests, and early ABHA integration interfaces. I conducted usability testing across 12 patients and 8 clinicians, streamlining appointment booking from 6 steps to 4 and lifting completion from 71% to 83%.

I’m based in Delhi NCR, available immediately with zero notice period (open to Bangalore on-site / hybrid).

Portfolio: https://workofhayaat.framer.website (Master Product Designer CV attached).

Would welcome a conversation on how my clinical and enterprise UX background can support Merck’s digital innovation teams in India.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "studiomurb-email.txt": """Hi Studio Murb team,

I came across Studio Murb’s work across digital products and brand systems, and I really admire your focus on high-craft visual execution paired with tight interaction details.

I’m a Senior Product & UI/UX Designer with 6+ years of experience delivering shipped mobile apps, B2B SaaS platforms, and brand-led digital experiences:
• End-to-End Product Craft: Led design from discovery, user flows, and wireframes to high-fidelity UI, fluid prototypes, and design systems at FuelBuddy, Meddo, and Maximor AI.
• Measurable Business Impact: Simplified 22-step commercial ordering down to 4 steps at FuelBuddy (62% to 78% completion); lifted patient booking conversion at Meddo from 71% to 83%.
• Design Systems Architecture: Deep Figma mastery—tokenized variables, auto-layout variants, and component documentation for zero-drift developer handoff.
• Creative Depth: Beyond UI/UX, I bring strong visual storytelling, art direction, and brand systems thinking.

I’m based in Delhi NCR, immediately available (0-day notice).

Portfolio: https://workofhayaat.framer.website (CV attached).

Are you currently taking on product designers or senior UI/UX collaborators for upcoming client projects?

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "shapercult-email.txt": """Hi Kajal,

Designing B2B SaaS software that people actually enjoy using is hard—it requires untangling complex operational logic, organizing dense data tables, and delivering micro-interactions that feel crisp and modern.

I’m a Senior Product Designer with 6+ years specializing in technical B2B platforms, enterprise dashboards, and design systems. At FuelBuddy, I designed enterprise operations tools replacing chaotic spreadsheets with unified dispatch and live asset tracking platforms, cutting manual customer support by 43%. At Maximor AI (maximor.ai), I designed autonomous finance workflows structuring complex multi-tier calculations into clean, reviewable screens.

I'm based in Delhi NCR, immediately available with zero notice period.

You can explore my live SaaS case studies at https://workofhayaat.framer.website (CV attached).

Are you looking for senior product designers to collaborate on ShaperCult's product design engagements?

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "socialwatch-email.txt": """Hi Social Watch team,

In social analytics and multi-channel monitoring SaaS, users need to spot trends, sentiment shifts, and engagement spikes in seconds. Great analytics design is about glanceable visual hierarchy, smart filter persistence, and zero lag.

I’m a Product & UI/UX Designer with 6+ years designing data-dense B2B dashboards, multi-metric analytics tools, and mobile platforms. At FuelBuddy, I designed real-time telemetry and operational analytics dashboards handling live data streams across hundreds of assets. Over the past 6 years, I’ve built complete design systems from scratch in Figma with modular chart widgets and clean responsive tables for rapid developer implementation.

I’m based in Delhi NCR and available to join immediately (0-day notice).

Portfolio: https://workofhayaat.framer.website (CV attached).

Are you currently hiring UI/UX or Product Designers to help expand Social Watch’s web dashboard and reporting features?

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
