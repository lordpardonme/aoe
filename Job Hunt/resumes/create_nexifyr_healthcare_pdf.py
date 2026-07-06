from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_UI_UX_Designer_Nexifyr_Digital_Health_US.pdf")
INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#145C63")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=23, leading=26, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.8, leading=13.5, textColor=ACCENT, spaceAfter=4),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.8, leading=11.3, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11.1, leading=13.5, textColor=ACCENT, spaceBefore=6.5, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.85, leading=11.7, textColor=INK, spaceAfter=2.4),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.4, leading=11.4, textColor=INK, spaceBefore=3.5),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=8.25, leading=10.2, textColor=MUTED, spaceAfter=1.8),
    "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=8.35, leading=11.15, leftIndent=12, firstLineIndent=-8, spaceAfter=1.6, textColor=INK),
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
p("UI/UX DESIGNER | DIGITAL HEALTH, MOBILE APPS & DESIGN SYSTEMS", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Remote consultant / contract", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
p("<b>UI/UX and Product Designer with 6+ years of experience</b> designing shipped mobile apps, healthcare journeys, patient/provider workflows, B2B dashboards, and scalable Figma design systems. Strong fit for remote digital-health consulting across mobile app UX, virtual care flows, patient engagement, accessibility-aware interfaces, prototyping, and developer handoff.")

sec("Relevant Skills")
p("<b>Healthcare & Patient UX:</b> appointment booking, doctor profiles, patient records, lab-test flows, memberships, provider/back-office tools, healthcare workflow simplification, usability testing with patients and doctors")
p("<b>Mobile Product Design:</b> iOS/Android app UX, responsive web, interaction design, wireframes, prototypes, user journeys, task flows, senior-user clarity, WCAG/accessibility-aware interface decisions")
p("<b>Systems & Delivery:</b> Figma, FigJam, Auto Layout, design systems, reusable components, states, documentation, design QA, product/engineering collaboration, remote consulting delivery")

sec("Professional Experience")
role("Product Designer | Uncover by Meddo", "Gurgaon, India | Mar 2022 - May 2023", [
    "Designed patient, doctor, and back-office healthcare experiences across discovery, appointment booking, healthcare memberships, lab tests, digital records, and early ABHA integration interfaces.",
    "Reduced appointment booking from six steps to four, improving completion from 71% to 83% over eight weeks using analytics and patient feedback.",
    "Redesigned doctor profiles, increasing profile views by 28% and appointment requests by 15% in a 5,000-user A/B test.",
    "Conducted usability testing with 12 patients and 8 doctors, translating findings into prioritized UX, design-system, and engineering improvements.",
])
role("Product Designer | FuelBuddy", "Gurgaon, India | Jul 2023 - Jun 2024", [
    "Designed customer, FMS, pilot, driver, and franchise products across India and UAE, spanning mobile apps, B2B web platforms, dashboards, maps, live tracking, and operational workflows.",
    "Redesigned a complex ordering journey from 20-22 steps into a focused location, quantity, schedule, and payment flow, improving completion from 62% to 78%.",
    "Reduced payment transaction errors by 38% through wallet UX improvements, delegated access, secondary-user controls, and configurable spend limits.",
    "Built scalable Figma design-system foundations across consumer, B2B, franchise, field, and operational products with reusable components and implementation documentation.",
])
role("Product Designer | I-DOD", "New Delhi, India | Jul 2025 - Mar 2026", [
    "Translated ambiguous founder requirements into user flows, wireframes, prototypes, high-fidelity interfaces, and release-ready product decisions.",
    "Built a design system from scratch with reusable Figma components, interaction patterns, states, and developer-ready documentation.",
])
role("Creative Designer | Crevia", "Delhi NCR, India | Jun 2026 - Present", [
    "Deliver responsive website assets, campaign material, product imagery, graphics, and video across multiple client brands and concurrent deadlines.",
])
role("UI Designer | AcadPlaza", "Remote | Jun 2020 - Mar 2022", [
    "Created responsive web and mobile interfaces, wireframes, component patterns, and discovery journeys with an eight-person product, engineering, and content team.",
])

sec("Selected Live Work")
bullet("Portfolio: https://workofhayaat.framer.website")
bullet("Uncover healthcare product: https://uncover.co.in/")
bullet("Meddo patient app: https://play.google.com/store/apps/details?id=in.meddo.patient&amp;hl=en_IN")
bullet("FuelBuddy UAE: https://fuelbuddy.ae/")
bullet("FuelBuddy customer web app: https://app.fuelbuddy.in/")
bullet("FuelBuddy Android: https://play.google.com/store/apps/details?id=in.fuelbuddy.app&amp;hl=en_IN")
bullet("FuelBuddy FMS: https://play.google.com/store/apps/details?id=in.fuelbuddy.fms&amp;hl=en_IN")
bullet("Vgen23 genetic interpretation and reporting app: https://vgen23.com/")

sec("Tools & Education")
p("<b>Tools:</b> Figma, FigJam, Framer, Wix, Adobe Photoshop, Illustrator, After Effects, Rive, Miro, Adobe XD, Google Analytics, Hotjar")
p("<b>BBA, Business Administration</b> | Sam Higginbottom University of Agriculture, Technology and Sciences | 2017 - 2020")

SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=.55 * inch,
    rightMargin=.55 * inch,
    topMargin=.45 * inch,
    bottomMargin=.45 * inch,
    title="Mohd Hayaat Ali - UI/UX Designer - Nexifyr Digital Health"
).build(story)
print(OUT)
