from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_Product_Designer_Digital_Regenesys.pdf")

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
p("PRODUCT DESIGNER | LEARNING PLATFORMS, END-TO-END UX &amp; FIGMA DESIGN SYSTEMS", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Open to relocating to Mumbai", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
p("<b>Product Designer with 6+ years of experience</b> owning the full design process from research and wireframing through high-fidelity UI, design systems, and developer handoff. I have shipped course discovery and enrollment journeys for a learning marketplace, run usability testing and A/B tests that moved completion and engagement metrics, and built design systems from scratch on three products. I work closely with product managers, engineers, and content teams, and I justify design decisions with analytics and user evidence rather than preference.")

sec("Core Skills")
p("<b>End-to-End Product Design:</b> User research, usability testing, user flows, information architecture, wireframes, interaction design, high-fidelity UI, prototyping, design QA, developer handoff")
p("<b>Design Systems:</b> Figma, FigJam, Auto Layout, components, variants, component libraries, interaction patterns, UI states, documentation, cross-platform consistency")
p("<b>Learning and Content Platforms:</b> Course catalog and search, discovery journeys, enrollment flows, content-heavy interfaces, responsive web and mobile, onboarding")
p("<b>Data-Informed Design:</b> A/B testing, funnel and drop-off analysis, Google Analytics, Hotjar, usability sessions, feedback synthesis, metric-led iteration")
p("<b>Collaboration:</b> Product managers, engineers, content teams, founders and leadership, design rationale presentation, scoping and feasibility trade-offs, accessibility awareness")

sec("Professional Experience")
role("Creative Designer | Crevia", "Delhi NCR, India | Jun 2026 - Present", [
    "Create graphics, videos, social content, product imagery, website assets, and campaign material across multiple client brands and fast deadlines.",
    "Design and build responsive website experiences in Wix, covering page structure, content presentation, visual direction, and launch-ready assets.",
    "Maintain consistent visual systems across web and social touchpoints while working to short delivery cycles.",
])
role("Product Designer | I-DOD", "New Delhi, India | Jul 2025 - Mar 2026", [
    "Owned the design process end to end for assigned product areas, translating ambiguous requirements into user flows, wireframes, prototypes, and high-fidelity interfaces.",
    "Built a reusable Figma design system from scratch with components, interaction patterns, states, and implementation-ready documentation.",
    "Designed onboarding, profile creation, verification, and beta feedback journeys, then worked directly with engineers on scoping and release decisions.",
])
role("Product Designer | FuelBuddy", "Gurgaon, India | Jul 2023 - Jun 2024", [
    "Redesigned a 20-22 step ordering journey into a focused flow, improving completion from 62% to 78%.",
    "Reduced transaction errors by 38% through wallet improvements, delegated access, secondary-user controls, and configurable spend limits.",
    "Built the FuelBuddy design system from scratch and maintained consistency across consumer, B2B, franchise, field, and operational products.",
    "Reduced manual support input by 43% and improved ticket handling and resolution by 57% through restructured support workflows.",
    "Presented design rationale to product, engineering, and business stakeholders, balancing user needs against technical constraints and commercial goals.",
])
role("Product Designer | Uncover by Meddo", "Gurgaon, India | Mar 2022 - May 2023", [
    "Reduced appointment booking from six steps to four, improving completion from 71% to 83% over eight weeks using analytics and user feedback.",
    "Redesigned profile pages, increasing profile views by 28% and appointment requests by 15% in a 5,000-user A/B test.",
    "Conducted usability testing with 12 patients and 8 doctors, translating findings into product, design-system, and engineering priorities.",
    "Designed discovery, booking, membership, records, and back-office journeys across mobile and web.",
])
role("UI Designer | AcadPlaza", "Remote | Jun 2020 - Mar 2022", [
    "Redesigned course catalog and search for a learning marketplace, increasing enrollments by 18% quarter over quarter.",
    "Designed discovery journeys that helped learners find relevant courses faster across responsive web and mobile.",
    "Created wireframes, reusable component patterns, and high-fidelity interfaces with an eight-person product, engineering, and content team.",
])

sec("Selected Live Work")
bullet('<b>Portfolio:</b> <link href="https://workofhayaat.framer.website" color="#155E75">workofhayaat.framer.website</link>')
bullet("<b>AcadPlaza:</b> Learning marketplace course catalog, search, and enrollment discovery journeys. Work predates a public live link; walkthrough available on request.")
bullet('<b>Uncover:</b> Consumer discovery, booking, and membership journeys across responsive web. <link href="https://uncover.co.in/" color="#155E75">uncover.co.in</link>')
bullet('<b>Meddo Patient App (Android):</b> Shipped consumer mobile experience for discovery, appointments, and records. <link href="https://play.google.com/store/apps/details?id=in.meddo.patient&amp;hl=en_IN" color="#155E75">play.google.com/store/apps/details?id=in.meddo.patient</link>')
bullet('<b>FuelBuddy Customer Web App:</b> Consumer and B2B ordering and account experience. <link href="https://app.fuelbuddy.in/" color="#155E75">app.fuelbuddy.in</link>')
bullet('<b>FuelBuddy Android App:</b> Shipped consumer mobile ordering and tracking experience. <link href="https://play.google.com/store/apps/details?id=in.fuelbuddy.app&amp;hl=en_IN" color="#155E75">play.google.com/store/apps/details?id=in.fuelbuddy.app</link>')
bullet('<b>Vgen23:</b> Content-heavy web application simplifying complex clinical and genomic reporting workflows. <link href="https://vgen23.com/" color="#155E75">vgen23.com</link>')
bullet('<b>Maximor AI:</b> Conversion-focused product page for an AI finance-automation platform. <link href="https://www.maximor.ai/cfo-offer-all" color="#155E75">maximor.ai/cfo-offer-all</link>')

sec("Tools and Education")
p("<b>Tools:</b> Figma, FigJam, Framer, Wix, Adobe XD, Adobe Photoshop, Illustrator, After Effects, Rive, Miro, Google Analytics, Hotjar")
p("<b>BBA, Business Administration</b> | Sam Higginbottom University of Agriculture, Technology and Sciences | 2017 - 2020")

SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=.55 * inch,
    rightMargin=.55 * inch,
    topMargin=.45 * inch,
    bottomMargin=.45 * inch,
    title="Mohd Hayaat Ali - Product Designer - Digital Regenesys",
).build(story)
print(OUT)
