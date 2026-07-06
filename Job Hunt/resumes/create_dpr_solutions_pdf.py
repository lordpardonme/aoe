from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_Senior_UX_UI_Designer_DPR_Solutions.pdf")
INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#155E75")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=23, leading=26, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.7, leading=13.3, textColor=ACCENT, spaceAfter=4),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.75, leading=11.2, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11.0, leading=13.3, textColor=ACCENT, spaceBefore=6.5, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.7, leading=11.4, textColor=INK, spaceAfter=2.2),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.25, leading=11.2, textColor=INK, spaceBefore=3.2),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=8.15, leading=10.0, textColor=MUTED, spaceAfter=1.7),
    "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=8.15, leading=10.85, leftIndent=12, firstLineIndent=-8, spaceAfter=1.4, textColor=INK),
}

story = []
def p(text, style="body"): story.append(Paragraph(text, styles[style]))
def sec(text):
    p(text, "section")
    story.append(HRFlowable(width="100%", thickness=.65, color=colors.HexColor("#C8D4D5"), spaceAfter=3))
def bullet(text): p("-&nbsp;&nbsp;" + text, "bullet")
def role(title, meta, items):
    p(title, "role"); p(meta, "meta")
    for item in items: bullet(item)

p("Mohd Hayaat Ali", "name")
p("SENIOR UX/UI DESIGNER | DESIGN SYSTEMS, FRONT-END AWARE UX & AI WORKFLOWS", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Remote | Immediate / short-notice discussion", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
p("<b>Senior UX/UI and Product Designer with 6+ years of experience</b> designing web and mobile applications, SaaS/B2B products, healthcare, fintech/payment UX, logistics dashboards, and design systems. Strong fit for roles requiring Figma components, Auto Layout, user research, prototypes, accessible responsive UI, collaboration with developers, front-end-aware handoff, and AI-assisted design workflows.")

sec("Relevant Skills")
p("<b>UX/UI:</b> product discovery, user research, usability testing, journey mapping, wireframes, prototypes, high-fidelity UI, interaction design, responsive and accessible design")
p("<b>Design Systems:</b> Figma, Auto Layout, components, variants, states, tokens, documentation, scalable UI patterns, developer-ready handoff, design QA")
p("<b>Front-End & AI Workflow:</b> HTML/CSS/JavaScript awareness, React/Next.js collaboration, Tailwind-style utility systems, Framer, ChatGPT/Claude-style workflow acceleration, Figma AI, Cursor/GitHub Copilot awareness")
p("<b>Domains:</b> SaaS, B2B products, healthcare, fintech/payment UX, logistics, dashboards, internal tools, consumer mobile experiences")

sec("Professional Experience")
role("Product Designer | FuelBuddy", "Gurgaon, India | Jul 2023 - Jun 2024", [
    "Designed customer, FMS, pilot, driver, and franchise products across India and UAE, spanning mobile apps, B2B web products, dashboards, maps, live tracking, asset management, and account controls.",
    "Redesigned diesel ordering from a 20-22 step journey into a focused location, quantity, schedule, and payment flow, improving completion from 62% to 78%.",
    "Reduced payment transaction errors by 38% through wallet improvements, delegated access, secondary-user controls, and configurable spend limits.",
    "Built the FuelBuddy design system across consumer, B2B, franchise, field, and operational products with reusable Figma components, states, patterns, and handoff documentation.",
])
role("Product Designer | Uncover by Meddo", "Gurgaon, India | Mar 2022 - May 2023", [
    "Designed patient, doctor, and back-office healthcare experiences across discovery, appointments, memberships, lab tests, digital records, and early ABHA integration interfaces.",
    "Reduced appointment booking from six steps to four, improving completion from 71% to 83% over eight weeks using analytics and user feedback.",
    "Conducted usability testing with 12 patients and 8 doctors, translating findings into product, design-system, and engineering priorities.",
])
role("Product Designer | I-DOD", "New Delhi, India | Jul 2025 - Mar 2026", [
    "Translated founder requirements into user flows, wireframes, prototypes, high-fidelity interfaces, and practical release decisions with developers.",
    "Built a Figma design system from scratch with reusable components, Auto Layout patterns, states, interaction patterns, and implementation-ready documentation.",
])
role("Creative Designer | Crevia", "Delhi NCR, India | Jun 2026 - Present", [
    "Design and build responsive website assets, product imagery, campaign material, graphics, videos, and launch-ready digital experiences across client brands.",
])
role("UI Designer | AcadPlaza", "Remote | Jun 2020 - Mar 2022", [
    "Redesigned course catalog and search for a learning marketplace, increasing enrollments by 18% quarter over quarter.",
    "Created responsive web/mobile interfaces, wireframes, component patterns, and discovery journeys with an eight-person product, engineering, and content team.",
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
    title="Mohd Hayaat Ali - Senior UX UI Designer - DPR Solutions"
).build(story)
print(OUT)
