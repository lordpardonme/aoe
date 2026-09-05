import sys
from pathlib import Path

emails = {
    "sap-email.txt": """Hi SAP design & product team,

Scaling design consistency across enterprise software portfolios without sacrificing component flexibility is one of the toughest challenges in enterprise UX. I have immense respect for the engineering and design governance behind SAP Fiori and the Horizon visual theme.

I’m a Product & UI/UX Designer with 6+ years specializing in enterprise design systems and complex B2B workflow software. Over the past several years, I’ve architected tokenized component architectures in Figma from the ground up, enforcing responsive auto-layout variables and strict developer handoff documentation to ensure zero UI drift across distributed engineering teams. At Maximor AI, I designed autonomous financial workflows structuring multi-tier reconciliation data into clear, accessible views.

I am eligible for the German EU Blue Card (Fachkräfteeinwanderungsgesetz) and available to relocate to Walldorf, Berlin, or Munich immediately (0-day notice).

Portfolio: https://workofhayaat.framer.website (German CV attached).

Would love to connect with your design leadership regarding product design and design systems opportunities at SAP.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "siemens-email.txt": """Hi Siemens digital product & UX team,

Industrial automation and IoT telemetry (Siemens Xcelerator / MindSphere) demand interface designs that bridge physical machinery and cloud analytics—where operators need instant anomaly detection and deep drill-down capability without cognitive overload.

I’m a Senior Product Designer with 6+ years designing IoT monitoring dashboards, fleet telemetry, and mission-critical operations software. At FuelBuddy, I designed our operational mobility platform handling real-time sensor streams, asset telemetry, and automated alert resolution across hundreds of field units in India and the UAE. My focus is always on glanceable data density, robust error recovery, and modular component design.

I hold qualification for the German EU Blue Card and am available to relocate to Munich, Nuremberg, or Erlangen with zero notice period.

You can explore my live systems work at https://workofhayaat.framer.website (CV attached in Lebenslauf format).

Are you open to product designers who can help shape industrial IoT and digital enterprise interfaces at Siemens?

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "volkswagen-email.txt": """Hi Volkswagen Group digital UX team,

The transition to software-defined vehicles is fundamentally redefining in-car user experience. Whether it’s intuitive digital instrument clusters, charging management, or over-the-air companion app ecosystems, automotive UI must deliver intelligence while prioritizing driver focus and safety.

I’m a Product & UI/UX Designer with 6+ years of experience designing automotive platforms, IoT dispatch tools, and companion mobile apps. I designed FuelBuddy’s mobile and web platforms across India and UAE, structuring live GPS route tracking, automated vehicle authorizations, and wallet spend controls into effortless, high-trust flows.

I’m based in India, EU Blue Card eligible, and available to relocate to Wolfsburg, Berlin, or Munich immediately (0-day notice).

Portfolio: https://workofhayaat.framer.website (German CV attached).

I’d welcome the chance to speak with your design and product leads regarding UI/UX opportunities within Volkswagen Group’s digital and in-cabin teams.

Best,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "infineon-email.txt": """Hi Infineon digital experience team,

As semiconductor architectures power the future of decarbonization, automotive electronics, and smart IoT, developer-facing evaluation tools and digital configuration platforms need to match the world-class precision of Infineon’s hardware.

I’m a Product Designer who specializes in technical B2B platforms, data-dense dashboards, and modular design systems. Over the past 6 years, I’ve built complete Figma component token systems and designed complex telemetry interfaces that translate technical parameters into clear, intuitive interaction patterns. At Maximor AI, I designed automation platforms structuring complex AI calculation models into transparent, reviewable flows.

I am eligible for the German EU Blue Card and available to relocate to Munich/Neubiberg immediately with 0-day notice.

Portfolio: https://workofhayaat.framer.website (German-standard CV attached).

Would love to learn if Infineon is looking for product designers to elevate digital customer tools and software platforms.

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
