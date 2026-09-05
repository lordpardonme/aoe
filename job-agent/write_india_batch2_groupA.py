import sys
from pathlib import Path

emails = {
    "artgripper-email.txt": """Hi Artgripper Studio team,

I’ve been admiring Artgripper's bold visual identity work and conceptual branding projects. Creating distinct brand worlds that stand out in crowded feeds requires sharp art direction, strong typography, and obsessive craft.

I’m a Creative Director & Visual Designer with 6+ years of experience across visual branding, art direction, and digital product design:
• Visual Craft & Brand Systems: Built complete brand identities, high-impact motion graphics, and visual design assets across commercial and D2C brands.
• Cross-Disciplinary Range: Directing commercial films, brand photography, and conceptual visual campaigns alongside digital UI/UX.
• Shipped Execution: Delivered 200+ brand assets, campaign creatives, and responsive digital brand touchpoints.

I’m based in Delhi NCR, available immediately (0-day notice).

Portfolio: https://workofhayaat.framer.website
Showreel & Films: https://drive.google.com/drive/folders/1bE_C_D3C_5k1P6s5p1t4H9V5H8h3X6mJ

Attached is my Master Creative CV. Would love to collaborate on upcoming visual design and branding projects with Artgripper.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "artiumacademy-email.txt": """Hi Priya & Pallav,

Teaching music and creative arts online is all about visual rhythm, dynamic video production, and high-energy learning content that keeps students engaged from lesson one.

I’m a Creative Producer, Video Director & Product Designer with 6+ years of experience crafting high-retention video content, music films, and interactive learning platforms:
• Video Production & Direction: Directed and edited 50+ commercial films, short-form reels, and educational visual stories with dynamic pacing and sound design.
• EdTech Product Experience: Led catalog and course discovery design at AcadPlaza, boosting course enrollments by 18% QoQ.
• Creative & Visual Systems: Complete workflow in Adobe Premiere Pro, After Effects, DaVinci Resolve, and Figma.

I’m based in Delhi NCR and available to start immediately with zero notice period.

Portfolio: https://workofhayaat.framer.website
Film & Video Showreel: https://drive.google.com/drive/folders/1bE_C_D3C_5k1P6s5p1t4H9V5H8h3X6mJ

Attached is my Master Creative CV. I’d love to explore creative production or visual content roles with Artium Academy.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "asapmedia-email.txt": """Hi ASAP Media team,

In fast-paced commercial video production and social-first brand campaigns, turnaround speed can never compromise cinematographic framing, punchy editorial pacing, and sound design.

I’m a Video Director, Editor & Creative Lead with 6+ years delivering high-impact video campaigns, commercial reels, and brand films:
• End-to-End Production: Pre-production scripting, camera direction/DOP, multi-cam editing, color grading (DaVinci Resolve), and motion graphics (After Effects).
• Social & Short-Form Mastery: Directed and edited high-velocity vertical reels and campaign hero films generating hundreds of thousands of organic views.
• Hybrid Capability: Combining cinematic video storytelling with visual brand identity systems.

I’m based in Delhi NCR and available immediately (0-day notice).

Film & Video Work: https://drive.google.com/drive/folders/1bE_C_D3C_5k1P6s5p1t4H9V5H8h3X6mJ
Portfolio: https://workofhayaat.framer.website

Attached is my Master Creative CV. Are you currently taking on freelance or full-time video editors / creative producers for upcoming ASAP Media shoots?

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "byondstudio-email.txt": """Hi Byond Studio team,

I’ve been following Byond Studio's work across 3D visual storytelling, interactive branding, and motion design—the level of spatial depth and textural craft is fantastic.

I’m a Creative Lead & Visual Designer with 6+ years of experience across art direction, motion design, video production, and digital products:
• Multi-Disciplinary Direction: Directed visual campaigns, brand films, and 3D-integrated web experiences from moodboards to final post-production.
• Motion & Visual Craft: Hands-on expertise across After Effects, Premiere Pro, DaVinci Resolve, and Figma.
• Systemic Execution: Bridging bold visual aesthetics with structured digital design systems.

I’m based in Delhi NCR and available to collaborate immediately with zero notice period.

Visual Portfolio: https://workofhayaat.framer.website
Films & Motion Showreel: https://drive.google.com/drive/folders/1bE_C_D3C_5k1P6s5p1t4H9V5H8h3X6mJ

Attached is my Master Creative CV. Would love to connect and see how I can support Byond Studio’s creative engagements.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "jaaniscafe-email.txt": """Hi Jaani's Cafe team,

In hospitality and specialty cafes, great social content isn't just about showing food—it's about capturing the morning light, the sound of espresso extraction, the texture of the space, and the human vibe that makes people walk through your doors.

I’m a Creative Director, Filmmaker & Photographer based in Delhi NCR. Over the past 6+ years, I’ve shot and directed commercial brand films, architectural spaces, and high-aesthetic social reels that drive footfall and brand affinity.

I would love to produce a dedicated set of 3 high-craft vertical reels and photography for Jaani’s Cafe capturing your menu, ambiance, and community.

Film & Photography Work: https://drive.google.com/drive/folders/1bE_C_D3C_5k1P6s5p1t4H9V5H8h3X6mJ
Portfolio: https://workofhayaat.framer.website

Attached is my Master Creative CV. I’m available to shoot in person right away.

Warm regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "littlegreenstudio-email.txt": """Hi Little Green Studio team,

I love Little Green Studio’s thoughtful visual storytelling, delicate illustrations, and conscious brand design language. It’s rare to find studios that balance organic warmth with rigorous design execution.

I’m a Visual Designer, Art Director & Filmmaker with 6+ years of experience across brand identity, editorial design, and visual storytelling:
• Brand Systems & Typography: Created complete visual identity packages, packaging graphics, and digital brand collateral with distinct emotional resonance.
• Visual Storytelling: Combining photography, film direction, and graphic design to tell authentic stories.
• Tools & Craft: Advanced proficiency in Figma, Adobe Illustrator, Photoshop, InDesign, and Premiere Pro.

I’m based in Delhi NCR and available immediately (0-day notice).

Portfolio: https://workofhayaat.framer.website (Master Creative CV attached).
Showreel: https://drive.google.com/drive/folders/1bE_C_D3C_5k1P6s5p1t4H9V5H8h3X6mJ

Would love to connect and explore how I can collaborate with Little Green Studio on upcoming brand design and storytelling mandates.

Best regards,
Mohd Hayaat Ali
+91-7905194153
hayaat0806@gmail.com
""",

    "lovedwell-email.txt": """Hi Lovedwell team,

In modern D2C lifestyle and wellness brands, visual consistency across packaging, social feeds, and digital storefronts is what turns first-time scrollers into loyal repeat customers.

I’m a Visual Designer & Creative Lead with 6+ years of experience building high-conversion D2C brand assets, lifestyle reels, and digital web experiences:
• Brand & Social Visuals: Designed 200+ marketing creatives, product launch campaigns, and high-retention short-form video content.
• E-Commerce UX: Redesigned commercial ordering funnels from 22 steps to 4 at FuelBuddy, boosting checkout conversion from 62% to 78%.
• Creative Direction: Directing product photography, lifestyle video, and cohesive graphic design systems.

I’m based in Delhi NCR and available to start immediately (0-day notice).

Portfolio: https://workofhayaat.framer.website
Visual & Video Work: https://drive.google.com/drive/folders/1bE_C_D3C_5k1P6s5p1t4H9V5H8h3X6mJ

Attached is my Master Creative CV. Would love to discuss creative collaboration opportunities for Lovedwell’s brand and digital content.

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
