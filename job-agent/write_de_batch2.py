import sys
from pathlib import Path

emails = {
    "flix-email.txt": """Hi Flix Team,

I've been following how Flix continues to scale green, affordable mobility across Europe, connecting millions through smart scheduling, dynamic routing, and seamless booking. I'm reaching out regarding Product Design opportunities with your passenger and operations teams across Munich and Berlin.

I'm a Product & UI/UX Designer with 6+ years of experience building complex fleet logistics software, dispatch dashboards, and high-volume mobile booking experiences:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Munich/Berlin or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for Flix:
• Fleet Operations & Dispatch Systems: Replaced spreadsheet-heavy fleet operations at FuelBuddy with integrated driver, vehicle, shift, route planning, and live IoT tracking tools—reducing manual support load by 43%.
• Multi-Modal Booking & Checkout: Redesigned multi-step ordering from 22 steps to 4, boosting checkout completion from 62% to 78%; designed map-based live vehicle tracking for drivers and consumers.
• Multi-Country Scale: Shipped web and mobile products operating across diverse regional requirements in India and the UAE.
• Design Systems: Built comprehensive Figma component libraries, auto-layout tokens, and rigorous engineering handoff pipelines.

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• FuelBuddy Web App: https://app.fuelbuddy.in/
• FuelBuddy FMS: https://play.google.com/store/apps/details?id=in.fuelbuddy.fms
• Uncover: https://uncover.co.in/

Attached is my Master Product Designer CV. I'd love to connect on how my operations and mobility design background can support Flix's product roadmap.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "contentful-email.txt": """Hi Contentful Team,

I've been a close follower of Contentful's leadership in composable content platforms and how your design system powers flexible, developer-friendly editorial canvases. I'm reaching out regarding Product Design opportunities with your product and design systems teams in Berlin.

I'm a Product & UI/UX Designer with 6+ years of experience architecting complex enterprise SaaS interfaces, developer handoff frameworks, and modular design systems:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Berlin or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for Contentful:
• Design Systems & Token Governance: Architected comprehensive Figma component libraries with tokenized variables, nested component logic, auto-layout variants, and clear developer documentation.
• Complex B2B Canvases & Workflows: Designed complex operations platforms and automated financial workflows for Maximor AI (maximor.ai), structuring dense data tables and multi-state workflows into clear hierarchy.
• Cross-Functional Collaboration: Deep experience partnering directly with front-end engineers to ensure zero design drift across React/web implementations.
• Measurable UX Craft: Redesigned complex workflows at Meddo (71% to 83% completion) and FuelBuddy (62% to 78% order completion).

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• Maximor AI: https://www.maximor.ai/cfo-offer-all
• FuelBuddy Web App: https://app.fuelbuddy.in/
• Uncover: https://uncover.co.in/

Attached is my Master Product Designer CV. I'd welcome the chance to speak with your design leadership regarding product design roles at Contentful.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "choco-email.txt": """Hi Choco Team,

I've been following Choco's mission to digitize the global food supply chain and eliminate food waste through intuitive ordering tools for restaurants and suppliers. I'm reaching out regarding Senior Product Designer opportunities with your Berlin product team.

I'm a Product & UI/UX Designer with 6+ years of experience designing fast-paced B2B ordering interfaces, supplier portals, and inventory/dispatch tools:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Berlin or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for Choco:
• High-Velocity B2B Ordering: Redesigned complex commercial fuel ordering at FuelBuddy from 22 steps down to 4, lifting ordering conversion from 62% to 78%.
• Supplier & Fleet Tooling: Replaced manual operational spreadsheets with unified tools for dispatch, inventory quantity correction, shift management, and automated ticketing.
• Mobile & Field Optimization: Designed companion mobile apps for drivers, pilots, and field operators, ensuring flawless usability in high-distraction, time-critical environments.
• Design Systems Architecture: Built cohesive, tokenized Figma component libraries bridging consumer web, field mobile, and back-office management.

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• FuelBuddy Web App: https://app.fuelbuddy.in/
• FuelBuddy FMS: https://play.google.com/store/apps/details?id=in.fuelbuddy.fms
• Uncover: https://uncover.co.in/

Attached is my Master Product Designer CV. I'd love to connect on how my B2B workflow and mobile experience can support Choco's product goals.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "adjust-email.txt": """Hi Adjust Team,

I've been following Adjust's role as a cornerstone of mobile measurement, attribution, and analytics for global app publishers. I wanted to reach out regarding Product Design opportunities with your product and reporting teams across Berlin and Munich.

I'm a Product & UI/UX Designer with 6+ years of experience designing data-dense B2B dashboards, multi-metric analytics tools, and scalable design systems:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Berlin/Munich or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for Adjust:
• Complex Data Visualization & Dashboards: Designed multi-tenant operational analytics, live IoT telemetry, and financial reporting dashboards at FuelBuddy and Maximor AI.
• Information Hierarchy & Density: Deep experience organizing multi-dimensional datasets, filter logic, export states, and drill-down views without cluttering cognitive load.
• Design Systems at Scale: Architected comprehensive tokenized component systems in Figma, ensuring design parity across web platforms and mobile apps.
• Conversion & UX Impact: Streamlined complex multi-step workflows at Meddo (71% to 83% completion) and reduced transaction errors at FuelBuddy by 38%.

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• Maximor AI: https://www.maximor.ai/cfo-offer-all
• FuelBuddy Web App: https://app.fuelbuddy.in/
• Kama Capital: https://kama-capital.com/

Attached is my Master Product Designer CV. I'd welcome the chance to connect regarding UI/UX and product design roles at Adjust.

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
