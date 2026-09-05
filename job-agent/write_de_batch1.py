import sys
from pathlib import Path

emails = {
    "deepl-email.txt": """Hi DeepL Team,

I've been following DeepL's expansion from precision machine translation into enterprise AI communication and writing tools. I wanted to reach out regarding Product Design and UI/UX Designer opportunities with your product and design teams in Germany.

I'm a Product & UI/UX Designer with 6+ years of experience designing complex B2B SaaS tools, AI automation interfaces, and high-scale consumer applications:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Germany or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz / Skilled Immigration)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for DeepL:
• AI & B2B Product Interfaces: Designed AI financial automation workflows for Maximor AI (maximor.ai), structuring multi-step autonomous close and reconciliation tasks into clear, trust-building interaction patterns.
• Design Systems & Token Architecture: Deep Figma mastery—architecting tokenized component libraries, auto layout variables, responsive grids, and zero-drift developer handoff.
• High-Impact UX Optimization: Redesigned core clinical appointment journeys at Meddo, lifting conversion from 71% to 83%; streamlined FuelBuddy ordering from 22 steps to 4, boosting completion from 62% to 78%.
• Complex Multi-Language UX: Delivered multi-asset trading interfaces for Kama Capital with dual English/Arabic considerations.

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• Maximor AI: https://www.maximor.ai/cfo-offer-all
• FuelBuddy Web App: https://app.fuelbuddy.in/
• Kama Capital: https://kama-capital.com/

Attached is my Master Product Designer CV (Lebenslauf format). I'd welcome the chance to connect with your design leadership regarding product design roles at DeepL.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "blinkist-email.txt": """Hi Blinkist Team,

I've long admired how Blinkist distills dense ideas into engaging, bite-sized microlearning formats across audio and text. I'm reaching out regarding Product Design and UX opportunities with your mobile and content experience teams in Berlin.

I'm a Product & UI/UX Designer with 6+ years of experience crafting consumer mobile apps, learning marketplaces, and habit-forming digital experiences:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Berlin or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for Blinkist:
• Consumer Engagement & Conversion: Redesigned patient appointment flows at Meddo, lifting booking conversion from 71% to 83%; redesigned course catalog and discovery for AcadPlaza, increasing enrollments by 18% QoQ.
• Content & Mobile Discovery: Designed intuitive reading and audio consumption flows, user onboarding paths, and personalized recommendations across mobile apps serving 100k+ users.
• Polished Interaction Craft: Deep Figma design systems expertise, interactive micro-prototypes, typography hierarchy for readability, and tight cross-functional collaboration with mobile engineering.
• Community Building: Curated and hosted design community sessions inside Google and Microsoft offices during a 2024–2025 sabbatical.

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• Uncover: https://uncover.co.in/
• FuelBuddy Mobile (Play Store): https://play.google.com/store/apps/details?id=in.fuelbuddy.app
• Meddo Patient App: https://play.google.com/store/apps/details?id=in.meddo.patient

Attached is my Master Product Designer CV. I'd love to connect on how I can contribute to Blinkist's reader and audio engagement journeys.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "personio-email.txt": """Hi Personio Team,

I've been closely following Personio's evolution into Europe's leading HR operating system and your focus on People Workflow Automation. I'm reaching out regarding Senior Product Designer opportunities across your Munich and Berlin product hubs.

I'm a Product & UI/UX Designer with 6+ years of experience designing complex multi-tenant B2B SaaS platforms, enterprise workflow automation, and operational dashboards:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Munich/Berlin or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for Personio:
• Complex Workflow Automation: Replaced spreadsheet-heavy operational workflows at FuelBuddy with structured dispatch, asset tracking, and role-based access tools, reducing manual support input by 43%.
• Measurable Journey Improvements: Redesigned multi-step checkout and appointment flows at Meddo (71% to 83% completion) and FuelBuddy (62% to 78% order completion).
• Permissions & Multi-Tenant Controls: Architected delegated access, secondary-user permissions, and configurable spend limits, cutting financial transaction errors by 38%.
• Design System Architecture: Built complete design systems from scratch in Figma with tokenized variables, component libraries, and seamless engineering handoff.

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• FuelBuddy Web App: https://app.fuelbuddy.in/
• Maximor AI: https://www.maximor.ai/cfo-offer-all
• Uncover: https://uncover.co.in/

Attached is my Master Product Designer CV. I'd welcome the opportunity to discuss how my systems design background can support Personio's product teams.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "getyourguide-email.txt": """Hi GetYourGuide Team,

I've been following how GetYourGuide continues to redefine travel experiences globally, pairing rich discovery with high-converting booking funnels. I'm reaching out regarding Product Design opportunities with your experience, marketplace, or booking teams in Berlin.

I'm a Product & UI/UX Designer with 6+ years of experience optimizing high-traffic consumer booking journeys, mobile marketplaces, and location-based discovery:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Berlin or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for GetYourGuide:
• Funnel & Conversion Optimization: Redesigned clinical appointment booking at Meddo from 6 steps to 4, lifting completion from 71% to 83% via A/B testing and user research; increased doctor profile views by 28%.
• Location & Map-Based UX: Designed real-time tracking, live map interfaces, and location-based asset discovery at FuelBuddy across web and mobile.
• Global & Multilingual Consideration: Designed cross-border platforms for Kama Capital and FuelBuddy UAE, accounting for multi-currency and regional user behaviors.
• Scalable Design Systems: Architected reusable Figma token systems, responsive mobile/web components, and cross-functional QA handoff.

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• Uncover: https://uncover.co.in/
• FuelBuddy UAE: https://fuelbuddy.ae/
• Meddo Patient App: https://play.google.com/store/apps/details?id=in.meddo.patient

Attached is my Master Product Designer CV. I'd love to connect with your product design team in Berlin.

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
