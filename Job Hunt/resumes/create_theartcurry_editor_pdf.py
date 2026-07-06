from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_Creative_Video_Editor_The_Art_Curry.pdf")
INK = colors.HexColor("#161B22")
MUTED = colors.HexColor("#5B6470")
ACCENT = colors.HexColor("#0F6A57")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=23, leading=26, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.8, leading=13.4, textColor=ACCENT, spaceAfter=4),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.8, leading=11.2, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11.0, leading=13.2, textColor=ACCENT, spaceBefore=6.5, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.7, leading=11.4, textColor=INK, spaceAfter=2.2),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.25, leading=11.15, textColor=INK, spaceBefore=3.2),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=8.15, leading=10.0, textColor=MUTED, spaceAfter=1.7),
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


def role(title, meta, items):
    p(title, "role")
    p(meta, "meta")
    for item in items:
        bullet(item)


p("Mohd Hayaat Ali", "name")
p("CREATIVE VIDEO EDITOR | MOTION, VISUAL STORYTELLING & BRAND CONTENT", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Open to Delhi relocation", "contact")
p("Portfolio: https://workofhayaat.framer.website", "contact")
p("<b>Creative designer with hands-on experience</b> across graphics, video editing, website work, social content, product imagery, and brand/project support. I work best where taste, pacing, and polished visual execution matter: shaping edits, refining motion-friendly assets, editing podcast videos, and building launch-ready creative across web and social touchpoints.")

sec("Relevant Skills")
p("<b>Creative Tools:</b> Adobe After Effects, Adobe Photoshop, Illustrator, Figma, Framer, Wix, Miro")
p("<b>Creative Work:</b> video editing, podcast edits, social content, product imagery, website assets, campaign graphics, brand support, visual direction")
p("<b>Delivery Strengths:</b> taste-driven composition, pacing, visual hierarchy, cross-brand consistency, deadline management, client-ready output")

sec("Professional Experience")
role("Creative Designer | Crevia", "Delhi NCR, India | Jun 2026 - Present", [
    "Work spans graphics, video editing, website work, social media posts, product images, and brand/project support across multiple client brands.",
    "Building a Wix website for Mymy, a perfume brand, including visual direction, product presentation, and launch-ready assets.",
    "Editing podcast videos for an industry-focused project and refining product images for client-facing use.",
    "Support creative output across Mymy, Al Yamin, Klay Consultants, ATK shoe manufacturer, and other brand projects.",
])
role("Product Designer | FuelBuddy", "Gurgaon, India | Jul 2023 - Jun 2024", [
    "Designed customer, FMS, pilot, driver, and franchise products across India and UAE, spanning mobile apps, web products, dashboards, maps, live tracking, and account controls.",
    "Built the FuelBuddy design system from scratch across consumer, B2B, franchise, field, and operational products with reusable components and implementation documentation.",
])
role("Product Designer | Uncover by Meddo", "Gurgaon, India | Mar 2022 - May 2023", [
    "Designed patient, doctor, and back-office healthcare experiences across discovery, appointments, memberships, lab tests, digital records, and early ABHA integration interfaces.",
    "Created Uncover's logo and brand foundation, then carried the system into its website, mobile experience, and reusable UI patterns.",
])

sec("Selected Work")
bullet("Showreel: https://drive.google.com/file/d/1RhueHDKvNI4tvzsPcLZgKNXJPfICHI25/view?usp=drivesdk")
bullet("Portfolio: https://workofhayaat.framer.website")
bullet("Mymy perfume website: built in Wix")
bullet("FuelBuddy customer web app: https://app.fuelbuddy.in/")
bullet("Uncover: https://uncover.co.in/")
bullet("Meddo patient app: https://play.google.com/store/apps/details?id=in.meddo.patient&hl=en_IN")

sec("Education")
p("<b>BBA, Business Administration</b> | Sam Higginbottom University of Agriculture, Technology and Sciences | 2017 - 2020")

SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=0.55 * inch,
    rightMargin=0.55 * inch,
    topMargin=0.45 * inch,
    bottomMargin=0.45 * inch,
    title="Mohd Hayaat Ali - Creative Video Editor - The Art Curry",
).build(story)
print(OUT)
