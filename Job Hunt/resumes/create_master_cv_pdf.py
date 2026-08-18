from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

OUT = Path(__file__).with_name("Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf")

INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#0B666A")
RULE = colors.HexColor("#C8D4D5")
LINK = colors.HexColor("#0B666A")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle(
        "Name",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=29,
        textColor=INK,
        spaceAfter=3,
    ),
    "title": ParagraphStyle(
        "Title",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=ACCENT,
        spaceAfter=7,
    ),
    "contact": ParagraphStyle(
        "Contact",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9.4,
        leading=13.2,
        textColor=MUTED,
        spaceAfter=2,
    ),
    "summary": ParagraphStyle(
        "Summary",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        textColor=INK,
        spaceBefore=8,
        spaceAfter=7,
    ),
    "section": ParagraphStyle(
        "Section",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12.4,
        leading=15,
        textColor=ACCENT,
        spaceBefore=12,
        spaceAfter=3,
    ),
    "role": ParagraphStyle(
        "Role",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.7,
        leading=13.5,
        textColor=INK,
        spaceBefore=7,
        spaceAfter=1,
    ),
    "meta": ParagraphStyle(
        "Meta",
        parent=base["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9.2,
        leading=12,
        textColor=MUTED,
        spaceAfter=5,
    ),
    "body": ParagraphStyle(
        "Body",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.8,
        textColor=INK,
        spaceAfter=4,
    ),
    "bullet": ParagraphStyle(
        "Bullet",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9.35,
        leading=13.4,
        textColor=INK,
        leftIndent=15,
        firstLineIndent=-10,
        bulletIndent=0,
        spaceAfter=3.0,
    ),
    "compact": ParagraphStyle(
        "Compact",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9.15,
        leading=13.1,
        textColor=INK,
        spaceAfter=3,
    ),
}


def section(title):
    return [
        Paragraph(title, styles["section"]),
        HRFlowable(width="100%", thickness=0.8, color=RULE, spaceBefore=0, spaceAfter=5),
    ]


def bullet(text):
    return Paragraph(f"-&nbsp;&nbsp;{text}", styles["bullet"])


def role(title, meta, bullets):
    items = [
        Paragraph(title, styles["role"]),
        Paragraph(meta, styles["meta"]),
    ]
    items.extend(bullet(item) for item in bullets)
    items.append(Spacer(1, 4))
    return items


def linked(label, url):
    return f'<link href="{url}" color="#0B666A"><u>{label}</u></link>'


story = [
    Paragraph("Mohd Hayaat Ali", styles["name"]),
    Paragraph("PRODUCT DESIGNER | UI/UX, INTERACTION AND VISUAL SYSTEMS", styles["title"]),
    Paragraph(
        f'{linked("mohdhayaat1@outlook.com", "mailto:mohdhayaat1@outlook.com")}  |  '
        f'{linked("+91-7905194153", "tel:+917905194153")}  |  Delhi NCR, India',
        styles["contact"],
    ),
    Paragraph(
        f'{linked("Portfolio", "https://workofhayaat.framer.website")}  |  '
        "Open to relocation and remote opportunities",
        styles["contact"],
    ),
    Paragraph(
        "<b>Product and UI/UX designer with 6+ years of experience</b> across shipped mobile apps, "
        "web products, B2B platforms, internal tools, healthcare, fuel-tech, logistics, fintech, "
        "AI automation, e-commerce, and brand-led digital experiences. I work from problem framing "
        "and user flows through wireframes, high-fidelity UI, prototypes, design systems, usability "
        "testing, and developer handoff. My strongest work simplifies complex operational journeys "
        "while maintaining clear interaction patterns and polished visual execution.",
        styles["summary"],
    ),
]

story.extend(section("Core Capabilities"))
for line in [
    "<b>Product and UX:</b> Product discovery, user flows, information architecture, journey mapping, "
    "wireframing, interaction design, responsive web and mobile design, prototyping, usability testing, A/B testing",
    "<b>Systems and Delivery:</b> Design systems, Figma components, Auto Layout, component documentation, "
    "accessibility awareness, developer handoff, design QA, stakeholder presentations, product and engineering collaboration",
    "<b>Domain Experience:</b> B2B SaaS, operational dashboards, internal tools, payment and wallet UX, KYC, "
    "logistics and fleet workflows, healthcare journeys, marketplaces, AI and finance automation, consumer brands",
]:
    story.append(Paragraph(line, styles["compact"]))

