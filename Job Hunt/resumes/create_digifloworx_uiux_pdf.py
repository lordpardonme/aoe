from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_UI_UX_Designer_DigiFloworx.pdf")

INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#1E5A78")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=22, leading=25, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.7, leading=13, textColor=ACCENT, spaceAfter=3),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.35, leading=10.5, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.8, leading=13, textColor=ACCENT, spaceBefore=6, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.26, leading=10.7, textColor=INK, spaceAfter=2),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.05, leading=10.8, textColor=INK, spaceBefore=3),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=7.85, leading=9.4, textColor=MUTED, spaceAfter=1.4),
    "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=7.86, leading=10.15, leftIndent=11, firstLineIndent=-7, spaceAfter=1.25, textColor=INK),
}

story = []


def p(text, style="body"):
    story.append(Paragraph(text, styles[style]))


def sec(text):
    p(text, "section")
    story.append(HRFlowable(width="100%", thickness=0.55, color=colors.HexColor("#C7D2DC"), spaceAfter=2.4))


def bullet(text):
    p("-&nbsp;&nbsp;" + text, "bullet")


def role(title, meta, items):
    p(title, "role")
    p(meta, "meta")
    for item in items:
        bullet(item)


p("Mohd Hayaat Ali", "name")
p("UI/UX DESIGNER | WEB, MOBILE AND DESIGN SYSTEMS", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Open to remote, hybrid, or on-site opportunities", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
story.append(Spacer(1, 3))
p("<b>UI/UX and Product Designer with 6+ years of experience</b> designing responsive web products, mobile apps, B2B platforms, internal tools, and reusable design systems. Strong in turning real client and product requirements into user flows, wireframes, prototypes, high-fidelity UI, and developer-ready handoff. I bring proven work across healthcare, logistics, fintech-adjacent products, marketplaces, and brand-led digital projects, along with a portfolio of shipped and client-facing work.")

sec("Core Skills")
p("<b>UI/UX:</b> User flows, information architecture, wireframing, interaction design, responsive web and mobile UI, prototyping, usability testing, design thinking, stakeholder communication")
p("<b>Systems and Delivery:</b> Figma, FigJam, Auto Layout, reusable components, design systems, design QA, developer handoff, client revisions, cross-functional collaboration")
p("<b>Visual and Digital Product Work:</b> Website mockups, landing pages, dashboards, content-led UI, brand-led digital experiences, design polishing, layout systems, typography, visual hierarchy")

sec("Professional Experience")
role("Creative Designer | Crevia", "Delhi NCR, India | Jun 2026 - Present", [
    "Create graphics, videos, social content, product imagery, website assets, and campaign material across multiple client brands and deadlines.",
    "Design and build responsive website experiences in Wix, covering page structure, product presentation, visual direction, and launch-ready assets.",
    "Edit podcast videos, product images, and campaign content while keeping visual systems consistent across web and social touchpoints.",
])
role("Product Designer | I-DOD", "New Delhi, India | Jul 2025 - Mar 2026", [
    "Turned ambiguous founder and stakeholder requirements into user flows, wireframes, prototypes, high-fidelity interfaces, and release-ready product decisions.",
    "Built a reusable Figma design system from scratch with components, interaction patterns, states, and implementation-ready documentation.",
    "Designed onboarding, profile creation, and beta feedback journeys for an early-stage product.",
])
role("Product Designer | FuelBuddy", "Gurgaon, India | Jul 2023 - Jun 2024", [
    "Redesigned diesel ordering from a 20-22 step journey into a focused location, quantity, schedule, and payment flow, improving completion from 62% to 78%.",
    "Reduced payment transaction errors by 38% through wallet improvements, delegated access, secondary-user controls, and configurable spend limits.",
    "Designed customer, business account, FMS, pilot, driver, and franchise experiences across India and UAE, spanning mobile apps, B2B web products, analytics, maps, live tracking, asset management, and account controls.",
    "Built the FuelBuddy design system from scratch across consumer, B2B, franchise, field, and operational products.",
])
role("Product Designer | Uncover by Meddo", "Gurgaon, India | Mar 2022 - May 2023", [
    "Reduced appointment booking from six steps to four, improving completion from 71% to 83% over eight weeks using analytics and user feedback.",
    "Redesigned doctor profiles, increasing profile views by 28% and appointment requests by 15% in a 5,000-user A/B test.",
    "Designed patient, doctor, and back-office experiences spanning discovery, appointments, lab tests, records, and early ABHA integration interfaces.",
    "Conducted usability testing with 12 patients and 8 doctors, translating findings into product and engineering priorities.",
])
role("UI Designer | AcadPlaza", "Remote | Jun 2020 - Mar 2022", [
    "Redesigned course catalog and search for a learning marketplace, increasing enrollments by 18% quarter over quarter.",
    "Created responsive web and mobile interfaces, wireframes, component patterns, and discovery journeys with an eight-person product, engineering, and content team.",
])

sec("Selected Work")
bullet("Portfolio: https://workofhayaat.framer.website")
bullet("Uncover / Meddo: healthcare product UX and design system work. https://uncover.co.in/")
bullet("FuelBuddy: customer, business, and operational product design across web and mobile. https://app.fuelbuddy.in/")
bullet("Kama Capital: multi-asset trading website and onboarding journeys. https://kama-capital.com/")
bullet("TS Logix Peru: logistics and warehousing web and internal tooling. https://tslogixperu.com/")

sec("Tools and Education")
p("<b>Tools:</b> Figma, FigJam, Framer, Wix, Adobe Photoshop, Illustrator, After Effects, Rive, Miro, Adobe XD, Google Analytics, Hotjar")
p("<b>BBA, Business Administration</b> | Sam Higginbottom University of Agriculture, Technology and Sciences | 2017 - 2020")

SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=0.5 * inch,
    rightMargin=0.5 * inch,
    topMargin=0.42 * inch,
    bottomMargin=0.42 * inch,
    title="Mohd Hayaat Ali - UI UX Designer - DigiFloworx",
).build(story)

print(OUT)
