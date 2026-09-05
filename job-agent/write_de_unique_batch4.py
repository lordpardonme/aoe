import sys
from pathlib import Path

emails = {
    "mambo-email.txt": """Hi Mambo team,

Effective gamification in enterprise software is rarely about adding arbitrary badges—it’s about designing intuitive feedback loops, behavioral incentives, and clear progression paths that seamlessly fit existing employee workflows.

I’m a Product & UI/UX Designer with 6+ years designing motivational user journeys, reward wallet systems, and B2B SaaS platforms. At FuelBuddy, I designed driver and operator engagement tools with automated milestone tracking and wallet rewards, reducing operational errors by 38% while improving support resolution times by 57%. I build scalable tokenized design systems in Figma for seamless multi-platform deployment.

I am eligible for the German EU Blue Card and available to relocate or work in a remote/hybrid model immediately (0-day notice).

Portfolio: https://workofhayaat.framer.website (German CV attached).

Are you currently hiring product designers to help expand Mambo's enterprise engagement and rewards platform?

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "monikasaleta-email.txt": """Hi Monika,

I came across your studio's product design and digital innovation work in Germany and wanted to reach out regarding product design collaboration and senior UI/UX design opportunities.

I’m a Product & UI/UX Designer with 6+ years of experience delivering scalable web and mobile products across healthcare, logistics, fintech, and AI automation:
• Shipped High-Impact Products: Redesigned clinical appointment booking at Meddo, lifting conversion from 71% to 83%; simplified commercial fuel ordering at FuelBuddy from 22 steps to 4 (62% to 78% completion).
• Design Systems Mastery: Comprehensive Figma architecture—component tokenization, responsive auto-layout variants, and zero-drift developer handoff.
• Community Leadership: Curated and hosted design industry community sessions inside Google and Microsoft offices during an intentional 2024–2025 sabbatical.

I am eligible for the German EU Blue Card (0-day notice, immediate availability).

You can review my live case studies at https://workofhayaat.framer.website (German-standard CV attached).

Would welcome the opportunity to connect and discuss how I can support your studio's upcoming client and product design engagements.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "dastn-email.txt": """Hi DastN team,

Building robust enterprise software and custom cloud solutions requires interface design that matches technical architecture—clean data structures, clear visual hierarchy, and intuitive user workflows that simplify complex business logic.

I’m a Product & UI/UX Designer with 6+ years designing enterprise B2B software, operational dashboards, and complex web applications. At Maximor AI (https://www.maximor.ai/cfo-offer-all), I designed autonomous close and financial automation workflows, structuring multi-step calculations into clean, reviewable screens. I have extensive experience building tokenized Figma design systems that bridge seamlessly into engineering codebases.

I hold qualification for the German EU Blue Card and am available to relocate to Germany immediately (0-day notice).

Portfolio: https://workofhayaat.framer.website (German CV attached).

Are you open to product and UI/UX designers who can partner with your engineering team on custom software engagements?

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "atrya-email.txt": """Hi Atrya digital & recruitment team,

Digital configurators and smart building systems require interfaces that make complex architectural choices, materials, and energy specifications effortless for homeowners and trade partners alike.

I’m a Product & UI/UX Designer with 6+ years of experience designing multi-step interactive configurators, B2B operational platforms, and consumer digital products. At Meddo and FuelBuddy, I specialized in breaking down dense 20+ step workflows into focused 4-step progressive flows, lifting user completion rates significantly (62% to 78% order completion). I architect modular Figma component systems with clean responsive patterns for web and mobile.

I am eligible for work authorization in Germany/Europe (EU Blue Card scheme) and immediately available with 0-day notice.

Portfolio: https://workofhayaat.framer.website (CV attached).

Would love to connect regarding digital product design and UI/UX opportunities within Atrya’s digital platforms.

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
