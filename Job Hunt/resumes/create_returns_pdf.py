from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_Product_Designer_Returns.pdf")

INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#184F7A")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=22, leading=25, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.7, leading=13, textColor=ACCENT, spaceAfter=3),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.35, leading=10.5, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.8, leading=13, textColor=ACCENT, spaceBefore=6, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.28, leading=10.75, textColor=INK, spaceAfter=2),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.05, leading=10.8, textColor=INK, spaceBefore=3),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=7.85, leading=9.4, textColor=MUTED, spaceAfter=1.4),
    "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=7.86, leading=10.15, leftIndent=11, firstLineIndent=-7, spaceAfter=1.25, textColor=INK),
}

story = []


def p(text, style="body"):
    story.append(Paragraph(text, styles[style]))


def sec(text):
    p(text, "section")
    story.append(HRFlowable(width="100%", thickness=0.55, color=colors.HexColor("#C7D2DC"), spaceAfter=2.4))


def bullet(text):
    p("-&nbsp;&nbsp;" + text, "bullet")


def role(title, meta, items):
    p(title, "role")
    p(meta, "meta")
    for item in items:
        bullet(item)


p("Mohd Hayaat Ali", "name")
p("PRODUCT DESIGNER | WEALTH-TECH, FINTECH UX AND DESIGN SYSTEMS", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Open to office-first / relocation discussion", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
story.append(Spacer(1, 3))
p("<b>Product Designer with 6+ years of experience</b> designing mobile and web products across fintech-adjacent flows, payment and wallet UX, B2C journeys, B2B platforms, dashboards, healthcare, logistics, and scalable Figma design systems. Strong fit for Returns through experience simplifying complex transactional journeys, improving conversion and reliability, designing trust-heavy account and payment flows, and collaborating from research and wireframes through polished UI and developer handoff.")

sec("Core Skills")
p("<b>Product and UX:</b> Product discovery, user flows, information architecture, journey mapping, wireframing, interaction design, responsive web and mobile design, prototyping, usability testing, A/B testing, feedback-led iteration")
p("<b>Fintech and Complex Journeys:</b> Payment UX, wallet flows, delegated access, spend limits, KYC, account onboarding, trading/investment website UX, finance automation, trust and error states, conversion-focused product design")
p("<b>Systems and Delivery:</b> Figma, FigJam, Auto Layout, reusable components, design systems, design QA, developer handoff, stakeholder presentations, product-engineering collaboration, startup delivery")

sec("Professional Experience")
role("Creative Designer | Crevia", "Delhi NCR, India | Jun 2026 - Present", [
    "Create graphics, videos, social content, product imagery, website assets, and campaign material across multiple client brands and concurrent timelines.",
    "Design and build responsive website experiences in Wix, covering page structure, product presentation, visual direction, and launch-ready assets.",
])
role("Product Designer | I-DOD", "New Delhi, India | Jul 2025 - Mar 2026", [
    "Turned ambiguous founder and stakeholder requirements into user flows, wireframes, prototypes, high-fidelity interfaces, and release-ready product decisions.",
    "Designed onboarding, KYC verification, profile creation, matching journeys, and beta feedback loops for an early-stage consumer product.",
    "Built a reusable Figma design system from scratch with components, interaction patterns, states, and implementation-ready documentation.",
])
role("Product Designer | FuelBuddy", "Gurgaon, India | Jul 2023 - Jun 2024", [
    "Redesigned diesel ordering from a 20-22 step journey into a focused location, quantity, schedule, and payment flow, improving completion from 62% to 78%.",
    "Reduced payment transaction errors by 38% through wallet UX improvements, delegated access, secondary-user controls, configurable spend limits, and clearer payment states.",
    "Designed customer, business account, FMS, pilot, driver, and franchise experiences across India and UAE, spanning mobile apps, B2B web products, analytics, maps, tracking, asset management, account controls, and dashboards.",
    "Designed business-account flows where registered partners could manage orders, fuel storage, asset fill status, wallet balance, users, delegated access, credit limits, invoices, and payment history.",
    "Built the FuelBuddy design system across consumer, B2B, franchise, field, and operational products, partnering with product and engineering through handoff and design QA.",
])
role("Product Designer | Uncover by Meddo", "Gurgaon, India | Mar 2022 - May 2023", [
    "Reduced appointment booking from six steps to four, improving completion from 71% to 83% over eight weeks using analytics and user feedback.",
    "Redesigned doctor profiles, increasing profile views by 28% and appointment requests by 15% in a 5,000-user A/B test.",
    "Designed patient, doctor, and back-office experiences across discovery, appointments, memberships, lab tests, records, and early ABHA integration interfaces.",
])
role("UI Designer | AcadPlaza", "Remote | Jun 2020 - Mar 2022", [
    "Redesigned course catalog and search for a learning marketplace, increasing enrollments by 18% quarter over quarter.",
    "Created responsive web and mobile interfaces, wireframes, component patterns, and discovery journeys with an eight-person product, engineering, and content team.",
])

sec("Selected Product Work")
bullet("Kama Capital trading website covering forex, commodities, indices, stocks, account types, and onboarding: https://kama-capital.com/")
bullet("Maximor AI finance-automation offer page covering close, reconciliation, reporting, and forecasting: https://www.maximor.ai/cfo-offer-all")
bullet("FuelBuddy consumer ordering, business wallet/account, payment, dashboard, and operations workflows: https://app.fuelbuddy.in/ | https://fuelbuddy.ae/")
bullet("Meddo / Uncover healthcare booking, profile, patient, doctor, and records workflows: https://uncover.co.in/")
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
    title="Mohd Hayaat Ali - Product Designer - Returns",
).build(story)

print(OUT)
