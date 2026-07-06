from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_BlueStone_Product_Designer_Summary.pdf")
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
p("PRODUCT DESIGNER | CONSUMER COMMERCE, TRUST & DESIGN SYSTEMS", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Open to India relocation / hybrid", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
p("<b>6+ years of product design experience</b> across consumer apps, marketplaces, B2B platforms, internal tools, healthcare, logistics, fintech, and brand-led digital work. Strong in turning complex journeys into simpler flows, building reusable design systems, and shipping interfaces with clear handoff and practical execution. The closest relevant proof for BlueStone is consumer discovery, trust building, payment UX, marketplace navigation, and conversion-focused product design.")

sec("Most Relevant Examples")
bullet("FuelBuddy consumer ordering and payment UX: reduced a 20-22 step journey into a focused location, quantity, schedule, and payment flow; improved completion from 62% to 78% and reduced payment errors by 38%.")
bullet("AcadPlaza marketplace search and catalog design: improved discovery and increased enrollments by 18% quarter over quarter.")
bullet("Uncover by Meddo: helped shape a consumer brand and app experience with measurable booking improvements, stronger doctor discovery, and clearer product journeys.")
bullet("Crevia current brand-led work: website assets, product imagery, and launch-ready creative for consumer-facing brand projects including Mymy.")
bullet("FuelBuddy and I-DOD design systems: reusable Figma components, states, patterns, and implementation-ready documentation for product teams.")

sec("What I Would Bring")
bullet("Consumer journey simplification for discovery, product detail, trust, and checkout.")
bullet("Design systems and scalable UI patterns that help teams ship faster without losing polish.")
bullet("Clear collaboration with product and engineering teams on production-minded decisions.")
bullet("Visual discipline for premium products where presentation and confidence matter.")

sec("Selected Live Work")
bullet("Portfolio: https://workofhayaat.framer.website")
bullet("FuelBuddy customer web app: https://app.fuelbuddy.in/")
bullet("FuelBuddy UAE: https://fuelbuddy.ae/")
bullet("FuelBuddy Android app: https://play.google.com/store/apps/details?id=in.fuelbuddy.app&hl=en_IN")
bullet("FuelBuddy FMS: https://play.google.com/store/apps/details?id=in.fuelbuddy.fms&hl=en_IN")
bullet("FuelBuddy Pilot app: https://play.google.com/store/apps/details?id=pilot.fuelbuddy.in&hl=en_IN")
bullet("FuelBuddy Driver app: https://play.google.com/store/apps/details?id=in.fuelbuddy.driver&hl=en_IN")
bullet("Uncover: https://uncover.co.in/")
bullet("Doxper website: https://doxper.com/home/")
bullet("Meddo patient app: https://play.google.com/store/apps/details?id=in.meddo.patient&hl=en_IN")
bullet("Vgen23: https://vgen23.com/")
bullet("TS Logix Peru: https://tslogixperu.com/")
bullet("Maximor AI: https://www.maximor.ai/cfo-offer-all")
bullet("Kama Capital: https://kama-capital.com/")

SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=0.55 * inch,
    rightMargin=0.55 * inch,
    topMargin=0.45 * inch,
    bottomMargin=0.45 * inch,
    title="Mohd Hayaat Ali - BlueStone Product Designer Summary",
).build(story)
print(OUT)
