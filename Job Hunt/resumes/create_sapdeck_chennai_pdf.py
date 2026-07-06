from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_Senior_UI_UX_Designer_Sapdeck_Chennai.pdf")
INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#164E63")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=23, leading=26, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.8, leading=13.5, textColor=ACCENT, spaceAfter=4),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.8, leading=11.3, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11.1, leading=13.5, textColor=ACCENT, spaceBefore=6.5, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.8, leading=11.55, textColor=INK, spaceAfter=2.4),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.35, leading=11.3, textColor=INK, spaceBefore=3.5),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=8.2, leading=10.1, textColor=MUTED, spaceAfter=1.8),
    "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=8.25, leading=11.0, leftIndent=12, firstLineIndent=-8, spaceAfter=1.5, textColor=INK),
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
p("SENIOR UI/UX DESIGNER | WEB, MOBILE, RESEARCH & DESIGN SYSTEMS", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Open to Chennai contract / remote-hybrid discussions", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
p("<b>Senior UI/UX and Product Designer with 6+ years of experience</b> designing responsive web, mobile apps, B2B SaaS, healthcare, logistics, fintech, and internal tools. Strong hands-on fit for contract teams needing user research, usability testing, interaction design, wireframes, prototypes, high-fidelity UI, WCAG-aware responsive design, stakeholder management, and Figma design systems.")

sec("Core Skills")
p("<b>UX & Research:</b> user research, usability testing, journey mapping, information architecture, task flows, interaction design, wireframing, prototyping, stakeholder workshops")
p("<b>UI & Visual Design:</b> responsive web, mobile-first design, iOS/Android app UX, visual systems, typography, layout, accessibility/WCAG-aware interface decisions, high-fidelity UI")
p("<b>Tools & Delivery:</b> Figma, FigJam, Adobe XD, Adobe Creative Suite, Framer, Miro, Hotjar, Google Analytics, developer handoff, design QA, design-system documentation")

sec("Professional Experience")
role("Product Designer | FuelBuddy", "Gurgaon, India | Jul 2023 - Jun 2024", [
    "Designed customer, FMS, pilot, driver, and franchise products across India and UAE, spanning mobile apps, B2B web products, dashboards, maps, live tracking, asset management, and account controls.",
    "Redesigned diesel ordering from a 20-22 step journey into a focused location, quantity, schedule, and payment flow, improving completion from 62% to 78%.",
    "Reduced payment transaction errors by 38% through wallet improvements, delegated access, secondary-user controls, and configurable spend limits.",
    "Built the FuelBuddy design system across consumer, B2B, franchise, field, and operational products with reusable Figma components and handoff documentation.",
])
role("Product Designer | Uncover by Meddo", "Gurgaon, India | Mar 2022 - May 2023", [
    "Designed patient, doctor, and back-office healthcare experiences covering discovery, appointments, memberships, lab tests, digital records, and early ABHA integration interfaces.",
    "Reduced appointment booking from six steps to four, improving completion from 71% to 83% over eight weeks using analytics and user feedback.",
    "Conducted usability testing with 12 patients and 8 doctors, translating findings into product, design-system, and engineering priorities.",
    "Redesigned doctor profiles, increasing profile views by 28% and appointment requests by 15% in a 5,000-user A/B test.",
])
role("Product Designer | I-DOD", "New Delhi, India | Jul 2025 - Mar 2026", [
    "Translated ambiguous requirements into user flows, wireframes, prototypes, high-fidelity interfaces, and release-ready decisions with founders and developers.",
    "Built a Figma design system from scratch with reusable components, interaction patterns, states, and implementation-ready documentation.",
])
role("Creative Designer | Crevia", "Delhi NCR, India | Jun 2026 - Present", [
    "Deliver responsive website assets, product imagery, campaign material, graphics, video, and launch-ready design work across multiple client brands.",
])
role("UI Designer | AcadPlaza", "Remote | Jun 2020 - Mar 2022", [
    "Redesigned course catalog and search for a learning marketplace, increasing enrollments by 18% quarter over quarter.",
    "Created responsive web and mobile interfaces, wireframes, component patterns, and discovery journeys with an eight-person cross-functional team.",
])

sec("Selected Live Work")
bullet("Portfolio: https://workofhayaat.framer.website")
bullet("FuelBuddy UAE: https://fuelbuddy.ae/")
bullet("FuelBuddy customer web app: https://app.fuelbuddy.in/")
bullet("FuelBuddy Android: https://play.google.com/store/apps/details?id=in.fuelbuddy.app&amp;hl=en_IN")
bullet("FuelBuddy FMS: https://play.google.com/store/apps/details?id=in.fuelbuddy.fms&amp;hl=en_IN")
bullet("Uncover: https://uncover.co.in/")
bullet("Meddo patient app: https://play.google.com/store/apps/details?id=in.meddo.patient&amp;hl=en_IN")
bullet("Vgen23: https://vgen23.com/")

sec("Education")
p("<b>BBA, Business Administration</b> | Sam Higginbottom University of Agriculture, Technology and Sciences | 2017 - 2020")

SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=.55 * inch,
    rightMargin=.55 * inch,
    topMargin=.45 * inch,
    bottomMargin=.45 * inch,
    title="Mohd Hayaat Ali - Senior UI UX Designer - Sapdeck Chennai"
).build(story)
print(OUT)
