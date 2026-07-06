from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_Senior_UI_UX_Designer_Marc_Ellis.pdf")

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
p("SENIOR UI/UX DESIGNER | AI-DRIVEN DESIGN SYSTEMS & DIGITAL PRODUCTS", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Open to Dubai onsite opportunities | Immediate / short-notice discussion", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
story.append(Spacer(1, 3))
p("<b>Senior UI/UX and Product Designer with 6+ years of experience</b> designing responsive websites, mobile applications, and digital products with a strong focus on scalable design systems. Strong in user journeys, high-fidelity UI, prototyping, micro-interactions, and turning business requirements into implementation-ready interfaces. I also use AI-assisted workflows to accelerate ideation, documentation, iteration, and production support.")

sec("Core Skills")
p("<b>UI/UX and Product Design:</b> User journeys, information architecture, wireframing, interaction design, responsive desktop and mobile UI, prototyping, usability testing, design thinking, stakeholder communication")
p("<b>Design Systems and Delivery:</b> Figma, FigJam, Auto Layout, reusable components, variants, design systems, design QA, developer handoff, cross-functional collaboration, responsive specifications")
p("<b>Visual and Interaction Design:</b> Typography, spacing, color, visual hierarchy, layout systems, accessibility-aware UI, micro-interactions, interactive states, polished high-fidelity design")
p("<b>AI-Assisted Workflow:</b> Claude-style AI workflows, design ideation, prompt-assisted exploration, iteration speed, documentation support, design problem solving")

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
    "Standardized repeated screens and operational states so teams could move faster while keeping the interface language consistent across modules.",
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
    leftMargin=.55 * inch,
    rightMargin=.55 * inch,
    topMargin=.45 * inch,
    bottomMargin=.45 * inch,
    title="Mohd Hayaat Ali - Senior UI UX Designer - Marc Ellis"
).build(story)
print(OUT)
