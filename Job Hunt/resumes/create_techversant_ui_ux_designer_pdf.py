from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_UI_UX_Designer_Techversant.pdf")

INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#155E75")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=23, leading=26, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.2, leading=12.9, textColor=ACCENT, spaceAfter=4),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.45, leading=10.8, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.7, leading=12.8, textColor=ACCENT, spaceBefore=6.0, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.25, leading=10.75, textColor=INK, spaceAfter=1.8),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=8.95, leading=10.8, textColor=INK, spaceBefore=2.8),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=7.9, leading=9.6, textColor=MUTED, spaceAfter=1.5),
    "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=7.72, leading=10.25, leftIndent=12, firstLineIndent=-8, spaceAfter=1.1, textColor=INK),
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
p("UI/UX DESIGNER | WEB, MOBILE, FIGMA SYSTEMS, MOTION & DEVELOPER HANDOFF", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Open to Trivandrum / Cochin relocation or hybrid discussion", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
p("<b>UI/UX Designer with 6+ years of hands-on experience</b> designing user-centered web and mobile products, responsive interfaces, interaction flows, prototypes, visual systems, and developer-ready handoffs. Strong in Figma, FigJam, Auto Layout, components, design systems, Adobe Illustrator, After Effects, motion-oriented visual work, usability testing, and cross-functional collaboration with product, engineering, marketing, and founders. Experienced across healthcare, logistics, fintech-adjacent products, education/learning, B2B platforms, dashboards, internal tools, and customer-facing apps.")

sec("Core Skills")
p("<b>UX and Product Design:</b> User research, user journeys, journey maps, information architecture, user flows, wireframes, high-fidelity UI, interaction design, usability testing, product iteration, stakeholder feedback")
p("<b>Visual, Motion and UI Craft:</b> Typography, layout, color, spacing, visual hierarchy, illustration support, micro-interaction thinking, UI animation direction, gamified flow patterns, responsive composition")
p("<b>Figma and Design Systems:</b> Figma, FigJam, Auto Layout, reusable components, variants, UI states, design-system documentation, accessibility awareness, platform-specific iOS/Android patterns")
p("<b>Delivery and Collaboration:</b> Developer handoff, design QA, HTML/CSS collaboration basics, responsive web/mobile specifications, cross-functional work with product, engineering, marketing, and client stakeholders")
p("<b>Tools:</b> Figma, FigJam, Adobe Illustrator, Adobe After Effects, Photoshop, Framer, Wix, Rive, Miro, Adobe XD, Google Analytics, Hotjar")

sec("Professional Experience")
role("Creative Designer | Crevia", "Delhi NCR, India | Jun 2026 - Present", [
    "Create graphics, videos, social content, product imagery, website assets, and campaign material across multiple client brands and fast deadlines.",
    "Design and build responsive website experiences in Wix, covering page structure, product presentation, visual direction, brand consistency, and launch-ready assets.",
    "Edit podcast videos, product images, and campaign content while keeping visual systems consistent across web, social, and marketing touchpoints.",
])
role("Product Designer | I-DOD", "New Delhi, India | Jul 2025 - Mar 2026", [
    "Translated ambiguous founder and stakeholder requirements into user flows, wireframes, prototypes, high-fidelity interfaces, and practical release decisions.",
    "Built a reusable Figma design system from scratch with components, interaction patterns, states, and implementation-ready documentation.",
    "Designed onboarding, profile creation, verification, matching, and beta feedback journeys for an early-stage product.",
    "Collaborated with stakeholders and developers to clarify requirements, refine flows, and prepare screens for build handoff.",
])
role("Product Designer | FuelBuddy", "Gurgaon, India | Jul 2023 - Jun 2024", [
    "Designed customer, business account, FMS, pilot, driver, and franchise experiences across India and UAE, spanning mobile apps, B2B web products, dashboards, analytics, maps, live tracking, asset management, and account controls.",
    "Redesigned diesel ordering from a 20-22 step journey into a focused location, quantity, schedule, and payment flow, improving completion from 62% to 78%.",
    "Reduced payment transaction errors by 38% through wallet improvements, delegated access, secondary-user controls, and configurable spend limits.",
    "Built the FuelBuddy design system from scratch across consumer, B2B, franchise, field, and operational products.",
    "Replaced spreadsheet-heavy operational patterns with structured workflows for drivers, trucks, routes, shifts, delivery planning, corrections, and reporting.",
])
role("Product Designer | Uncover by Meddo", "Gurgaon, India | Mar 2022 - May 2023", [
    "Reduced appointment booking from six steps to four, improving completion from 71% to 83% over eight weeks using analytics and user feedback.",
    "Redesigned doctor profiles, increasing profile views by 28% and appointment requests by 15% in a 5,000-user A/B test.",
    "Designed patient, doctor, and back-office experiences spanning discovery, appointments, lab tests, records, and early ABHA integration interfaces.",
    "Conducted usability testing with 12 patients and 8 doctors, translating findings into product, design-system, and engineering priorities.",
])
role("UI Designer | AcadPlaza", "Remote | Jun 2020 - Mar 2022", [
    "Redesigned course catalog and search for a learning marketplace, increasing enrollments by 18% quarter over quarter.",
    "Created responsive web and mobile interfaces, wireframes, reusable components, and discovery journeys with an eight-person product, engineering, and content team.",
])

sec("Selected Work")
bullet("Portfolio: https://workofhayaat.framer.website")
bullet("FuelBuddy Customer Web App: Responsive customer and B2B fuel-ordering/account experience across web and mobile. https://app.fuelbuddy.in/")
bullet("Uncover / Meddo: Healthcare product UX, booking flows, patient experience, usability testing, and design-system work. https://uncover.co.in/")
bullet("Vgen23: Web-based genetic interpretation and reporting platform for complex clinical workflows. https://vgen23.com/")
bullet("TS Logix Peru: Logistics website and internal WMS work covering inventory and operational workflows. https://tslogixperu.com/")
bullet("Kama Capital: Multi-asset trading website and onboarding journeys. https://kama-capital.com/")

sec("Education")
p("<b>BBA, Business Administration</b> | Sam Higginbottom University of Agriculture, Technology and Sciences | 2017 - 2020")

SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=.55 * inch,
    rightMargin=.55 * inch,
    topMargin=.45 * inch,
    bottomMargin=.45 * inch,
    title="Mohd Hayaat Ali - UI UX Designer - Techversant",
).build(story)
print(OUT)