story.extend(section("Professional Experience"))
story.extend(
    role(
        "Creative Designer | Crevia",
        "Delhi NCR, India | June 2026 - Present",
        [
            "Create graphics, videos, social content, product imagery, website assets, and campaign material across "
            "brands including Mymy, Al Yamin, Klay Consultants, ATK Shoe Manufacturer, and other client projects.",
            "Designed social posts and reels for ATK Designs and Klay Consultants that generated 30,000+ views; "
            "ad creative for La Well and Herbal Hand Jatibooti drove 10,00,000+ ad views.",
            "Designed 200+ product creatives across La Well's 35-product catalog for their Amazon store and "
            "website; currently redesigning the ATK Designs website.",
            "Design and build the Mymy perfume-brand website in Wix, covering responsive page structure, product "
            "presentation, visual direction, and launch-ready assets.",
            "Edit podcast videos, product images, and campaign content while maintaining consistent visual systems "
            "across web and social touchpoints.",
        ],
    )
)
story.extend(
    role(
        "Product Designer | I-DOD",
        "New Delhi, India | July 2025 - March 2026",
        [
            "Designed onboarding, KYC verification, profile creation, matching journeys, and beta feedback loops "
            "for an early-stage relationship platform.",
            "Built the design system from scratch with reusable Figma components, interaction patterns, states, "
            "and implementation-ready documentation.",
            "Worked directly with founders and developers to turn ambiguous requirements into user flows, "
            "prototypes, high-fidelity interfaces, and practical release decisions.",
        ],
    )
)
story.extend(
    role(
        "Product Designer | FuelBuddy",
        "Gurgaon, India | July 2023 - June 2024",
        [
            "Redesigned diesel ordering from a 20-22 step journey into a focused location, quantity, schedule, "
            "and payment flow, improving completion from 62% to 78%.",
            "Reduced payment transaction errors by 38% through wallet improvements, delegated access, "
            "secondary-user controls, and configurable spend limits.",
            "Designed customer, FMS, pilot, and driver experiences across India and UAE, spanning mobile apps, "
            "B2B web products, analytics, maps, live tracking, asset management, and account controls.",
            "Replaced spreadsheet-heavy franchise operations with tools for trucks, drivers, routes, bowsers, "
            "shifts, delivery planning, quantity correction, reports, and operational status management.",
            "Reduced manual support input by 43% and improved ticket handling and resolution by 57% through "
            "structured support and ticketing workflows.",
            "Built the FuelBuddy design system from scratch across consumer, B2B, franchise, field, and operational products.",
        ],
    )
)

story.extend(
    role(
        "Product Designer | Uncover by Meddo",
        "Gurgaon, India | March 2022 - May 2023",
        [
            "Reduced appointment booking from six steps to four, improving completion from 71% to 83% over eight "
            "weeks using analytics and user feedback.",
            "Redesigned doctor profiles, increasing profile views by 28% and appointment requests by 15% in a "
            "5,000-user A/B test.",
            "Designed patient, doctor, and back-office experiences spanning discovery, appointments, healthcare "
            "memberships, lab tests, digital records, and early ABHA integration interfaces.",
            "Conducted usability testing with 12 patients and 8 doctors, translating findings into product, "
            "design-system, and engineering priorities.",
            "Created Uncover's logo and brand foundation, then carried the system into its website, mobile "
            "experience, and reusable UI patterns.",
        ],
    )
)
story.extend(
    role(
        "UI Designer | AcadPlaza",
        "Remote | June 2020 - March 2022",
        [
            "Redesigned course catalog and search for a learning marketplace, increasing enrollments by 18% quarter over quarter.",
            "Created responsive web and mobile interfaces, wireframes, component patterns, and discovery journeys "
            "with an eight-person product, engineering, and content team.",
        ],
    )
)

story.extend(section("Selected Consulting and Product Work"))
for item in [
    f'<b>Vgen23:</b> Genetic interpretation and reporting web app for clinical and genomic workflows. '
    f'{linked("Live product", "https://vgen23.com/")}',
    f'<b>TS Logix Peru:</b> Public website and internal WMS for logistics, inventory, warehousing, and '
    f'pharmaceutical distribution. {linked("Live website", "https://tslogixperu.com/")}',
    f'<b>Maximor AI:</b> Conversion-focused CFO offer page for AI finance automation across close, reconciliation, '
    f'reporting, and forecasting. {linked("Live page", "https://www.maximor.ai/cfo-offer-all")}',
    f'<b>Kama Capital:</b> Multi-asset trading website covering forex, commodities, indices, stocks, account types, '
    f'and onboarding. {linked("Live website", "https://kama-capital.com/")}',
    f'<b>Doxper and Meddo:</b> Doctor application, website, patient experience, design system, and digitised '
    f'healthcare workflows. {linked("Doxper", "https://doxper.com/home/")}',
    "<b>Gaming and consumer brands:</b> Casino and iGaming landing pages, platform flows, and visual systems; "
    "additional work includes Gamemano, Vgenomics, Arata Hair Care, and other client products.",
]:
    story.append(bullet(item))

story.extend(section("Selected Live Work"))
story.append(
    Paragraph(
        f'{linked("Portfolio", "https://workofhayaat.framer.website")}  |  '
        f'{linked("FuelBuddy Web App", "https://app.fuelbuddy.in/")}  |  '
        f'{linked("FuelBuddy UAE", "https://fuelbuddy.ae/")}  |  '
        f'{linked("FuelBuddy Android", "https://play.google.com/store/apps/details?id=in.fuelbuddy.app")}',
        styles["compact"],
    )
)
story.append(
    Paragraph(
        f'{linked("FuelBuddy FMS", "https://play.google.com/store/apps/details?id=in.fuelbuddy.fms")}  |  '
        f'{linked("Uncover", "https://uncover.co.in/")}  |  '
        f'{linked("Meddo Patient App", "https://play.google.com/store/apps/details?id=in.meddo.patient")}',
        styles["compact"],
    )
)

story.extend(section("Tools"))
story.append(
    Paragraph(
        "Figma, FigJam, Framer, Wix, Adobe Photoshop, Illustrator, After Effects, Rive, Miro, Adobe XD, "
        "Google Analytics, Hotjar",
        styles["body"],
    )
)

story.extend(section("Education"))
story.append(Paragraph("<b>BBA, Business Administration</b>", styles["body"]))
story.append(
    Paragraph(
        "Sam Higginbottom University of Agriculture, Technology and Sciences | 2017 - 2020",
        styles["compact"],
    )
)

doc = SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=0.65 * inch,
    rightMargin=0.65 * inch,
    topMargin=0.58 * inch,
    bottomMargin=0.58 * inch,
    title="Mohd Hayaat Ali - Master Product Designer CV",
    author="Mohd Hayaat Ali",
    subject="Product Design, UI/UX, Interaction Design and Visual Systems",
)
doc.build(story)
print(OUT)





