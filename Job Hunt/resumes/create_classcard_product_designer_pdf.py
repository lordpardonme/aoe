from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_Product_Designer_Classcard.pdf")

INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#155E75")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=23, leading=26, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.4, leading=13.1, textColor=ACCENT, spaceAfter=4),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.65, leading=11.1, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.8, leading=13.0, textColor=ACCENT, spaceBefore=6.2, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.45, leading=11.05, textColor=INK, spaceAfter=2.0),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.1, leading=11.0, textColor=INK, spaceBefore=3.0),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=8.05, leading=9.8, textColor=MUTED, spaceAfter=1.6),
    "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=7.95, leading=10.55, leftIndent=12, firstLineIndent=-8, spaceAfter=1.25, textColor=INK),
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
p("PRODUCT DESIGNER | SAAS, WEB/MOBILE, FIGMA SYSTEMS & AI-ASSISTED DESIGN", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Remote India", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
p("<b>Hands-on Product Designer with 6+ years of experience</b> designing responsive web and mobile products, B2B SaaS-style workflows, dashboards, and scalable Figma design systems. Strong in UI craft, user journeys, information architecture, prototypes, design QA, and developer handoff. Experienced working with founders, product teams, and engineers to move from ambiguous requirements to shipped interfaces for real users. I also use AI-assisted workflows for faster exploration, sharper iteration, and design-to-code collaboration without lowering product judgment or visual quality.")

sec("Core Skills")
p("<b>Product and UX:</b> User journeys, information architecture, wireframes, interaction design, high-fidelity UI, responsive web/mobile design, prototyping, usability testing, product iteration, stakeholder feedback")
p("<b>Figma and Systems:</b> Figma, FigJam, Auto Layout, components, variants, design systems, reusable patterns, UI states, visual consistency, design QA, developer handoff")
p("<b>SaaS and Web/Mobile:</b> B2B portals, dashboards, onboarding, account controls, operational workflows, analytics surfaces, marketplace flows, content-heavy interfaces, responsive websites")
p("<b>AI-Assisted Workflow:</b> AI design tools, prompt-assisted ideation, rapid concept exploration, design-to-code collaboration, production support, structured iteration")

sec("Professional Experience")
role("Creative Designer | Crevia", "Delhi NCR, India | Jun 2026 - Present", [
    "Create graphics, videos, social content, product imagery, website assets, and campaign material across multiple client brands and fast deadlines.",
    "Design and build responsive website experiences in Wix, covering page structure, product presentation, visual direction, and launch-ready assets.",
    "Edit podcast videos, product images, and campaign content while keeping visual systems consistent across web and social touchpoints.",
])
role("Product Designer | I-DOD", "New Delhi, India | Jul 2025 - Mar 2026", [
    "Translated ambiguous founder and stakeholder requirements into user flows, wireframes, prototypes, high-fidelity interfaces, and practical release decisions.",
    "Built a reusable Figma design system from scratch with components, interaction patterns, states, and implementation-ready documentation.",
    "Designed onboarding, profile creation, verification, matching, and beta feedback journeys for an early-stage product.",
])
role("Product Designer | FuelBuddy", "Gurgaon, India | Jul 2023 - Jun 2024", [
    "Designed customer, business account, FMS, pilot, driver, and franchise experiences across India and UAE, spanning mobile apps, B2B web products, dashboards, analytics, maps, live tracking, asset management, and account controls.",
    "Redesigned diesel ordering from a 20-22 step journey into a focused location, quantity, schedule, and payment flow, improving completion from 62% to 78%.",
    "Reduced payment transaction errors by 38% through wallet improvements, delegated access, secondary-user controls, and configurable spend limits.",
    "Built the FuelBuddy design system from scratch across consumer, B2B, franchise, field, and operational products.",
    "Replaced spreadsheet-heavy operational patterns with structured product workflows for drivers, trucks, routes, shifts, delivery planning, corrections, and reporting.",
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
bullet("FuelBuddy Customer Web App: B2B/customer fuel ordering and account experience across web and mobile. https://app.fuelbuddy.in/")
bullet("Maximor AI: AI automation platform landing page for finance operations and close workflows. https://www.maximor.ai/cfo-offer-all")
bullet("Vgen23: Web-based genetic interpretation and reporting platform for complex clinical workflows. https://vgen23.com/")
bullet("Uncover / Meddo: Healthcare product UX, booking flows, patient experience, and design-system work. https://uncover.co.in/")
bullet("TS Logix Peru: Logistics website and internal WMS work covering inventory and operational workflows. https://tslogixperu.com/")

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
    title="Mohd Hayaat Ali - Product Designer - Classcard",
).build(story)
print(OUT)
