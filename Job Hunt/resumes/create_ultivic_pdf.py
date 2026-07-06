from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_Senior_UI_UX_Designer_Ultivic.pdf")
INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#0B666A")
base = getSampleStyleSheet()
s = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=24, leading=27, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=ACCENT, spaceAfter=5),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=9, leading=12, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=ACCENT, spaceBefore=8, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=9.2, leading=12.6, textColor=INK, spaceAfter=3),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.8, leading=12, textColor=INK, spaceBefore=5),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=8.6, leading=11, textColor=MUTED, spaceAfter=2),
    "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=8.8, leading=12.1, leftIndent=13, firstLineIndent=-9, spaceAfter=2, textColor=INK),
}

story = []
def p(text, style="body"): story.append(Paragraph(text, s[style]))
def section(text):
    p(text, "section")
    story.append(HRFlowable(width="100%", thickness=.7, color=colors.HexColor("#C8D4D5"), spaceAfter=3))
def bullet(text): p("-&nbsp;&nbsp;" + text, "bullet")
def role(title, meta, items):
    p(title, "role"); p(meta, "meta")
    for item in items: bullet(item)

p("Mohd Hayaat Ali", "name")
p("SENIOR UI/UX DESIGNER | PRODUCT DESIGN, DESIGN SYSTEMS & CLIENT DELIVERY", "title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India", "contact")
p("Portfolio: https://workofhayaat.framer.website | Open to relocate to Mohali", "contact")
p("<b>Senior UI/UX and Product Designer with 6+ years of hands-on experience</b> designing responsive web and mobile products, B2B platforms, internal tools, and reusable design systems. Experienced in translating client and stakeholder requirements into user flows, wireframes, prototypes, polished interfaces, and implementation-ready specifications.")
section("Core Skills")
p("<b>UI/UX:</b> User flows, information architecture, wireframing, interaction design, responsive web and mobile UI, prototyping, usability testing, A/B testing")
p("<b>Team & Client Delivery:</b> Requirement clarification, stakeholder presentations, client collaboration, design reviews, developer handoff, design QA, cross-functional delivery")
p("<b>Systems & Tools:</b> Design systems, Figma components, Auto Layout, Figma, FigJam, Framer, Photoshop, Illustrator, After Effects, Rive, Miro, Adobe XD")
section("Professional Experience")
role("Creative Designer | Crevia", "Delhi NCR | Jun 2026 - Present", ["Deliver website assets, product imagery, campaign material, social content, graphics, and video across multiple client brands.", "Design and build the responsive Mymy perfume website in Wix, covering product presentation and visual direction."])
role("Product Designer | I-DOD", "New Delhi | Jul 2025 - Mar 2026", ["Worked directly with founders and developers to turn ambiguous requirements into user flows, prototypes, high-fidelity interfaces, and release decisions.", "Built a reusable Figma design system from scratch with components, states, patterns, and implementation-ready documentation."])
role("Product Designer | FuelBuddy", "Gurgaon | Jul 2023 - Jun 2024", ["Designed customer, FMS, pilot, driver, and franchise experiences across India and UAE spanning mobile apps, B2B web products, dashboards, tracking, and account controls.", "Redesigned diesel ordering from 20-22 steps, improving completion from 62% to 78%.", "Reduced payment transaction errors by 38% through wallet improvements, delegated access, and configurable spend limits.", "Built the FuelBuddy design system and partnered with product and engineering through handoff and design QA."])
role("Product Designer | Uncover by Meddo", "Gurgaon | Mar 2022 - May 2023", ["Improved appointment completion from 71% to 83% using analytics and user feedback.", "Redesigned doctor profiles, increasing views by 28% and appointment requests by 15% in a 5,000-user A/B test.", "Conducted usability testing with 12 patients and 8 doctors and translated findings into product and engineering priorities."])
role("UI Designer | AcadPlaza", "Remote | Jun 2020 - Mar 2022", ["Redesigned course catalog and search, increasing enrollments by 18% quarter over quarter.", "Created responsive interfaces, wireframes, and components with an eight-person cross-functional team."])
section("Selected Product Work")
bullet("TS Logix Peru: Public website and internal WMS for logistics and inventory workflows.")
bullet("Vgen23: Genetic interpretation and reporting web application for complex clinical workflows.")
bullet("Maximor AI and Kama Capital: AI finance and trading web experiences with conversion and onboarding flows.")
section("Education")
p("<b>BBA, Business Administration</b> | Sam Higginbottom University | 2017 - 2020")

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=.58*inch, rightMargin=.58*inch, topMargin=.48*inch, bottomMargin=.48*inch, title="Mohd Hayaat Ali - Ultivic Senior UI UX Designer")
doc.build(story)
print(OUT)
