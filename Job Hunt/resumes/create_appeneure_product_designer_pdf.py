from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_Product_Designer_Appeneure.pdf")

INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#155E75")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=23, leading=26, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.4, leading=13.1, textColor=ACCENT, spaceAfter=4),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.65, leading=11.1, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.8, leading=13.0, textColor=ACCENT, spaceBefore=6.2, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.45, leading=11.05, textColor=INK, spaceAfter=2.0),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.1, leading=11.0, textColor=INK, spaceBefore=3.0),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=8.05, leading=9.8, textColor=MUTED, spaceAfter=1.6),
    "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=7.95, leading=10.55, leftIndent=12, firstLineIndent=-8, spaceAfter=1.25, textColor=INK),
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
p("PRODUCT DESIGNER | VISUAL CRAFT, HERO SCREENS &amp; SHIPPED MOBILE APPS", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Available on-site in Noida", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
p("<b>Product designer with 6+ years of experience</b> turning ideas into pixel-perfect, shipped experiences across mobile apps, web products, and brand-led work. I design the hero screens people remember and the invisible flows they never notice, then carry the same visual system through to launch. I have taken products from concept to store listing on Android and web, built three design systems from scratch, and currently work across multiple client brands producing UI, motion, video, and campaign visuals to short deadlines.")

sec("Core Skills")
p("<b>Visual and Interface Craft:</b> High-fidelity UI, hero and landing screens, typography, colour and layout systems, iconography, brand-led product visuals, pixel-level polish, design QA")
p("<b>Motion and Creative Tooling:</b> Figma, FigJam, Framer, Rive, Adobe After Effects, Photoshop, Illustrator, Wix, Adobe XD, Miro")
p("<b>Product and UX:</b> User flows, information architecture, wireframing, interaction design, prototyping, usability testing, responsive web and mobile, onboarding and discovery journeys, developer handoff")
p("<b>AI in Design:</b> Actively exploring AI-assisted design and prototyping tooling, including Figma's AI features, as part of day-to-day workflow experimentation")

sec("Professional Experience")
role("Creative Designer | Crevia", "Delhi NCR, India | Jun 2026 - Present", [
    "Produce graphics, motion and video edits, social content, product imagery, and website assets across brands including Mymy, Al Yamin, Klay Consultants, and ATK Shoe Manufacturer, working to short delivery cycles.",
    "Design and build the Mymy perfume-brand website in Wix end to end, covering responsive page structure, product presentation, visual direction, and launch-ready assets.",
    "Hold visual consistency across web, product, and social touchpoints while switching between brand systems daily.",
])
role("Product Designer | I-DOD", "New Delhi, India | Jul 2025 - Mar 2026", [
    "Designed onboarding, verification, profile creation, and matching journeys for an early-stage relationship platform, working directly with founders on ambiguous, fast-moving requirements.",
    "Built the design system from scratch with reusable Figma components, variants, interaction patterns, and implementation-ready documentation.",
    "Translated concept-stage ideas into user flows, prototypes, and high-fidelity interfaces ready for engineering handoff.",
])
role("Product Designer | FuelBuddy", "Gurgaon, India | Jul 2023 - Jun 2024", [
    "Redesigned diesel ordering from a 20-22 step journey into a focused location, quantity, schedule, and payment flow, improving completion from 62% to 78%.",
    "Designed customer, FMS, pilot, and driver mobile apps across India and UAE, all shipped and publicly listed on the Play Store.",
    "Reduced payment transaction errors by 38% through wallet improvements, delegated access, and configurable spend limits.",
    "Built the FuelBuddy design system from scratch and held visual consistency across consumer, B2B, franchise, and field products.",
])
role("Product Designer | Uncover by Meddo", "Gurgaon, India | Mar 2022 - May 2023", [
    "Created Uncover's logo and brand foundation during the Meddo-to-Uncover transition, then carried that identity into the app, website, and reusable UI patterns.",
    "Reduced appointment booking from six steps to four, improving completion from 71% to 83% over eight weeks.",
    "Redesigned doctor profiles, increasing profile views by 28% and appointment requests by 15% in a 5,000-user A/B test.",
    "Conducted usability testing with 12 patients and 8 doctors and fed findings into product and design-system priorities.",
])
role("UI Designer | AcadPlaza", "Remote | Jun 2020 - Mar 2022", [
    "Redesigned course catalog and search for a learning marketplace, increasing enrollments by 18% quarter over quarter.",
    "Created responsive web and mobile interfaces, wireframes, and reusable component patterns with an eight-person product and engineering team.",
])

sec("Selected Live Work")
bullet('<b>Portfolio:</b> <link href="https://workofhayaat.framer.website" color="#155E75">workofhayaat.framer.website</link>')
bullet('<b>Kama Capital:</b> Multi-asset trading website with conversion-led onboarding and a strong visual system. <link href="https://kama-capital.com/" color="#155E75">kama-capital.com</link>')
bullet('<b>Maximor AI:</b> Conversion-focused CFO offer page for an AI finance-automation platform. <link href="https://www.maximor.ai/cfo-offer-all" color="#155E75">maximor.ai/cfo-offer-all</link>')
bullet('<b>Uncover:</b> Consumer discovery, booking, and membership journeys; identity and product design. <link href="https://uncover.co.in/" color="#155E75">uncover.co.in</link>')
bullet('<b>FuelBuddy Android App:</b> Shipped consumer ordering and tracking experience. <link href="https://play.google.com/store/apps/details?id=in.fuelbuddy.app&amp;hl=en_IN" color="#155E75">play.google.com/store/apps/details?id=in.fuelbuddy.app</link>')
bullet('<b>Meddo Patient App:</b> Shipped consumer healthcare mobile experience. <link href="https://play.google.com/store/apps/details?id=in.meddo.patient&amp;hl=en_IN" color="#155E75">play.google.com/store/apps/details?id=in.meddo.patient</link>')
bullet('<b>Vgen23:</b> Genetic interpretation and reporting web application. <link href="https://vgen23.com/" color="#155E75">vgen23.com</link>')
bullet('<b>TS Logix Peru:</b> Logistics website and internal warehouse-management tool. <link href="https://tslogixperu.com/" color="#155E75">tslogixperu.com</link>')

sec("Tools and Education")
p("<b>Tools:</b> Figma, FigJam, Framer, Rive, Wix, Adobe Photoshop, Illustrator, After Effects, Adobe XD, Miro, Google Analytics, Hotjar")
p("<b>BBA, Business Administration</b> | Sam Higginbottom University of Agriculture, Technology and Sciences | 2017 - 2020")

SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=.55 * inch,
    rightMargin=.55 * inch,
    topMargin=.45 * inch,
    bottomMargin=.45 * inch,
    title="Mohd Hayaat Ali - Product Designer - Appeneure",
).build(story)
print(OUT)
