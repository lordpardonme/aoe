import sys
from pathlib import Path

emails = {
    "volocopter-email.txt": """Hi Volocopter design & talent team,

Urban air mobility creates an entirely new category of passenger experience—from booking a VoloCity flight to navigating the physical-digital touchpoints of a VoloPort. In an aircraft where safety and calm are paramount, the UI cannot afford ambiguity or friction.

I’m a Senior Product Designer with 6+ years designing complex mobility software, live IoT dispatch dashboards, and consumer booking apps. At FuelBuddy, I architected our field mobility platform handling real-time GPS telemetry, pilot dispatch, and automated safety workflows across India and UAE. I specialize in designing interfaces with zero cognitive clutter and airtight state management.

I’m eligible for the German EU Blue Card (Fachkräfteeinwanderungsgesetz) and available to relocate to Bruchsal or Munich immediately (0-day notice).

Portfolio: https://workofhayaat.framer.website (German-standard CV attached).

Are you currently looking for product designers to help define Volocopter's passenger booking or ground operations interfaces?

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "lufthansa-systems-email.txt": """Hi Lufthansa Systems team,

Aviation software demands ruthless reliability—whether it’s NetLine flight scheduling under irregular operations or BoardConnect in-flight passenger digital services. Every interaction must reduce pilot and crew cognitive load while keeping airline operations running on time.

I’m a Product & UI/UX Designer with 6+ years in mission-critical operations software, logistics routing, and high-volume mobile platforms. At FuelBuddy, I replaced manual spreadsheet-heavy fleet operations with structured dispatch and live asset tracking tools, cutting support tickets by 43%. I've built complete design systems from scratch in Figma with strict token governance for zero-drift engineering handoff.

I hold qualification for the German EU Blue Card and am available to relocate to Frankfurt/Raunheim with 0-day notice.

You can review my live product work at https://workofhayaat.framer.website (CV attached in Lebenslauf format).

Would welcome a conversation on how my systems design background can support digital aviation products at Lufthansa Systems.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "bmw-group-email.txt": """Hi BMW Group digital design team,

The challenge of modern in-cabin UX (BMW iDrive / Operating System 9) is finding the delicate balance between rich digital intelligence and zero driver distraction. The interaction between physical tactile controls, voice, and touchscreens requires extreme spatial and visual discipline.

I’m a Product & UI/UX Designer with 6+ years designing automotive companion apps, live IoT fleet tracking, and complex multi-modal digital experiences. I designed the consumer mobile and commercial web platforms at FuelBuddy across India and UAE, structuring dense live telemetry and automated payment workflows into effortless, glanceable interfaces.

I am based in India, EU Blue Card eligible, and available to relocate to Munich immediately with zero notice period.

My portfolio is at https://workofhayaat.framer.website and my German-standard CV is attached.

Would love to connect with your digital design leads regarding UI/UX opportunities within BMW’s digital and in-car experience teams.

Best,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "kaufland-ecommerce-email.txt": """Hi Kaufland e-commerce design team,

Running a multi-category marketplace with millions of SKUs across Germany and Central Europe means checkout conversion lives and dies on clear product taxonomy, transparent shipping timelines, and low-friction mobile purchasing.

I’m a Product Designer with 6+ years of experience optimizing high-traffic digital marketplaces and complex checkout funnels. At Meddo, I redesigned our core booking flows from 6 steps down to 4, boosting completion from 71% to 83% and lifting doctor profile views by 28% in A/B testing. At FuelBuddy, I redesigned commercial ordering from 22 steps to 4, increasing order conversion from 62% to 78%.

I am eligible for the German EU Blue Card and available to relocate to Cologne or work in a hybrid setup immediately (0-day notice).

Portfolio: https://workofhayaat.framer.website (German CV attached).

Are you looking for product designers to help optimize buyer conversion or seller portal experiences at Kaufland e-commerce?

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
