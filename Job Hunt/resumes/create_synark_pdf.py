from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_Product_Designer_Synark.pdf")
INK, MUTED, ACCENT = colors.HexColor("#17212B"), colors.HexColor("#56616B"), colors.HexColor("#0B666A")
b = getSampleStyleSheet()
s = {
 "name": ParagraphStyle("name", parent=b["Normal"], fontName="Helvetica-Bold", fontSize=24, leading=27, textColor=INK),
 "title": ParagraphStyle("title", parent=b["Normal"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=ACCENT, spaceAfter=5),
 "contact": ParagraphStyle("contact", parent=b["Normal"], fontSize=9, leading=12, textColor=MUTED),
 "section": ParagraphStyle("section", parent=b["Normal"], fontName="Helvetica-Bold", fontSize=11.3, leading=14, textColor=ACCENT, spaceBefore=7, spaceAfter=2),
 "body": ParagraphStyle("body", parent=b["Normal"], fontSize=9, leading=12.3, textColor=INK, spaceAfter=2.5),
 "role": ParagraphStyle("role", parent=b["Normal"], fontName="Helvetica-Bold", fontSize=9.7, leading=12, textColor=INK, spaceBefore=4),
 "meta": ParagraphStyle("meta", parent=b["Normal"], fontName="Helvetica-Oblique", fontSize=8.5, leading=10.5, textColor=MUTED, spaceAfter=2),
 "bullet": ParagraphStyle("bullet", parent=b["Normal"], fontSize=8.65, leading=11.8, leftIndent=13, firstLineIndent=-9, spaceAfter=1.8, textColor=INK),
}
story=[]
def p(t,k="body"): story.append(Paragraph(t,s[k]))
def sec(t): p(t,"section"); story.append(HRFlowable(width="100%",thickness=.7,color=colors.HexColor("#C8D4D5"),spaceAfter=3))
def bullet(t): p("-&nbsp;&nbsp;"+t,"bullet")
def role(t,m,items):
 p(t,"role"); p(m,"meta")
 for x in items: bullet(x)

p("Mohd Hayaat Ali","name")
p("PRODUCT DESIGNER | WEB, MOBILE & DESIGN SYSTEMS","title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India | Remote","contact")
p("Portfolio: https://workofhayaat.framer.website","contact")
p("<b>Hands-on Product Designer with 6+ years of experience</b> turning product ideas into user flows, wireframes, interactive prototypes, high-fidelity interfaces, and scalable Figma design systems. Experienced across responsive web, mobile, B2B platforms, dashboards, and internal tools, with project-based delivery from discovery through design QA.")
sec("Core Skills")
p("<b>Product & UX:</b> UX research, user-centered design, information architecture, user flows, wireframes, interaction design, prototypes, usability testing, stakeholder feedback")
p("<b>UI & Systems:</b> High-fidelity UI, responsive web and mobile design, accessibility awareness, typography, color, spacing, layout, design systems, reusable components, Auto Layout")
p("<b>Delivery & Tools:</b> Figma, FigJam, Framer, developer handoff, design QA, task prioritization, deadline management, Photoshop, Illustrator, After Effects, Rive, Miro")
sec("Professional Experience")
role("Creative Designer | Crevia","Delhi NCR | Jun 2026 - Present",["Deliver responsive website assets, product imagery, campaign material, graphics, and video across multiple client brands and concurrent deadlines.","Design and build the Mymy perfume website in Wix, covering page structure, product presentation, and launch-ready assets."])
role("Product Designer | I-DOD","New Delhi | Jul 2025 - Mar 2026",["Translated founder and stakeholder requirements into user flows, wireframes, prototypes, high-fidelity interfaces, and release decisions.","Built a reusable Figma design system from scratch with components, states, patterns, and implementation-ready documentation."])
role("Product Designer | FuelBuddy","Gurgaon | Jul 2023 - Jun 2024",["Designed responsive customer, FMS, pilot, driver, and franchise products across India and UAE spanning web, mobile, dashboards, maps, and tracking.","Redesigned diesel ordering from 20-22 steps, improving completion from 62% to 78%.","Reduced payment errors by 38% through wallet improvements, delegated access, and configurable spend limits.","Built the FuelBuddy design system and partnered with product and engineering through handoff and design QA."])
role("Product Designer | Uncover by Meddo","Gurgaon | Mar 2022 - May 2023",["Improved appointment completion from 71% to 83% using analytics and user feedback.","Conducted usability testing with 12 patients and 8 doctors and translated research into product and engineering priorities.","Created Uncover's brand foundation and carried it into responsive web, mobile, and reusable UI patterns."])
role("UI Designer | AcadPlaza","Remote | Jun 2020 - Mar 2022",["Redesigned course catalog and search, increasing enrollments by 18% quarter over quarter.","Created responsive interfaces, wireframes, and components with an eight-person cross-functional team."])
sec("Selected Live Projects")
bullet("FuelBuddy Customer Web App — https://app.fuelbuddy.in/")
bullet("Vgen23 genetic interpretation and reporting application — https://vgen23.com/")
bullet("TS Logix Peru logistics and WMS work — https://tslogixperu.com/")
bullet("Portfolio — https://workofhayaat.framer.website")
sec("Education")
p("<b>BBA, Business Administration</b> | Sam Higginbottom University | 2017 - 2020")
SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=.58*inch,rightMargin=.58*inch,topMargin=.48*inch,bottomMargin=.48*inch,title="Mohd Hayaat Ali - Product Designer - Synark").build(story)
print(OUT)
