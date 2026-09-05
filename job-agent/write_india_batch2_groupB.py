import sys
from pathlib import Path

emails = {
    "museocamera-email.txt": """Hi Museo Camera team,

As a visual creative and photographer based in Delhi NCR, Museo Camera has always stood out to me as an incredible institution for visual history, photographic craft, and lens-based storytelling.

I’m a Photographer, Filmmaker & Visual Designer with 6+ years of experience across visual curation, exhibition media, brand films, and digital experiences:
• Photographic & Lens Craft: Deep expertise across digital cinematography, lighting, documentary photography, and visual archival work.
• Digital Media & Exhibition Content: Directing and editing high-resolution video documentaries, interactive media, and archival design assets.
• Community & Curation: Curated and hosted design and photography community workshops inside Google and Microsoft spaces.

I’m based locally in Delhi NCR / Gurgaon and available to collaborate on-site immediately.

Visual & Film Work: https://drive.google.com/drive/folders/1bE_C_D3C_5k1P6s5p1t4H9V5H8h3X6mJ
Portfolio: https://workofhayaat.framer.website

Attached is my Master Creative CV. Would love to discuss visual curation, media production, or exhibition design opportunities with Museo Camera.

Warm regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "radlvng-email.txt": """Hi RAD LVNG team,

I’ve been loving RAD LVNG’s aesthetic—the mix of modern lifestyle culture, editorial design, and vibrant visual energy is super refreshing.

I’m a Creative Lead, Visual Designer & Video Director with 6+ years of experience crafting culture-driven brand visuals, lifestyle reels, and digital experiences:
• Editorial & Visual Direction: Directed fashion/lifestyle shoots, social-first reels, and complete brand systems with punchy editorial typography.
• Motion & Video Production: Hands-on camera work, pacing, and color grading across Premiere Pro, After Effects, and DaVinci Resolve.
• Digital Platforms: Translating brand aesthetic seamlessly into responsive web interfaces and mobile digital touchpoints.

I’m based in Delhi NCR and available to start immediately (0-day notice).

Portfolio: https://workofhayaat.framer.website
Video & Film Work: https://drive.google.com/drive/folders/1bE_C_D3C_5k1P6s5p1t4H9V5H8h3X6mJ

Attached is my Master Creative CV. Would love to collaborate with RAD LVNG on upcoming visual campaigns and creative content.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "remotehub-talent-email.txt": """Hi Remotehub Talent team,

I'm reaching out to introduce myself for remote Senior Product Designer and Creative Lead opportunities in your talent network.

I’m a Senior Product Designer & Creative Director with 6+ years of experience delivering high-scale digital platforms, B2B SaaS tools, and visual brand systems:
• Shipped International Scale: Designed digital platforms serving 100k+ active users; streamlined appointment booking conversion from 71% to 83% at Meddo and commercial ordering from 62% to 78% at FuelBuddy.
• Design Systems Architecture: Advanced mastery in Figma—modular token variables, responsive component libraries, and zero-drift developer handoff.
• Creative & Visual Depth: Directing commercial brand films, motion graphics, and visual identity systems alongside digital product design.

I'm based in Delhi NCR, available for immediate remote engagement with zero notice period.

Portfolio: https://workofhayaat.framer.website
Showreel: https://drive.google.com/drive/folders/1bE_C_D3C_5k1P6s5p1t4H9V5H8h3X6mJ

Attached is my Master CV. Would welcome representation for relevant high-impact remote design mandates.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "neeraj-lead-email.txt": """Hi Neeraj,

I came across your design hiring note and wanted to share my portfolio and CV for your open Product & UI/UX Design mandates.

I’m a Senior Product & UI/UX Designer with 6+ years of experience shipping scalable digital products, SaaS dashboards, and consumer mobile apps:
• Proven UX Results: Simplified 22-step commercial ordering to 4 steps at FuelBuddy (62% to 78% completion); lifted patient booking conversion from 71% to 83% at Meddo.
• Design Systems: Architected production Figma libraries with tokenized variables, responsive auto-layout variants, and tight engineering documentation.
• Multi-Domain Range: Deep experience across logistics operations, healthcare workflows, consumer fintech, and AI automation.

I am based in Delhi NCR and available to join immediately (0-day notice).

Portfolio: https://workofhayaat.framer.website (Master Product Designer CV attached).

I’d welcome the opportunity to connect and discuss how my design background fits your current opening.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "mushroomstudios-email.txt": """Hi Mushroom Studios team,

I'm reaching out regarding Freelance and Full-Time Video Editor / Post-Production opportunities with Mushroom Studios.

I’m a Senior Video Editor, Colorist & Motion Designer with 6+ years of experience crafting high-retention commercial reels, brand films, and narrative videos:
• Editorial Pacing & Flow: Multi-camera editing, dynamic beat-syncing, sound design, and narrative flow across horizontal brand films and vertical short-form content.
• Motion & Color Mastery: Expert color grading in DaVinci Resolve, 2D motion graphics and kinetic typography in Adobe After Effects, and rapid editing in Premiere Pro.
• High Turnaround: Experienced working in fast-paced studio environments delivering polished cuts on tight deadlines.

I’m based in Delhi NCR, available immediately with full editing suite setup.

Video & Film Work: https://drive.google.com/drive/folders/1bE_C_D3C_5k1P6s5p1t4H9V5H8h3X6mJ
Portfolio: https://workofhayaat.framer.website

Attached is my Master Creative CV. Would love to take on an edit test or jump into upcoming project timelines.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "orange-agency-email.txt": """Hi Orange Corporate Solutions recruitment team,

I am reaching out to introduce myself for Senior Product Design, UI/UX, and Digital Design mandates with your enterprise and startup clients across India.

I am a Senior Product Designer with 6+ years of experience shipping scalable B2B SaaS platforms, complex logistics tools, and consumer mobile applications:
• Shipped Scale: Led UX design for platforms serving 100k+ active users; lifted patient booking conversion from 71% to 83% at Meddo and commercial ordering from 62% to 78% at FuelBuddy.
• Enterprise & Operational Systems: Replaced manual spreadsheets with unified dispatch and live telemetry at FuelBuddy, cutting operational support by 43%.
• Design Systems Architecture: Advanced mastery in Figma—tokenized variables, responsive component libraries, and clean developer handoff pipelines.

Location: Delhi NCR (Available for immediate start / 0-day notice; open to remote or hybrid).

Portfolio: https://workofhayaat.framer.website (Master Product Designer CV attached).

I would welcome representation for relevant senior design roles across your client portfolio.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "shell-consultancy-email.txt": """Hi Shell Consultancy team,

I am reaching out to submit my profile for Senior Product Design and UI/UX Designer opportunities across your corporate and tech client mandates.

I am a Product & UI/UX Designer with 6+ years of experience designing high-scale digital platforms, enterprise workflow software, and consumer mobile applications:
• Measurable UX Gains: Redesigned multi-step checkout flows at FuelBuddy (62% to 78% conversion) and clinical appointment booking at Meddo (71% to 83% completion).
• Systems & Delivery: Comprehensive mastery in Figma—modular component libraries, design tokens, and seamless engineering handoff.
• Operational Efficiency: Designed B2B dispatch and asset management tools that cut manual support overhead by 43%.

I am based in Delhi NCR and available to join immediately with zero notice period.

Portfolio: https://workofhayaat.framer.website (Master CV attached).

I would welcome the opportunity to discuss open senior design openings within your network.

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
