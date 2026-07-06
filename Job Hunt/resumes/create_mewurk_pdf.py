from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_UI_UX_Designer_Mewurk.pdf")
INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#0B666A")
base = getSampleStyleSheet()
s = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=23, leading=26, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.7, leading=13, textColor=ACCENT, spaceAfter=4),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.8, leading=11.5, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11.2, leading=13.5, textColor=ACCENT, spaceBefore=6, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.8, leading=12, textColor=INK, spaceAfter=2.2),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.5, leading=11.5, textColor=INK, spaceBefore=3.5),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=8.3, leading=10, textColor=MUTED, spaceAfter=1.5),
    "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=8.45, leading=11.45, leftIndent=13, firstLineIndent=-9, spaceAfter=1.5, textColor=INK),
}

story = []


def p(text, style="body"):
    story.append(Paragraph(text, s[style]))


def section(text):
    p(text, "section")
    story.append(HRFlowable(width="100%", thickness=.7, color=colors.HexColor("#C8D4D5"), spaceAfter=2.5))


def bullet(text):
    p("-&nbsp;&nbsp;" + text, "bullet")


def role(title, meta, items):
    p(title, "role")
    p(meta, "meta")
    for item in items:
        bullet(item)


p("Mohd Hayaat Ali", "name")
p("UI/UX DESIGNER | PRODUCT DESIGN, INTERACTION DESIGN & DESIGN SYSTEMS", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India", "contact")
p("Portfolio: https://workofhayaat.framer.website | Open to relocation, subject to role terms and work authorization", "contact")
p("<b>UI/UX and product designer with 6+ years of experience</b> shipping web and mobile experiences across commerce, healthcare, logistics, fintech, internal tools, and design systems. Strong in user flows, wireframing, high-fidelity UI, prototyping, usability testing, responsive design, and developer handoff.", "body")

section("Core Skills")
p("<b>UX & Product:</b> User research, usability testing, journey mapping, information architecture, user flows, wireframing, interaction design, responsive design, prototyping")
p("<b>UI & Systems:</b> High-fidelity UI, design systems, reusable Figma components, Auto Layout, visual hierarchy, accessibility awareness, design QA, developer handoff")
p("<b>Collaboration & Delivery:</b> Product thinking, stakeholder management, cross-functional collaboration, sprint feedback loops, iteration, presentation, implementation support")

section("Professional Experience")
role("Creative Designer | Crevia", "Delhi NCR, India | June 2026 - Present", [
    "Deliver websites, campaign assets, social content, graphics, and video across multiple client brands and concurrent deadlines.",
    "Design and build the Mymy perfume website in Wix, covering page structure, product presentation, visual direction, and launch-ready assets.",
])
role("Product Designer | I-DOD", "New Delhi, India | July 2025 - March 2026", [
    "Partnered directly with founders and developers to turn ambiguous product requirements into user flows, prototypes, high-fidelity interfaces, and release decisions.",
    "Built a reusable Figma design system from scratch with components, interaction patterns, states, and implementation-ready documentation.",
    "Designed onboarding, KYC verification, profile creation, matching journeys, and beta feedback loops for an early-stage relationship platform.",
])
role("Product Designer | FuelBuddy", "Gurgaon, India | July 2023 - June 2024", [
    "Redesigned diesel ordering from a 20-22 step journey into a focused location, quantity, schedule, and payment flow, improving completion from 62% to 78%.",
    "Reduced payment transaction errors by 38% through wallet improvements, delegated access, secondary-user controls, and configurable spend limits.",
    "Designed customer, FMS, pilot, and driver experiences across India and UAE, spanning mobile apps, B2B web products, analytics, maps, live tracking, asset management, and account controls.",
    "Reduced manual support input by 43% and improved ticket handling and resolution by 57% through structured support and ticketing workflows.",
    "Built the FuelBuddy design system from scratch across consumer, B2B, franchise, field, and operational products.",
])
role("Product Designer | Uncover by Meddo", "Gurgaon, India | March 2022 - May 2023", [
    "Reduced appointment booking from six steps to four, improving completion from 71% to 83% over eight weeks using analytics and user feedback.",
    "Redesigned doctor profiles, increasing profile views by 28% and appointment requests by 15% in a 5,000-user A/B test.",
    "Designed patient, doctor, and back-office experiences spanning discovery, appointments, healthcare memberships, lab tests, digital records, and early ABHA integration interfaces.",
    "Conducted usability testing with 12 patients and 8 doctors, translating findings into product, design-system, and engineering priorities.",
])
role("UI Designer | AcadPlaza", "Remote | June 2020 - March 2022", [
    "Redesigned course catalog and search for a learning marketplace, increasing enrollments by 18% quarter over quarter.",
    "Created responsive web and mobile interfaces, wireframes, component patterns, and discovery journeys with an eight-person product, engineering, and content team.",
])

section("Selected Live Projects")
bullet("Portfolio: https://workofhayaat.framer.website")
bullet("FuelBuddy Customer Web App: https://app.fuelbuddy.in/")
bullet("FuelBuddy UAE: https://fuelbuddy.ae/")
bullet("Vgen23: https://vgen23.com/")
bullet("TS Logix Peru: https://tslogixperu.com/")

section("Tools & Education")
p("<b>Tools:</b> Figma, FigJam, Framer, Wix, Adobe Photoshop, Illustrator, After Effects, Rive, Miro, Adobe XD, Google Analytics, Hotjar")
p("<b>BBA, Business Administration</b> | Sam Higginbottom University of Agriculture, Technology and Sciences | 2017 - 2020")

SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=.55 * inch,
    rightMargin=.55 * inch,
    topMargin=.44 * inch,
    bottomMargin=.44 * inch,
    title="Mohd Hayaat Ali - UI UX Designer Mewurk",
).build(story)

print(OUT)
