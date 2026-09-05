import sys
from pathlib import Path

emails = {
    "onegraphite-email.txt": """Hi Krunal,

I came across OneGraphite's work across product design and brand systems, and I love how your team brings clean structure and functional elegance to digital interfaces.

I’m a Senior Product & UI/UX Designer with 6+ years of experience designing complex web and mobile products across healthcare, logistics, fintech, and AI automation. Over the past several years, I’ve built complete design systems from scratch in Figma with strict token architectures, variable modes, and zero-drift developer handoff. At FuelBuddy, I redesigned our commercial ordering flows from 22 steps to 4 (62% to 78% completion); at Meddo, I lifted patient booking conversion from 71% to 83%.

I’m based in Delhi NCR and available to start immediately with zero notice period.

Portfolio: https://workofhayaat.framer.website (Master CV attached).

Are you currently looking for senior product designers to collaborate on OneGraphite's product design projects?

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "theombre-email.txt": """Hi The Ombre team,

I’ve been exploring The Ombre’s work across digital brand experiences and visual systems, and I really appreciate the refined aesthetic discipline and modern typography throughout your projects.

I’m a Product & UI/UX Designer with 6+ years of experience crafting conversion-focused digital experiences, design systems, and mobile applications. At Uncover by Meddo, I created the brand foundation and visual systems, translating them across web, mobile apps, and reusable UI components. At Crevia, I designed and built responsive web platforms and over 200+ brand assets while maintaining cohesive visual hierarchy.

I’m based in Delhi NCR, available immediately (0-day notice).

You can review my live portfolio and design systems at https://workofhayaat.framer.website (CV attached).

Would love to connect if you have an open seat for a product/visual systems designer on your team.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "bsd-email.txt": """Hi Amlanjyoti,

I'm reaching out regarding UI/UX and Product Design opportunities with your team at BSD.

I’m a Product & UI/UX Designer with 6+ years of experience delivering scalable web and mobile products, design systems, and enterprise operational platforms:
• Product UX & Optimization: Redesigned multi-step ordering flows at FuelBuddy from 22 steps down to 4 (lifting completion from 62% to 78%); lifted patient booking conversion at Meddo from 71% to 83%.
• Design Systems: Built comprehensive Figma component libraries from scratch with tokenized variables, responsive auto-layout variants, and tight engineering handoff documentation.
• Domain Depth: Experience spanning B2B SaaS, mobile consumer apps, operational dashboards, healthcare workflows, and AI automation interfaces.

I’m based in Delhi NCR and available to join immediately (0-day notice).

Portfolio: https://workofhayaat.framer.website (Master CV attached).

I’d welcome the chance to connect and discuss how my design background can support your upcoming design mandates.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "reslink-email.txt": """Hi Reslink team,

I'm reaching out regarding Product Design and UI/UX Designer opportunities with your product and platform team.

I’m a Product & UI/UX Designer with 6+ years of experience designing complex digital platforms, B2B SaaS tools, and high-conversion mobile applications:
• Complex Workflow Simplification: Replaced manual operational spreadsheets at FuelBuddy with structured dispatch, asset tracking, and role-based permissions, cutting support overhead by 43%.
• Measurable UX Gains: Streamlined multi-step user flows at Meddo (71% to 83% completion) and FuelBuddy (62% to 78% order conversion).
• Design Systems Architecture: Deep Figma mastery—architecting tokenized component libraries, interactive prototypes, and developer-friendly documentation.

I am based in Delhi NCR, immediately available with zero notice period.

My portfolio is at https://workofhayaat.framer.website and my CV is attached.

Are you currently hiring product designers to help build and scale Reslink's digital platforms?

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
