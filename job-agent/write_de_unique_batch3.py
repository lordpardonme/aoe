import sys
from pathlib import Path

emails = {
    "adidas-email.txt": """Hi adidas digital product & UX team,

High-heat sneaker releases and mobile commerce (the adidas app / CONFIRMED) present one of the most intense stress tests in digital product design: managing peak server loads, lottery fairness, and rapid checkout without frustrating loyal creators.

I’m a Product & UI/UX Designer with 6+ years designing high-traffic mobile apps and conversion-focused checkout flows. At Meddo, I redesigned our clinical consumer booking flows from 6 steps down to 4, boosting completion from 71% to 83%. At FuelBuddy, I streamlined mobile ordering from 22 steps to 4, lifting checkout conversion from 62% to 78% across 100k+ active users.

I am eligible for the German EU Blue Card (Fachkräfteeinwanderungsgesetz) and available to relocate to Herzogenaurach or work in adidas's digital tech hubs with zero notice period.

Portfolio: https://workofhayaat.framer.website (German CV attached).

Are you looking for product designers to help craft next-generation consumer and creator experiences across adidas digital platforms?

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "bayer-email.txt": """Hi Bayer digital health & product team,

Designing digital health tools and clinical trial platforms requires deep empathy for patients under stress combined with strict regulatory precision—interfaces must build absolute trust and make complex medical data effortlessly clear.

I’m a Product Designer with 6+ years specializing in healthcare UX and clinical systems design. At Uncover by Meddo, I led end-to-end patient and doctor interface design across digital health records, diagnostic booking, and ABHA interoperability. I conducted usability testing across 12 patients and 8 clinicians, streamlining appointment booking from 6 steps to 4 and lifting completion from 71% to 83%.

I hold qualification for the German EU Blue Card and am available to relocate to Leverkusen, Berlin, or Wuppertal immediately (0-day notice).

You can review my healthcare case studies at https://workofhayaat.framer.website (CV attached in Lebenslauf format).

Would welcome the chance to discuss how my clinical UX background can support digital health initiatives at Bayer.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "exmox-email.txt": """Hi exmox team,

Mobile gaming advertising is shifting fast toward rewarded discovery, where player retention depends on clear progression loops, transparent reward redemption, and frictionless micro-interactions.

I’m a Product & UI/UX Designer with 6+ years designing gamified consumer apps, reward wallet systems, and high-conversion mobile flows. At FuelBuddy, I redesigned commercial billing and wallet controls, reducing transaction errors by 38% while streamlining user reward and redemption mechanics. I also have deep experience designing visual assets and interactive landing pages across gaming and digital consumer brands.

I’m ready to relocate to Hamburg on an EU Blue Card (immediate joiner, 0-day notice).

Portfolio: https://workofhayaat.framer.website (German-standard CV attached).

Are you looking for a product designer to help scale exmox's player-facing rewarded engagement and publisher tools?

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "truechart-email.txt": """Hi TRUECHART team,

Data visualization in enterprise BI isn't just about rendering charts—it's about cognitive speed. Applying standardized visual notation (like IBCS) inside Power BI and Qlik transforms messy reporting into immediate executive decision-making.

I’m a Product Designer who specializes in dense data visualization, analytics architectures, and design systems. Over the past 6 years, I’ve designed multi-tenant operational analytics and IoT telemetry platforms at FuelBuddy and Maximor AI, turning multi-dimensional data sets into clean, glanceable visual hierarchies. I build modular component libraries in Figma with strict variable tokenization for seamless frontend implementation.

I’m eligible for the German EU Blue Card and available to relocate to Germany or collaborate in a remote/hybrid setup immediately (0-day notice).

Portfolio: https://workofhayaat.framer.website (German CV attached).

Would love to connect on how my data visualization and design systems background can support TRUECHART's next-gen analytics extensions.

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
