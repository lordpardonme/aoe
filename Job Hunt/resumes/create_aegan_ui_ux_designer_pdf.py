from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_UI_UX_Designer_Aegan.pdf")

INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#155E75")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=23, leading=26, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.2, leading=12.9, textColor=ACCENT, spaceAfter=4),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.55, leading=10.8, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.7, leading=12.8, textColor=ACCENT, spaceBefore=6.0, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.15, leading=10.55, textColor=INK, spaceAfter=1.65),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=8.85, leading=10.6, textColor=INK, spaceBefore=2.5),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=7.8, leading=9.4, textColor=MUTED, spaceAfter=1.3),
    "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=7.55, leading=9.95, leftIndent=12, firstLineIndent=-8, spaceAfter=.95, textColor=INK),
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
p("UI/UX DESIGNER | HEALTHCARE, DIGITAL CREATIVES, FIGMA & ADOBE SUITE", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Open to Bangalore discussion", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
p("<b>UI/UX Designer with 6+ years of experience</b> across healthcare, digital products, responsive web/mobile interfaces, brand assets, social creatives, product imagery, and design systems. Strong in Figma, Adobe Photoshop, Illustrator, Adobe XD, presentation-ready visual work, typography, layout, color, stakeholder coordination, and design handoff. Healthcare experience includes patient, doctor, back-office, booking, lab-test, records, and genomics workflow interfaces through Uncover/Meddo and Vgen23-adjacent portfolio work. Current creative role adds practical digital creative, website, campaign, and print-adjacent production experience.")

sec("Core Skills")
p("<b>UI/UX Design:</b> User flows, wireframes, high-fidelity UI, responsive web/mobile design, interaction design, usability testing, design systems, developer handoff")
p("<b>Adobe and Visual Design:</b> Adobe Photoshop, Illustrator, Adobe XD, After Effects, layout design, typography, color, spacing, visual hierarchy, brand assets, product imagery")
p("<b>Digital and Print-Adjacent Creatives:</b> Social creatives, campaign assets, website banners, product visuals, presentation graphics, print-basic layout awareness, marketing collateral support")
p("<b>Healthcare / Pharma Adjacent:</b> Patient journeys, doctor profiles, appointment booking, lab tests, records, back-office workflows, clinical/genomics reporting interfaces")
p("<b>Collaboration:</b> Stakeholder coordination, requirement clarification, product and engineering collaboration, client feedback, cross-functional delivery, presentation support")
p("<b>Tools:</b> Figma, FigJam, Adobe Photoshop, Illustrator, Adobe XD, After Effects, Framer, Wix, Rive, Miro, PowerPoint, Google Analytics, Hotjar")

sec("Professional Experience")
role("Creative Designer | Crevia", "Delhi NCR, India | Jun 2026 - Present", [
    "Create graphics, videos, social content, product imagery, website assets, and campaign material across multiple client brands and fast deadlines.",
    "Design and build responsive website experiences in Wix, covering page structure, product presentation, visual direction, brand consistency, and launch-ready assets.",
    "Edit podcast videos, product images, and campaign content while keeping visual systems consistent across web, social, and marketing touchpoints.",
    "Support brands including Mymy, Al Yamin, Klay Consultants, ATK shoe manufacturer, and other client projects with visual, web, and campaign assets.",
])
role("Product Designer | I-DOD", "New Delhi, India | Jul 2025 - Mar 2026", [
    "Translated founder and stakeholder requirements into user flows, wireframes, prototypes, high-fidelity interfaces, and practical release decisions.",
    "Built a reusable Figma design system from scratch with components, interaction patterns, UI states, and implementation-ready documentation.",
    "Designed onboarding, profile creation, verification, matching, and beta feedback journeys for an early-stage product.",
])
role("Product Designer | FuelBuddy", "Gurgaon, India | Jul 2023 - Jun 2024", [
    "Designed customer, business account, FMS, pilot, driver, and franchise experiences across India and UAE, spanning mobile apps, B2B web products, dashboards, analytics, maps, live tracking, asset management, and account controls.",
    "Redesigned diesel ordering from a 20-22 step journey into a focused location, quantity, schedule, and payment flow, improving completion from 62% to 78%.",
    "Reduced payment transaction errors by 38% through wallet improvements, delegated access, secondary-user controls, and configurable spend limits.",
    "Built the FuelBuddy design system from scratch across consumer, B2B, franchise, field, and operational products.",
])
role("Product Designer | Uncover by Meddo", "Gurgaon, India | Mar 2022 - May 2023", [
    "Reduced appointment booking from six steps to four, improving completion from 71% to 83% over eight weeks using analytics and user feedback.",
    "Redesigned doctor profiles, increasing profile views by 28% and appointment requests by 15% in a 5,000-user A/B test.",
    "Designed patient, doctor, and back-office experiences spanning discovery, appointments, lab tests, records, and early ABHA integration interfaces.",
    "Conducted usability testing with 12 patients and 8 doctors, translating findings into product, design-system, and engineering priorities.",
    "Created Uncover's visual identity foundation and carried it into responsive web, mobile, and reusable UI patterns.",
])
role("UI Designer | AcadPlaza", "Remote | Jun 2020 - Mar 2022", [
    "Redesigned course catalog and search for a learning marketplace, increasing enrollments by 18% quarter over quarter.",
    "Created responsive web and mobile interfaces, wireframes, reusable components, discovery journeys, and visual UI patterns with an eight-person product, engineering, and content team.",
])

sec("Selected Work")
bullet("Portfolio: https://workofhayaat.framer.website")
bullet("Uncover / Meddo: Healthcare product UX, booking flows, patient experience, usability testing, and design-system work. https://uncover.co.in/")
bullet("Vgen23: Genomics reporting platform and healthcare workflow product. https://vgen23.com/")
bullet("FuelBuddy Customer Web App: Customer and B2B account experience across web and mobile. https://app.fuelbuddy.in/")
bullet("Maximor AI: Enterprise AI finance-operations landing page. https://www.maximor.ai/offer")

sec("Education")
p("<b>BBA, Business Administration</b> | Sam Higginbottom University of Agriculture, Technology and Sciences | 2017 - 2020")

SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=.55 * inch,
    rightMargin=.55 * inch,
    topMargin=.45 * inch,
    bottomMargin=.45 * inch,
    title="Mohd Hayaat Ali - UI UX Designer - Aegan",
).build(story)
print(OUT)
