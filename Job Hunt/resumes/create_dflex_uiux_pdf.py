from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_UI_UX_Designer_Dflex.pdf")

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
p("UI/UX DESIGNER | COMMERCE JOURNEYS, ORDERING & DESIGN SYSTEMS", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Open to remote, hybrid, or relocation discussion", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
story.append(Spacer(1, 3))
p("<b>UI/UX and Product Designer with 6+ years of experience</b> designing connected customer journeys, operational platforms, responsive web and mobile products, and scalable design systems. Strong record of partnering with product managers, engineers, founders, and stakeholders to simplify complex workflows, improve completion, and translate business requirements into intuitive product experiences.")

sec("Core Capabilities")
p("<b>Product Strategy & UX:</b> Product thinking, UX strategy, user research, journey mapping, information architecture, user flows, service design, prototyping, usability testing, experimentation, product metrics")
p("<b>Commerce & Operations:</b> Ordering, payment and wallet UX, account controls, delegated access, fulfillment workflows, internal operations, dashboards, support systems, trust and error states, service flow simplification")
p("<b>UI & Delivery:</b> High-fidelity UI, responsive design, design systems, reusable Figma components, accessibility awareness, developer handoff, design QA, stakeholder management, cross-functional collaboration")

sec("Professional Experience")
role("Creative Designer | Crevia", "Delhi NCR, India | Jun 2026 - Present", [
    "Deliver responsive websites, product imagery, campaign assets, social content, graphics, and video across multiple client brands and concurrent deadlines.",
    "Design and build the Mymy perfume website in Wix, covering page structure, product presentation, visual direction, and launch-ready assets.",
])
role("Product Designer | I-DOD", "New Delhi, India | Jul 2025 - Mar 2026", [
    "Partnered directly with founders and developers to turn ambiguous product requirements into user flows, prototypes, high-fidelity interfaces, and release decisions.",
    "Built a reusable Figma design system from scratch with components, interaction patterns, states, and implementation-ready documentation.",
    "Designed onboarding, KYC verification, profile creation, matching journeys, and beta feedback loops for an early-stage relationship platform.",
])
role("Product Designer | FuelBuddy", "Gurgaon, India | Jul 2023 - Jun 2024", [
    "Designed connected customer ordering and operational workflows across India and UAE, spanning responsive web, mobile apps, dashboards, maps, live tracking, asset management, fulfillment, and account controls.",
    "Redesigned diesel ordering from 20-22 steps into a focused journey, improving completion from 62% to 78%.",
    "Reduced payment transaction errors by 38% through wallet improvements, delegated access, secondary-user controls, and configurable spend limits.",
    "Replaced spreadsheet-heavy franchise operations with workflows for drivers, trucks, routes, shifts, delivery planning, quantity correction, and reports.",
    "Reduced manual support input by 43% and improved ticket handling and resolution by 57% through structured support workflows.",
    "Built the FuelBuddy design system from scratch and collaborated with product and engineering through handoff and design QA.",
])
role("Product Designer | Uncover by Meddo", "Gurgaon, India | Mar 2022 - May 2023", [
    "Improved appointment completion from 71% to 83% by simplifying discovery and booking journeys using analytics and user feedback.",
    "Redesigned doctor profiles, increasing profile views by 28% and appointment requests by 15% in a 5,000-user A/B test.",
    "Conducted usability testing with 12 patients and 8 doctors, translating findings into product, design-system, and engineering priorities.",
    "Created Uncover's brand foundation and carried it into responsive web, mobile, and reusable UI patterns.",
])
role("UI Designer | AcadPlaza", "Remote | Jun 2020 - Mar 2022", [
    "Redesigned catalog and search for a learning marketplace, increasing enrollments by 18% quarter over quarter.",
    "Created responsive web and mobile interfaces, wireframes, component patterns, and discovery journeys with an eight-person product, engineering, and content team.",
])

sec("Selected Live Projects")
bullet("FuelBuddy Customer Web App: https://app.fuelbuddy.in/")
bullet("TS Logix Peru: logistics website and internal WMS work covering inventory and operational workflows. https://tslogixperu.com/")
bullet("Vgen23: complex genetic interpretation and reporting application. https://vgen23.com/")
bullet("Portfolio: product, UX/UI, systems, and visual work. https://workofhayaat.framer.website")

sec("Tools and Education")
p("<b>Tools:</b> Figma, FigJam, Framer, Adobe Photoshop, Illustrator, After Effects, Rive, Miro, Adobe XD, Google Analytics, Hotjar")
p("<b>BBA, Business Administration</b> | Sam Higginbottom University of Agriculture, Technology and Sciences | 2017 - 2020")

SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=.55 * inch,
    rightMargin=.55 * inch,
    topMargin=.45 * inch,
    bottomMargin=.45 * inch,
    title="Mohd Hayaat Ali - UI UX Designer - Dflex"
).build(story)
print(OUT)
