import sys
from pathlib import Path

emails = {
    "sumup-email.txt": """Hi SumUp Team,

I've been following how SumUp empowers millions of small businesses worldwide through frictionless card readers, companion point-of-sale tools, and business banking. I'm reaching out regarding Product Design opportunities with your merchant and payments teams in Berlin.

I'm a Product & UI/UX Designer with 6+ years of experience building merchant billing dashboards, wallet interfaces, and high-conversion payment flows:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Berlin or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for SumUp:
• Payment & Wallet UX: Redesigned commercial billing and wallet controls at FuelBuddy, cutting transaction errors by 38% through delegated access, secondary-user permissions, and configurable spend limits.
• Merchant & Operational Portals: Replaced complex manual billing and tracking with streamlined multi-tenant portals, saving 43% in manual customer support overhead.
• Mobile & Cross-Platform UX: Designed end-to-end mobile apps serving 100k+ users, ensuring rapid task completion and error prevention at the point of sale.
• Design Systems Architecture: Built comprehensive Figma component libraries with tokenized variables and tight engineering handoff pipelines.

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• FuelBuddy Web App: https://app.fuelbuddy.in/
• Maximor AI: https://www.maximor.ai/cfo-offer-all
• Kama Capital: https://kama-capital.com/

Attached is my Master Product Designer CV. I'd love to connect with your design leadership regarding product design roles at SumUp.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "raisin-email.txt": """Hi Raisin Team,

I've been following Raisin's growth as the premier pan-European savings and investment marketplace, breaking down cross-border banking barriers for retail and institutional depositors. I wanted to reach out regarding Product Design opportunities with your product teams in Berlin.

I'm a Product & UI/UX Designer with 6+ years of experience designing secure fintech interfaces, multi-asset portals, and compliant onboarding journeys:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Berlin or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for Raisin:
• FinTech & Cross-Border Platforms: Designed multi-asset trading interfaces for Kama Capital (kama-capital.com) and automated financial workflows for Maximor AI (maximor.ai).
• KYC & Trust-Centric Onboarding: Designed end-to-end KYC verification, profile setup, and security journeys for early-stage platforms at I-DOD and Meddo.
• Reducing Financial Errors: Reduced wallet and payment transaction failures by 38% at FuelBuddy through improved error recovery, clear state indicators, and account controls.
• Design Systems: Architected reusable Figma token systems, responsive tables, and modular financial widgets.

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• Kama Capital: https://kama-capital.com/
• Maximor AI: https://www.maximor.ai/cfo-offer-all
• FuelBuddy Web App: https://app.fuelbuddy.in/

Attached is my Master Product Designer CV. I'd welcome the chance to connect regarding product design opportunities at Raisin.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "taxfix-email.txt": """Hi Taxfix Team,

I've been following how Taxfix transforms complex German and European tax filing into a conversational, stress-free mobile experience that puts money back in people's pockets. I'm reaching out regarding Product Design opportunities with your Berlin product team.

I'm a Product & UI/UX Designer with 6+ years of experience simplifying dense multi-step regulatory journeys, complex user flows, and mobile consumer apps:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Berlin or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for Taxfix:
• Simplifying Complex Multi-Step Flows: Reduced clinical appointment journeys at Meddo from 6 steps to 4, boosting completion from 71% to 83%; simplified 22-step commercial ordering down to 4 at FuelBuddy (62% to 78% completion).
• Conversational & Guided UX: Expert in step-by-step progressive disclosure, error-tolerant form inputs, contextual tooltips, and anxiety-reducing feedback states.
• Design Systems & Micro-Interactions: Deep mastery in Figma token architectures, responsive auto-layout, and fluid mobile prototyping.
• Consumer Trust & Clarity: Experience building transparent financial summary screens and clear calculation breakdowns at Maximor AI and FuelBuddy.

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• Uncover: https://uncover.co.in/
• Meddo Patient App: https://play.google.com/store/apps/details?id=in.meddo.patient
• Maximor AI: https://www.maximor.ai/cfo-offer-all

Attached is my Master Product Designer CV. I'd love to connect on how my interaction design background can support Taxfix's mobile and web journeys.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "wolt-germany-email.txt": """Hi Wolt Germany Team,

I've been following how Wolt delivers top-tier food and quick commerce experiences across German cities, combining delightful consumer discovery with precision merchant and courier logistics. I'm reaching out regarding Product Design opportunities with your product and operations teams.

I'm a Product & UI/UX Designer with 6+ years of experience building on-demand logistics tools, live driver dispatch apps, and high-converting consumer marketplaces:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Germany or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for Wolt:
• Live On-Demand & Dispatch UX: Designed consumer on-demand fuel ordering apps and companion FMS driver tools at FuelBuddy across India and the UAE—covering live GPS tracking, route management, and proof-of-delivery.
• High-Velocity Ordering: Simplified multi-step ordering flows from 22 steps to 4, lifting checkout conversion from 62% to 78%.
• Merchant & Operational Efficiency: Replaced manual operational overhead with structured back-office tools, cutting support tickets by 43%.
• Scalable Design Systems: Built modular component libraries in Figma spanning consumer iOS/Android apps, driver mobile tools, and merchant web dashboards.

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• FuelBuddy Mobile (Play Store): https://play.google.com/store/apps/details?id=in.fuelbuddy.app
• FuelBuddy FMS: https://play.google.com/store/apps/details?id=in.fuelbuddy.fms
• Uncover: https://uncover.co.in/

Attached is my Master Product Designer CV. I'd love to connect regarding UI/UX and product design opportunities with Wolt.

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
