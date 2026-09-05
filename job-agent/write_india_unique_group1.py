import sys
from pathlib import Path

emails = {
    "celonis-email.txt": """Hi Celonis design & product team,

Process intelligence and enterprise execution management (EMS) present a unique design challenge: turning millions of complex ERP/supply chain event logs into clear, actionable visual process graphs that non-technical leaders can immediately act upon.

I’m a Senior Product Designer with 6+ years specializing in complex B2B workflow software, data-dense dashboards, and modular design systems. At Maximor AI (https://www.maximor.ai/cfo-offer-all), I designed autonomous finance workflows that structured multi-tier reconciliation data into transparent, step-by-step decision states. At FuelBuddy, I designed enterprise operational platforms replacing chaotic spreadsheets with structured dispatch tools, cutting manual operational support by 43%.

I’m based in Delhi NCR and available to join immediately with 0-day notice (open to Bangalore on-site / hybrid).

Portfolio: https://workofhayaat.framer.website (CV attached).

Are you looking for product designers to help scale Celonis's core execution and process visualization tools in India?

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "learntube-email.txt": """Hi Shronit & Gargi,

Turning static internet content into dynamic, bite-sized interactive learning courses with AI is an incredible product challenge. In microlearning, learner retention completely depends on low cognitive friction, instant feedback loops, and intuitive course progression.

I’m a Product & UI/UX Designer with 6+ years designing consumer mobile apps, learning marketplaces, and habit-forming digital products. At AcadPlaza, I redesigned our course catalog and search discovery flows, lifting enrollments by 18% quarter-over-quarter. At Meddo, I streamlined multi-step patient booking from 6 steps down to 4, boosting conversion from 71% to 83% across 100k+ users. I build tokenized component libraries in Figma for rapid, zero-drift engineering handoff.

I’m based in Delhi NCR, available immediately (0-day notice), and would love to help craft LearnTube’s learner and creator experience.

Portfolio: https://workofhayaat.framer.website (Master CV attached).

Are you open to product designers joining the LearnTube.ai core team?

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "webveda-email.txt": """Hi Divyam,

I’ve been following WebVeda's growth in making practical career and life education accessible to millions across India. Building an ed-tech ecosystem that feels personal, high-trust, and motivating requires obsessive attention to course consumption UX, community touchpoints, and smooth checkout funnels.

I’m a Product & UI/UX Designer with 6+ years of experience designing high-converting consumer products, course marketplaces, and mobile apps. At AcadPlaza, I led the discovery and enrollment redesign that pushed course purchases up 18% QoQ. At Meddo, I redesigned customer booking journeys, lifting completion from 71% to 83% and boosting profile engagement by 28% in A/B testing.

I’m based in Delhi NCR and available to start immediately with zero notice period.

You can check out my live work and design systems at https://workofhayaat.framer.website (CV attached).

I’d love to connect and see how my product design background can support WebVeda’s student learning and course platforms.

Best,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "nikahforever-email.txt": """Hi Nikah Forever hiring team,

In community matchmaking platforms, user trust is everything. Designing onboarding journeys that handle sensitive family preferences, verified photo IDs, and profile filters requires progressive disclosure that feels respectful, safe, and intuitive.

I’m a Product & UI/UX Designer with 6+ years of experience designing mobile consumer apps, trust-critical KYC onboarding, and matching platforms. At I-DOD (an early-stage relationship platform), I designed complete onboarding, KYC verification, profile creation, and matching journeys from scratch. At FuelBuddy, I redesigned multi-step user ordering from 22 steps to 4, lifting completion rates from 62% to 78%.

I’m based in Delhi NCR, immediately available (0-day notice), and would love to contribute to Nikah Forever's mobile app and web platform experience.

My portfolio is at https://workofhayaat.framer.website and my CV is attached.

Are you currently hiring UI/UX or Product Designers for your product team?

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
