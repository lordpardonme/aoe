from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_UX_Designer_Laerdal.pdf")

INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#0D5C63")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=22, leading=25, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.7, leading=13, textColor=ACCENT, spaceAfter=3),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.4, leading=10.5, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.8, leading=13, textColor=ACCENT, spaceBefore=6, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.35, leading=10.85, textColor=INK, spaceAfter=2),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.1, leading=11, textColor=INK, spaceBefore=3),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=7.9, leading=9.5, textColor=MUTED, spaceAfter=1.5),
    "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=7.95, leading=10.3, leftIndent=11, firstLineIndent=-7, spaceAfter=1.35, textColor=INK),
}

story = []


def p(text, style="body"):
    story.append(Paragraph(text, styles[style]))


def sec(text):
    p(text, "section")
    story.append(HRFlowable(width="100%", thickness=0.55, color=colors.HexColor("#C8D4D5"), spaceAfter=2.5))


def bullet(text):
    p("-&nbsp;&nbsp;" + text, "bullet")


def role(title, meta, items):
    p(title, "role")
    p(meta, "meta")
    for item in items:
        bullet(item)


p("Mohd Hayaat Ali", "name")
p("UX DESIGNER | HEALTHCARE, PRODUCT DESIGN AND DESIGN SYSTEMS", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Open to Bangalore hybrid / relocation discussion", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
story.append(Spacer(1, 3))
p("<b>UX/UI and Product Designer with 6+ years of experience</b> designing healthcare journeys, mobile apps, B2B SaaS platforms, internal tools, service workflows, and scalable Figma design systems. Strong fit for Laerdal's Bangalore UX roles through hands-on experience in user-centered healthcare products, usability testing, design facilitation, wireframing, prototyping, responsive UI, accessibility-aware decisions, and product-engineering collaboration.")

sec("Core Skills")
p("<b>Healthcare and User Research:</b> Healthcare UX, patient and doctor journeys, appointment booking, digital records, lab-test flows, usability testing, qualitative feedback, A/B testing, journey mapping, persona-driven design, accessibility-aware UX")
p("<b>Product and Interaction Design:</b> Information architecture, user flows, wireframes, responsive desktop and mobile UI, interaction design, prototyping, visual design, service workflow simplification, product discovery")
p("<b>Systems and Delivery:</b> Figma, FigJam, Auto Layout, reusable components, design systems, design QA, developer handoff, product owner collaboration, stakeholder presentations, user story refinement")

sec("Professional Experience")
role("Creative Designer | Crevia", "Delhi NCR, India | Jun 2026 - Present", [
    "Deliver website assets, product imagery, campaign material, social content, graphics, and video across multiple client brands while balancing parallel creative requirements.",
    "Design and build responsive website experiences in Wix, covering page structure, product presentation, visual direction, and launch-ready assets.",
])
role("Product Designer | I-DOD", "New Delhi, India | Jul 2025 - Mar 2026", [
    "Turned ambiguous founder and stakeholder requirements into user flows, wireframes, prototypes, high-fidelity interfaces, and release-ready product decisions.",
    "Built a reusable Figma design system from scratch with components, interaction patterns, states, and implementation-ready documentation.",
])
role("Product Designer | FuelBuddy", "Gurgaon, India | Jul 2023 - Jun 2024", [
    "Designed customer, FMS, pilot, driver, and franchise products across India and UAE, spanning mobile apps, B2B web platforms, analytics, maps, live tracking, asset management, field workflows, and account controls.",
    "Redesigned diesel ordering from a 20-22 step journey into a focused location, quantity, schedule, and payment flow, improving completion from 62% to 78%.",
    "Reduced payment transaction errors by 38% through wallet UX improvements, delegated access, secondary-user controls, and configurable spend limits.",
    "Reduced manual support input by 43% and improved ticket handling and resolution by 57% through clearer support and ticketing workflows.",
    "Built scalable Figma design-system foundations across consumer, B2B, franchise, field, and operational products with reusable components and developer-ready documentation.",
])
role("Product Designer | Uncover by Meddo", "Gurgaon, India | Mar 2022 - May 2023", [
    "Designed patient, doctor, and back-office healthcare experiences across discovery, appointment booking, healthcare memberships, lab tests, digital records, and early ABHA integration interfaces.",
    "Reduced appointment booking from six steps to four, improving completion from 71% to 83% over eight weeks using analytics and patient feedback.",
    "Redesigned doctor profiles, increasing profile views by 28% and appointment requests by 15% in a 5,000-user A/B test.",
    "Conducted usability testing with 12 patients and 8 doctors, translating findings into UX, design-system, and engineering priorities.",
])
role("UI Designer | AcadPlaza", "Remote | Jun 2020 - Mar 2022", [
    "Redesigned course catalog and search for a learning marketplace, increasing enrollments by 18% quarter over quarter.",
    "Created responsive web and mobile interfaces, wireframes, component patterns, and discovery journeys with an eight-person product, engineering, and content team.",
])

sec("Selected Relevant Work")
bullet("Uncover / Meddo healthcare UX: https://uncover.co.in/")
bullet("Doxper doctor-facing digital healthcare workflows: https://doxper.com/home/")
bullet("Meddo patient app: https://play.google.com/store/apps/details?id=in.meddo.patient&amp;hl=en_IN")
bullet("Vgen23 genetic interpretation and reporting app: https://vgen23.com/")
bullet("FuelBuddy UAE customer and operations work: https://fuelbuddy.ae/")
bullet("TS Logix Peru logistics and pharmaceutical distribution workflows: https://tslogixperu.com/")

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
    title="Mohd Hayaat Ali - UX Designer - Laerdal",
).build(story)

print(OUT)
