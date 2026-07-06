from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_SAB_Riyadh_Portfolio_Summary.pdf")
INK = colors.HexColor("#18202A")
MUTED = colors.HexColor("#5D6872")
ACCENT = colors.HexColor("#8B1D2C")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=23, leading=26, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.6, leading=13.2, textColor=ACCENT, spaceAfter=4),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.8, leading=11.2, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11.0, leading=13.1, textColor=ACCENT, spaceBefore=6.5, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.7, leading=11.4, textColor=INK, spaceAfter=2.2),
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


p("Mohd Hayaat Ali", "name")
p("PRODUCT DESIGNER | FINTECH, OPERATIONS & DESIGN SYSTEMS", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Open to Riyadh onsite discussion", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
p("<b>6+ years of product design experience</b> across mobile apps, web products, B2B platforms, operational dashboards, internal tools, healthcare, logistics, and fintech-adjacent flows. Strong in Figma, design systems, wireframes, high-fidelity UI, usability testing, and developer handoff. Closest relevant proof for corporate-banking-style work is wallet/payment UX, complex operations screens, and dashboard-heavy product systems.")

sec("Most Relevant Examples")
bullet("FuelBuddy wallet and payment UX: reduced transaction errors by 38%, supported delegated access, multi-user controls, and spend limits.")
bullet("FuelBuddy business and franchise surfaces: dashboards, live tracking, order control, asset management, and reporting workflows.")
bullet("Kama Capital: trading and finance website / conversion flow work.")
bullet("Maximor AI: finance automation landing page and CFO offer flow.")
bullet("TS Logix Peru: logistics and warehouse management software plus public website.")
bullet("Uncover / Meddo: patient, doctor, and back-office product design with measurable booking improvements.")

sec("What I Would Bring")
bullet("Figma design systems and component-based product design.")
bullet("Complex workflow design for finance, operations, and B2B tools.")
bullet("Clear handoff, QA, and collaboration with engineering and product stakeholders.")
bullet("Visual polish with practical, production-minded interface decisions.")

sec("Selected Live Work")
bullet("Portfolio: https://workofhayaat.framer.website")
bullet("FuelBuddy UAE: https://fuelbuddy.ae/")
bullet("FuelBuddy customer web app: https://app.fuelbuddy.in/")
bullet("FuelBuddy Android: https://play.google.com/store/apps/details?id=in.fuelbuddy.app&hl=en_IN")
bullet("FuelBuddy FMS: https://play.google.com/store/apps/details?id=in.fuelbuddy.fms&hl=en_IN")
bullet("Kama Capital: https://kama-capital.com/")
bullet("Maximor AI: https://www.maximor.ai/cfo-offer-all")
bullet("TS Logix Peru: https://tslogixperu.com/")
bullet("Vgen23: https://vgen23.com/")

SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=0.55 * inch,
    rightMargin=0.55 * inch,
    topMargin=0.45 * inch,
    bottomMargin=0.45 * inch,
    title="Mohd Hayaat Ali - SAB Riyadh Portfolio Summary",
).build(story)
print(OUT)
