from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_UI_UX_Designer_IMC_Bangalore.pdf")
INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#8B1E1E")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=23, leading=26, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.8, leading=13.4, textColor=ACCENT, spaceAfter=4),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.8, leading=11.2, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11.0, leading=13.2, textColor=ACCENT, spaceBefore=6.5, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.75, leading=11.45, textColor=INK, spaceAfter=2.2),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.25, leading=11.15, textColor=INK, spaceBefore=3.2),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=8.15, leading=10.0, textColor=MUTED, spaceAfter=1.7),
    "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=8.2, leading=10.9, leftIndent=12, firstLineIndent=-8, spaceAfter=1.4, textColor=INK),
}

story = []


def p(text, style="body"):
    story.append(Paragraph(text, styles[style]))


def sec(text):
    p(text, "section")
    story.append(HRFlowable(width="100%", thickness=0.65, color=colors.HexColor("#C8D4D5"), spaceAfter=3))


def bullet(text):
    p("-&nbsp;&nbsp;" + text, "bullet")


def role(title, meta, items):
    p(title, "role")
    p(meta, "meta")
    for item in items:
        bullet(item)


p("Mohd Hayaat Ali", "name")
p("UI/UX DESIGNER | WEB, MOBILE, DASHBOARDS & DESIGN SYSTEMS", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Open to Bangalore relocation / hybrid", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
p("<b>UI/UX and Product Designer with 6+ years of experience</b> building responsive web and mobile experiences, dashboards, portals, operational tools, and healthcare/fintech products. Hands-on across Figma, Photoshop, Illustrator, wireframes, prototypes, design systems, usability testing, and developer handoff, with a strong focus on clean visual design, typography, and practical delivery.")

sec("Core Skills")
p("<b>UX & Research:</b> user research, usability testing, journey mapping, information architecture, wireframing, prototyping, interaction design, responsive design")
p("<b>UI & Visual Design:</b> Figma, Photoshop, Illustrator, typography, color systems, layout, grid systems, premium visual polish, accessibility-aware interfaces")
p("<b>Delivery:</b> design systems, Auto Layout, reusable components, developer handoff, design QA, product collaboration, stakeholder communication, cross-functional teamwork")

sec("Professional Experience")
role("Product Designer | FuelBuddy", "Gurgaon, India | Jul 2023 - Jun 2024", [
    "Designed customer, FMS, pilot, driver, and franchise products across India and UAE, spanning mobile apps, dashboards, maps, live tracking, account controls, and operational workflows.",
    "Redesigned diesel ordering from a 20-22 step journey into a focused location, quantity, schedule, and payment flow, improving completion from 62% to 78%.",
    "Reduced payment transaction errors by 38% through wallet improvements, delegated access, secondary-user controls, and configurable spend limits.",
    "Built the FuelBuddy design system from scratch with reusable Figma components, states, patterns, and implementation-ready documentation.",
])
role("Product Designer | Uncover by Meddo", "Gurgaon, India | Mar 2022 - May 2023", [
    "Designed patient, doctor, and back-office healthcare experiences across discovery, appointments, memberships, lab tests, digital records, and early ABHA integration interfaces.",
    "Reduced appointment booking from six steps to four, improving completion from 71% to 83% over eight weeks using analytics and user feedback.",
    "Conducted usability testing with 12 patients and 8 doctors, translating findings into product, design-system, and engineering priorities.",
    "Redesigned doctor profiles, increasing profile views by 28% and appointment requests by 15% in a 5,000-user A/B test.",
])
role("Product Designer | I-DOD", "New Delhi, India | Jul 2025 - Mar 2026", [
    "Translated ambiguous founder requirements into user flows, wireframes, prototypes, high-fidelity interfaces, and practical release decisions with developers.",
    "Built a Figma design system from scratch with reusable components, Auto Layout patterns, states, and documentation.",
])
role("Creative Designer | Crevia", "Delhi NCR, India | Jun 2026 - Present", [
    "Create brand-led website assets, product imagery, campaign material, graphics, and video with an emphasis on polished visual presentation and launch-ready execution.",
])
role("UI Designer | AcadPlaza", "Remote | Jun 2020 - Mar 2022", [
    "Redesigned course catalog and search for a learning marketplace, increasing enrollments by 18% quarter over quarter.",
    "Created responsive web and mobile interfaces, wireframes, component patterns, and discovery journeys with an eight-person product, engineering, and content team.",
])

sec("Selected Live Work")
bullet("Portfolio: https://workofhayaat.framer.website")
bullet("FuelBuddy UAE: https://fuelbuddy.ae/")
bullet("FuelBuddy customer web app: https://app.fuelbuddy.in/")
bullet("FuelBuddy Android: https://play.google.com/store/apps/details?id=in.fuelbuddy.app&hl=en_IN")
bullet("FuelBuddy FMS: https://play.google.com/store/apps/details?id=in.fuelbuddy.fms&hl=en_IN")
bullet("Uncover: https://uncover.co.in/")
bullet("Meddo patient app: https://play.google.com/store/apps/details?id=in.meddo.patient&hl=en_IN")
bullet("Vgen23: https://vgen23.com/")
bullet("TS Logix Peru: https://tslogixperu.com/")
bullet("Maximor AI: https://www.maximor.ai/cfo-offer-all")
bullet("Kama Capital: https://kama-capital.com/")

sec("Education")
p("<b>BBA, Business Administration</b> | Sam Higginbottom University of Agriculture, Technology and Sciences | 2017 - 2020")

SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=0.55 * inch,
    rightMargin=0.55 * inch,
    topMargin=0.45 * inch,
    bottomMargin=0.45 * inch,
    title="Mohd Hayaat Ali - UI UX Designer - IMC Bangalore",
).build(story)
print(OUT)
