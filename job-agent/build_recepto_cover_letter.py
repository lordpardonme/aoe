import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

OUT = Path("Job Hunt/resumes/Mohd_Hayaat_Ali_Recepto_Cover_Letter.pdf")

INK = colors.HexColor("#0F172A")
MUTED = colors.HexColor("#475569")
ACCENT = colors.HexColor("#0052FF") # Recepto Brand Blue
RULE = colors.HexColor("#E2E8F0")
LINK = colors.HexColor("#0052FF")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle(
        "Name",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=INK,
        spaceAfter=2,
    ),
    "role": ParagraphStyle(
        "Role",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=ACCENT,
        spaceAfter=4,
    ),
    "contact": ParagraphStyle(
        "Contact",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=MUTED,
        spaceAfter=8,
    ),
    "meta": ParagraphStyle(
        "Meta",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13,
        textColor=INK,
        spaceAfter=8,
    ),
    "heading": ParagraphStyle(
        "Heading",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=INK,
        spaceBefore=8,
        spaceAfter=4,
    ),
    "body": ParagraphStyle(
        "Body",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=13.8,
        textColor=INK,
        spaceAfter=6,
    ),
    "bullet": ParagraphStyle(
        "Bullet",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=INK,
        leftIndent=12,
        firstLineIndent=-12,
        spaceAfter=4,
    ),
}

doc = SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=16 * mm,
    rightMargin=16 * mm,
    topMargin=14 * mm,
    bottomMargin=14 * mm,
)

story = []

# Header
story.append(Paragraph("Mohd Hayaat Ali", styles["name"]))
story.append(Paragraph("Product Designer & Design Systems", styles["role"]))
story.append(
    Paragraph(
        '+91-7905194153 &nbsp;|&nbsp; mohdhayaat1@outlook.com &nbsp;|&nbsp; <a href="https://workofhayaat.framer.website" color="#0052FF"><u>workofhayaat.framer.website</u></a> &nbsp;|&nbsp; Delhi NCR, India',
        styles["contact"],
    )
)
story.append(HRFlowable(width="100%", thickness=0.8, color=RULE, spaceAfter=8))

# Meta
story.append(
    Paragraph(
        '<b>To:</b> The Recepto Team / Hiring Team (hr@recepto.ai)<br/>'
        '<b>Role:</b> High-Trust Product Designer / Design Engineer<br/>'
        '<b>Date:</b> August 31, 2026',
        styles["meta"],
    )
)
story.append(Spacer(1, 3))

# Section 1
story.append(Paragraph("Why this role, and why Recepto", styles["heading"]))
story.append(
    Paragraph(
        "Your job description asks for something rare: not someone to churn out a queue of Figma mockups against a Jira ticket, but someone whose thinking you can trust when there is no ticket yet. "
        "Recepto is building an intent-first GTM engine that monitors 100+ unstructured 3rd-party data streams (Reddit, Slack, LinkedIn, job boards), runs proprietary NLP intent scoring (0–100), and converts messy web signals into automated Plays and enriched pipeline. "
        "In a product like that, the surface UI is only 10% of the iceberg. The real product is how you handle latency, data ambiguity, confidence thresholds, false positives, feedback recalibration loops, and the mental model an SDR needs to trust an AI recommendation. That is the exact kind of messy, high-leverage problem space where I do my best work.",
        styles["body"],
    )
)

# Section 2
story.append(Paragraph("The \"One Thing\": Owned end-to-end, and the number it moved", styles["heading"]))
story.append(
    Paragraph(
        "<b>The Product:</b> FuelBuddy — On-demand energy & fuel delivery platform (180+ cities, 50k+ businesses, 500k+ downloads).<br/>"
        "<b>The Problem:</b> The core ordering journey was a disjointed 20–22 step flow bloated with legacy asset verification fields, genset specs, and unvalidated location logic. Users were dropping off mid-funnel; support teams were manually rescuing failed orders.<br/>"
        "<b>The Solution:</b> Rather than reskinning screens, I tore down the business logic to its fundamental primitives: <b>Location + Quantity + Delivery Window + Payment</b>. I mapped every edge case (offline connectivity for field pilots, geofence mismatch, multi-wallet credit limit delegations, delayed bowser routing) and designed an adaptive state architecture that only requested granular asset data when strictly required for compliance.<br/>"
        "<b>The Number:</b> Lifted end-to-end order completion rate from <b>62% to 78%</b> across consumer and B2B web/app platforms, while reducing checkout drop-off and cutting transaction error rates by <b>38%</b>.",
        styles["body"],
    )
)
story.append(
    Paragraph(
        "Alongside this, I built the company's multi-platform design system from scratch — establishing the component tokens, interaction states, and dev-handoff specs that survived 10x user scaling across India and the UAE without requiring structural rewrites.",
        styles["body"],
    )
)

# Section 3
story.append(Paragraph("How I Think & Build", styles["heading"]))
story.append(
    Paragraph(
        "• <b>Obsessive Edge-Case Hyperfocus:</b> Most portfolios showcase pristine \"happy-path\" screens that break the second real-world data hits them. My brain is wired for edge cases: empty states, partial API returns, confidence score degradation, permission conflicts, and high-cognitive-load conditions. In an AI-native product like Recepto, edge cases <i>are</i> the product experience. I design failure states and degraded modes with the same craft as the primary flow.",
        styles["bullet"],
    )
)
story.append(
    Paragraph(
        "• <b>Systems Over Screens:</b> I build foundational primitives—scalable component architectures, unified token systems, and predictable UX patterns. When you 10x data inputs or roll out new Plays, the system absorbs complexity naturally.",
        styles["bullet"],
    )
)
story.append(
    Paragraph(
        "• <b>Frontend & Engineering Fluency:</b> I understand the constraints of the DOM, state lifecycles, and API latencies. Designing with code reality in mind means zero friction during engineering handoff and zero unbuildable designs.",
        styles["bullet"],
    )
)
story.append(
    Paragraph(
        "• <b>Agency & Commercial Alignment:</b> Freelancing gave me broad exposure, but building high-trust, compound product value in-house is where I belong. I look at where users hesitate, where numbers flatline, and where product logic leaks revenue, frame the problem clearly, and build the solution that moves the needle.",
        styles["bullet"],
    )
)

# Section 4
story.append(Spacer(1, 4))
story.append(
    Paragraph(
        '<b>Portfolio:</b> <a href="https://workofhayaat.framer.website" color="#0052FF"><u>workofhayaat.framer.website</u></a> &nbsp;|&nbsp; '
        '<b>Live Work:</b> <a href="https://app.fuelbuddy.in/" color="#0052FF"><u>FuelBuddy Web</u></a> &nbsp;•&nbsp; '
        '<a href="https://fuelbuddy.ae/" color="#0052FF"><u>FuelBuddy UAE</u></a> &nbsp;•&nbsp; '
        '<a href="https://uncover.co.in/" color="#0052FF"><u>Meddo / Uncover</u></a> &nbsp;•&nbsp; '
        '<a href="https://www.maximor.ai/cfo-offer-all" color="#0052FF"><u>Maximor AI</u></a>',
        styles["contact"],
    )
)
story.append(Spacer(1, 2))
story.append(
    Paragraph(
        "My Master Product Designer CV is attached for full timeline and verified delivery background. I’d welcome 20 minutes to pull apart an active problem at Recepto and show you how I think.<br/><br/>"
        "Warm regards,<br/>"
        "<b>Mohd Hayaat Ali</b>",
        styles["body"],
    )
)

doc.build(story)
print(f"Generated: {OUT}")
