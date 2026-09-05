import sys
from pathlib import Path

emails = {
    "finn-email.txt": """Hi FINN Team,

I've been following FINN's mission to make driving a car as simple as ordering shoes online through transparent, all-inclusive digital car subscriptions. I'm reaching out regarding Product Design opportunities with your e-commerce, consumer, and fleet operations teams in Munich.

I'm a Product & UI/UX Designer with 6+ years of experience designing automotive platforms, fleet tracking software, and high-converting e-commerce checkouts:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Munich or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for FINN:
• Automotive & Fleet Operations: Designed complete fleet, driver, route, and IoT telemetry management tools for commercial vehicle operations at FuelBuddy across India and UAE.
• High-Trust Consumer Onboarding: Designed digital verification and subscription journeys, simplifying multi-step onboarding down to intuitive, high-conversion flows (62% to 78% order completion).
• Payment & Account Controls: Architected delegated billing, monthly recurring wallet setups, and configurable spend limits, reducing payment errors by 38%.
• Design Systems Architecture: Built cohesive, tokenized Figma component libraries for responsive web and mobile interfaces.

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• FuelBuddy Web App: https://app.fuelbuddy.in/
• FuelBuddy FMS: https://play.google.com/store/apps/details?id=in.fuelbuddy.fms
• Uncover: https://uncover.co.in/

Attached is my Master Product Designer CV. I'd love to connect on how my automotive systems background can support FINN's product teams.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "solaris-email.txt": """Hi Solaris Team,

I've been following how Solaris empowers top European brands to build proprietary financial products through its modular Banking-as-a-Service platform and API architecture. I'm reaching out regarding Product Design opportunities with your Berlin product and platform teams.

I'm a Product & UI/UX Designer with 6+ years of experience designing complex developer consoles, fintech platforms, and compliant financial journeys:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Berlin or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for Solaris:
• FinTech & Banking Platforms: Designed multi-asset trading interfaces for Kama Capital and AI finance automation tools for Maximor AI (maximor.ai).
• Security, KYC & Wallet UX: Architected payment authorization, delegated access, and wallet controls at FuelBuddy, cutting transaction errors by 38%.
• Complex B2B & Developer Workflows: Expert in turning dense API parameters, multi-tenant dashboards, and regulatory compliance into clear, modular interaction components.
• Design Systems Architecture: Built comprehensive Figma component libraries with tokenized variables, responsive data tables, and strict developer handoff.

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• Kama Capital: https://kama-capital.com/
• Maximor AI: https://www.maximor.ai/cfo-offer-all
• FuelBuddy Web App: https://app.fuelbuddy.in/

Attached is my Master Product Designer CV. I'd welcome the chance to discuss how my systems design background can support Solaris.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "forto-email.txt": """Hi Forto Team,

I've been following how Forto transforms global supply chains into a seamless digital freight experience, providing real-time shipment visibility and proactive logistics management. I'm reaching out regarding Senior Product Designer opportunities with your Berlin product team.

I'm a Product & UI/UX Designer with 6+ years of experience designing complex logistics platforms, IoT fleet dispatch tools, and enterprise operational dashboards:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Berlin or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for Forto:
• Logistics & Dispatch Tooling: Replaced manual spreadsheet-heavy operations at FuelBuddy with unified platforms for vehicles, routes, bowsers, delivery planning, and real-time status management—reducing support load by 43%.
• Real-Time Tracking & Telemetry: Designed map-based tracking, live IoT status feeds, and asset management for mission-critical logistics operations across India and UAE.
• Enterprise Dashboards & WMS: Designed warehouse and inventory management systems (WMS) for TS Logix Peru (tslogixperu.com), managing pharmaceutical distribution workflows.
• Design Systems Architecture: Deep mastery in Figma token architectures, responsive data tables, and zero-drift engineering handoff.

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• FuelBuddy Web App: https://app.fuelbuddy.in/
• FuelBuddy FMS: https://play.google.com/store/apps/details?id=in.fuelbuddy.fms
• TS Logix Peru: https://tslogixperu.com/

Attached is my Master Product Designer CV. I'd love to connect on how my logistics design experience can support Forto's product roadmap.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "distribusion-email.txt": """Hi Distribusion Team,

I've been following how Distribusion powers global intercity ground transportation, connecting major travel retailers worldwide with bus, rail, and shuttle operators through a unified B2B platform. I'm reaching out regarding Product Design opportunities with your Berlin product team.

I'm a Product & UI/UX Designer with 6+ years of experience designing complex B2B travel platforms, ticket inventory management, and multi-currency checkout funnels:

Location, Visa & Availability:
• Current Location: Delhi NCR, India (Available for on-site relocation to Berlin or remote start)
• Work Permit: EU Blue Card eligible (Fachkräfteeinwanderungsgesetz)
• Notice Period: Immediate joiner (0-day notice period)

Relevant Experience for Distribusion:
• B2B Platforms & High-Volume Booking: Redesigned multi-step commercial ordering at FuelBuddy from 22 steps to 4, lifting completion from 62% to 78%; designed responsive course discovery at AcadPlaza (+18% QoQ enrollments).
• Complex Logistics & Transit Systems: Designed fleet, route, shift, and asset management tools handling mission-critical daily operations across India and UAE.
• Global & Multilingual UX: Delivered multi-asset trading interfaces for Kama Capital and consumer web apps for FuelBuddy UAE with regional localization.
• Scalable Design Systems: Architected reusable Figma token systems, responsive tables, and modular booking widgets.

Selected Live Work:
• Portfolio: https://workofhayaat.framer.website
• FuelBuddy Web App: https://app.fuelbuddy.in/
• Kama Capital: https://kama-capital.com/
• Uncover: https://uncover.co.in/

Attached is my Master Product Designer CV. I'd welcome the chance to connect regarding product design roles at Distribusion.

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
