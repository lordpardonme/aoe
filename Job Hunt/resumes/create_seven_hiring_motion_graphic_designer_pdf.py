from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_Motion_Graphic_Designer_Seven_Hiring.pdf")

INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#155E75")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=23, leading=26, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.2, leading=12.9, textColor=ACCENT, spaceAfter=4),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.55, leading=10.8, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.7, leading=12.8, textColor=ACCENT, spaceBefore=6.0, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.2, leading=10.65, textColor=INK, spaceAfter=1.75),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=8.9, leading=10.7, textColor=INK, spaceBefore=2.6),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=7.85, leading=9.5, textColor=MUTED, spaceAfter=1.4),
    "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=7.65, leading=10.05, leftIndent=12, firstLineIndent=-8, spaceAfter=1.0, textColor=INK),
}

story = []


def p(text, style="body"):
    story.append(Paragraph(text, styles[style]))


def sec(text):
    p(text, "section")
    story.append(HRFlowable(width="100%", thickness=.65, color=colors.HexColor("#C8D4D5"), spaceAfter=3))


def bullet(text):
    p("-&nbsp;&nbsp;" + text, "bullet")


def role(title, meta, items):
    p(title, "role")
    p(meta, "meta")
    for item in items:
        bullet(item)


p("Mohd Hayaat Ali", "name")
p("MOTION GRAPHIC DESIGNER | VIDEO EDITING, SOCIAL CONTENT, VISUAL DESIGN & UI/UX", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Open to Mumbai on-site discussion", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
p("<b>Creative Designer with 6+ years of design experience</b> across motion-led content, social media creatives, website assets, product imagery, UI/UX design, brand visuals, and digital product interfaces. Currently creating graphics, videos, product images, campaign assets, podcast edits, and web/social content across multiple brands at Crevia. Strong with Adobe After Effects, Photoshop, Illustrator, Figma, Framer, Wix, Rive, visual systems, layouts, typography, responsive composition, and design-to-production handoff. Product design background adds strength in UI/UX principles, interaction thinking, and structured visual problem solving.")

sec("Core Skills")
p("<b>Motion and Video:</b> Motion graphics, video editing, podcast editing, campaign videos, product-led content, social media reels/short-form assets, transitions, timing, visual rhythm, motion direction")
p("<b>Visual Design:</b> Social media creatives, product imagery, brand assets, layouts, typography, color, spacing, visual hierarchy, campaign systems, responsive web assets")
p("<b>2D / 3D / Interaction Adjacent:</b> 2D animation direction, UI micro-interaction thinking, Rive-based interaction work, motion-oriented interface concepts, 3D visual familiarity through digital product and campaign asset workflows")
p("<b>UI/UX Advantage:</b> Figma, user flows, wireframes, high-fidelity UI, responsive web/mobile design, interaction design, design systems, developer handoff, usability feedback")
p("<b>Tools:</b> Adobe After Effects, Adobe Photoshop, Adobe Illustrator, Figma, FigJam, Framer, Wix, Rive, Miro, Adobe XD, Google Analytics, Hotjar; AI-assisted creative exploration and production support")

sec("Professional Experience")
role("Creative Designer | Crevia", "Delhi NCR, India | Jun 2026 - Present", [
    "Create graphics, videos, social content, product imagery, website assets, and campaign material across multiple client brands and fast deadlines.",
    "Edit podcast videos, product images, and campaign content while keeping visual systems consistent across web, social, and marketing touchpoints.",
    "Design and build responsive website experiences in Wix, covering page structure, product presentation, visual direction, brand consistency, and launch-ready assets.",
    "Support brands including Mymy, Al Yamin, Klay Consultants, ATK shoe manufacturer, and other client projects with visual, web, and campaign assets.",
])
role("Product Designer | I-DOD", "New Delhi, India | Jul 2025 - Mar 2026", [
    "Translated founder and stakeholder requirements into user flows, wireframes, prototypes, high-fidelity interfaces, and practical release decisions.",
    "Built a reusable Figma design system from scratch with components, interaction patterns, UI states, and implementation-ready documentation.",
    "Designed onboarding, profile creation, verification, matching, and beta feedback journeys for an early-stage product.",
])
role("Product Designer | FuelBuddy", "Gurgaon, India | Jul 2023 - Jun 2024", [
    "Designed customer, business account, FMS, pilot, driver, and franchise experiences across India and UAE, spanning mobile apps, B2B web products, dashboards, analytics, maps, live tracking, asset management, and account controls.",
    "Redesigned diesel ordering from a 20-22 step journey into a focused location, quantity, schedule, and payment flow, improving completion from 62% to 78%.",
    "Built the FuelBuddy design system from scratch across consumer, B2B, franchise, field, and operational products.",
    "Created consistent interface patterns, visual states, and interaction-ready screens for product and engineering teams.",
])
role("Product Designer | Uncover by Meddo", "Gurgaon, India | Mar 2022 - May 2023", [
    "Reduced appointment booking from six steps to four, improving completion from 71% to 83% over eight weeks using analytics and user feedback.",
    "Redesigned doctor profiles, increasing profile views by 28% and appointment requests by 15% in a 5,000-user A/B test.",
    "Designed patient, doctor, and back-office experiences spanning discovery, appointments, lab tests, records, and early ABHA integration interfaces.",
    "Created Uncover's visual identity foundation and carried it into responsive web, mobile, and reusable UI patterns.",
])
role("UI Designer | AcadPlaza", "Remote | Jun 2020 - Mar 2022", [
    "Redesigned course catalog and search for a learning marketplace, increasing enrollments by 18% quarter over quarter.",
    "Created responsive web and mobile interfaces, wireframes, reusable components, discovery journeys, and visual UI patterns with an eight-person product, engineering, and content team.",
])

sec("Selected Work")
bullet("Portfolio: https://workofhayaat.framer.website")
bullet("Maximor AI: AI finance-operations landing page with strong website, conversion, and enterprise visual positioning. https://www.maximor.ai/offer")
bullet("TS Logix Peru: Logistics website and WMS-oriented digital experience. https://tslogixperu.com/")
bullet("FuelBuddy Customer Web App: Customer and B2B fuel-ordering/account experience across web and mobile. https://app.fuelbuddy.in/")
bullet("Kama Capital: Trading website and onboarding journeys. https://kama-capital.com/")

sec("Education")
p("<b>BBA, Business Administration</b> | Sam Higginbottom University of Agriculture, Technology and Sciences | 2017 - 2020")

SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=.55 * inch,
    rightMargin=.55 * inch,
    topMargin=.45 * inch,
    bottomMargin=.45 * inch,
    title="Mohd Hayaat Ali - Motion Graphic Designer - Seven Hiring",
).build(story)
print(OUT)
