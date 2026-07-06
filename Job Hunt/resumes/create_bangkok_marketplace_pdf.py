from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable

OUT=Path(__file__).with_name("Mohd_Hayaat_Ali_Senior_Product_Designer_Marketplace_Bangkok.pdf")
INK,MUTED,ACCENT=colors.HexColor("#17212B"),colors.HexColor("#56616B"),colors.HexColor("#0B666A")
b=getSampleStyleSheet()
s={"name":ParagraphStyle("name",parent=b["Normal"],fontName="Helvetica-Bold",fontSize=23,leading=26,textColor=INK),"title":ParagraphStyle("title",parent=b["Normal"],fontName="Helvetica-Bold",fontSize=10.7,leading=13,textColor=ACCENT,spaceAfter=4),"contact":ParagraphStyle("contact",parent=b["Normal"],fontSize=8.8,leading=11.5,textColor=MUTED),"section":ParagraphStyle("section",parent=b["Normal"],fontName="Helvetica-Bold",fontSize=11.2,leading=13.5,textColor=ACCENT,spaceBefore=6,spaceAfter=2),"body":ParagraphStyle("body",parent=b["Normal"],fontSize=8.8,leading=12,textColor=INK,spaceAfter=2.2),"role":ParagraphStyle("role",parent=b["Normal"],fontName="Helvetica-Bold",fontSize=9.5,leading=11.5,textColor=INK,spaceBefore=3.5),"meta":ParagraphStyle("meta",parent=b["Normal"],fontName="Helvetica-Oblique",fontSize=8.3,leading=10,textColor=MUTED,spaceAfter=1.5),"bullet":ParagraphStyle("bullet",parent=b["Normal"],fontSize=8.45,leading=11.45,leftIndent=13,firstLineIndent=-9,spaceAfter=1.5,textColor=INK)}
story=[]
def p(t,k="body"):story.append(Paragraph(t,s[k]))
def sec(t):p(t,"section");story.append(HRFlowable(width="100%",thickness=.7,color=colors.HexColor("#C8D4D5"),spaceAfter=2.5))
def bullet(t):p("-&nbsp;&nbsp;"+t,"bullet")
def role(t,m,xs):
 p(t,"role");p(m,"meta")
 for x in xs:bullet(x)
p("Mohd Hayaat Ali","name");p("SENIOR PRODUCT DESIGNER | COMMERCE JOURNEYS, OPERATIONS & DESIGN SYSTEMS","title")
p("mohdhayaat1@outlook.com | +91-7905194153 | Delhi NCR, India","contact");p("Portfolio: https://workofhayaat.framer.website | Open to Bangkok relocation, subject to work authorization","contact")
p("<b>Senior Product Designer with 6+ years of experience</b> designing connected customer journeys, operational platforms, responsive web and mobile products, and scalable design systems. Strong record partnering with PMs, engineers, founders, and stakeholders to improve funnel completion, payment reliability, trust, and service delivery.")
sec("Core Capabilities")
p("<b>Product Strategy & UX:</b> Product thinking, UX strategy, user research, journey mapping, information architecture, user flows, service design, prototyping, usability testing, experimentation, product metrics")
p("<b>Commerce & Operations:</b> Customer ordering, payment and wallet UX, account controls, delegated access, fulfillment workflows, internal operations, dashboards, support systems, trust and error states")
p("<b>UI & Delivery:</b> High-fidelity UI, responsive design, design systems, Figma components, accessibility awareness, developer handoff, design QA, stakeholder management")
sec("Professional Experience")
role("Creative Designer | Crevia","Delhi NCR | Jun 2026 - Present",["Deliver responsive websites, product imagery, campaign assets, graphics, and video across multiple client brands and concurrent deadlines."])
role("Product Designer | I-DOD","New Delhi | Jul 2025 - Mar 2026",["Partnered with founders and developers to turn ambiguous requirements into user flows, prototypes, high-fidelity interfaces, and release decisions.","Built a reusable Figma design system from scratch with components, states, patterns, and implementation-ready documentation."])
role("Product Designer | FuelBuddy","Gurgaon | Jul 2023 - Jun 2024",["Designed connected customer ordering and operational workflows across India and UAE spanning web, mobile, dashboards, tracking, fulfillment, and account controls.","Redesigned diesel ordering from 20-22 steps, improving completion from 62% to 78%.","Reduced payment errors by 38% through wallet improvements, delegated access, and configurable spend limits.","Replaced spreadsheet-heavy operations with workflows for drivers, trucks, routes, shifts, delivery planning, corrections, and reports.","Reduced manual support input by 43% and improved ticket handling and resolution by 57%.","Built the FuelBuddy design system and collaborated with product and engineering through handoff and design QA."])
role("Product Designer | Uncover by Meddo","Gurgaon | Mar 2022 - May 2023",["Improved appointment completion from 71% to 83% using analytics and user feedback.","Increased doctor-profile views by 28% and appointment requests by 15% in a 5,000-user A/B test.","Conducted usability testing with 12 patients and 8 doctors and translated findings into product and engineering priorities."])
role("UI Designer | AcadPlaza","Remote | Jun 2020 - Mar 2022",["Redesigned catalog and search for a learning marketplace, increasing enrollments by 18% quarter over quarter.","Created responsive interfaces, wireframes, and components with an eight-person cross-functional team."])
sec("Selected Live Projects")
bullet("FuelBuddy Customer Web App — https://app.fuelbuddy.in/");bullet("TS Logix Peru logistics and WMS work — https://tslogixperu.com/");bullet("Vgen23 complex reporting application — https://vgen23.com/");bullet("Portfolio — https://workofhayaat.framer.website")
sec("Tools & Education")
p("<b>Tools:</b> Figma, FigJam, Framer, Photoshop, Illustrator, After Effects, Rive, Miro, Adobe XD, Google Analytics, Hotjar")
p("<b>BBA, Business Administration</b> | Sam Higginbottom University | 2017 - 2020")
SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=.55*inch,rightMargin=.55*inch,topMargin=.44*inch,bottomMargin=.44*inch,title="Mohd Hayaat Ali - Senior Product Designer Marketplace Bangkok").build(story)
print(OUT)
