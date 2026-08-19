#!/usr/bin/env python3
"""
Generate a 1-page branded Cover Letter PDF for Bling Ping Post-Production Lead application.
"""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

FONT_DIR = Path("C:/Windows/Fonts")
pdfmetrics.registerFont(TTFont("Display", FONT_DIR / "ariblk.ttf"))
pdfmetrics.registerFont(TTFont("Body", FONT_DIR / "segoeui.ttf"))
pdfmetrics.registerFont(TTFont("BodyB", FONT_DIR / "segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("BodyI", FONT_DIR / "segoeuii.ttf"))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="BodyB", italic="BodyI")

RAW = colors.HexColor("#D81B60")
ACCENT = colors.Color(RAW.red * 0.82, RAW.green * 0.82, RAW.blue * 0.82)
ACCENT_HEX = "#%02X%02X%02X" % (int(ACCENT.red * 255), int(ACCENT.green * 255), int(ACCENT.blue * 255))
CARD = colors.Color(RAW.red + (1 - RAW.red) * 0.88,
                    RAW.green + (1 - RAW.green) * 0.88,
                    RAW.blue + (1 - RAW.blue) * 0.88)
PAGE = colors.Color(RAW.red + (1 - RAW.red) * 0.975,
                    RAW.green + (1 - RAW.green) * 0.975,
                    RAW.blue + (1 - RAW.blue) * 0.975)
INK = colors.HexColor("#141414")
MUTED = colors.HexColor("#6B6B6B")

b = getSampleStyleSheet()["Normal"]
S = {
    "name": ParagraphStyle("name", parent=b, fontName="Display", fontSize=24, leading=27, textColor=INK),
    "title": ParagraphStyle("title", parent=b, fontName="BodyB", fontSize=10.5, leading=14, textColor=ACCENT, spaceBefore=4),
    "contact": ParagraphStyle("contact", parent=b, fontName="Body", fontSize=8.8, leading=13.5, textColor=INK),
    "date": ParagraphStyle("date", parent=b, fontName="BodyB", fontSize=9.5, leading=14, textColor=MUTED, spaceBefore=14, spaceAfter=8),
    "recipient": ParagraphStyle("recipient", parent=b, fontName="BodyB", fontSize=10, leading=14.5, textColor=INK, spaceAfter=12),
    "body": ParagraphStyle("body", parent=b, fontName="Body", fontSize=9.5, leading=14.8, textColor=INK, spaceAfter=9),
    "bullet": ParagraphStyle("bullet", parent=b, fontName="Body", fontSize=9.2, leading=14.2, leftIndent=12, firstLineIndent=-12, spaceAfter=5, textColor=INK),
    "sign": ParagraphStyle("sign", parent=b, fontName="Body", fontSize=9.5, leading=14.5, textColor=INK, spaceBefore=10),
    "sign_name": ParagraphStyle("sign_name", parent=b, fontName="BodyB", fontSize=10.5, leading=14, textColor=INK, spaceBefore=4),
}

def furniture(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(PAGE); canvas.rect(0, 0, w, h, stroke=0, fill=1)
    canvas.setFillColor(ACCENT); canvas.rect(0, 0, w, 5.5, stroke=0, fill=1)
    canvas.setFont("Body", 7.6); canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 15, "Mohd Hayaat Ali — Cover Letter | Post-Production Lead")
    canvas.drawRightString(w - doc.leftMargin, 15, "1")
    canvas.restoreState()

def build_cover_letter(out_path):
    head = [
        Paragraph("Mohd Hayaat Ali", S["name"]),
        Paragraph("POST-PRODUCTION LEAD & CREATIVE DIRECTOR", S["title"]),
        Paragraph("mohdhayaat1@outlook.com | +91-7905194153 | Mumbai, India", S["contact"]),
        Paragraph(f'Portfolio: <link href="https://workofhayaat.framer.website" color="{ACCENT_HEX}"><b>workofhayaat.framer.website</b></link> | Showreel: <link href="https://drive.google.com/drive/folders/1maf7S6y-WwfE3cdVNO8SvmM7H6slgpZW" color="{ACCENT_HEX}"><b>Drive Showreel</b></link>', S["contact"])
    ]
    head_table = Table([[head]], colWidths=["100%"])
    head_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LINEBELOW", (0, 0), (-1, -1), 2.2, ACCENT)
    ]))

    story = [
        head_table,
        Spacer(1, 10),
        Paragraph("August 19, 2026", S["date"]),
        Paragraph("Hiring Team<br/><b>Bling Ping</b><br/>Mumbai, India", S["recipient"]),
        Paragraph("<b>Subject: Application for Post-Production Lead</b>", ParagraphStyle("subj", parent=b, fontName="BodyB", fontSize=10.5, leading=15, textColor=ACCENT, spaceAfter=10)),
        Paragraph("Dear Bling Ping Team,", S["body"]),
        Paragraph("I am writing to formally apply for the <b>Post-Production Lead</b> position at Bling Ping in Mumbai. With over a decade of hands-on post-production experience spanning commercial campaigns, music videos, and multi-stream digital content, I specialize in building disciplined editing workflows, enforcing rigorous quality control, and ensuring fast turnaround on high-volume deliverables.", S["body"]),
        Paragraph("Currently operating as a Creative Designer and Post-Production Lead, I supervise full post-production pipelines from raw ingestion and multi-cam synchronization to final grade, sound mix, and multi-format delivery. Key highlights of what I manage and deliver include:", S["body"]),
        Paragraph(f"<font color='{ACCENT_HEX}'><b>&rarr;</b></font>&nbsp;&nbsp;<b>End-to-End Workflow Management:</b> Structured post-production pipelines across 5+ active client brands at Crevia, reducing standard project turnaround from 5 days to 48 hours with zero QA defects.", S["bullet"]),
        Paragraph(f"<font color='{ACCENT_HEX}'><b>&rarr;</b></font>&nbsp;&nbsp;<b>Commercial & High-Impact Content:</b> Cut, graded, and finished ad campaigns for brands like Red Bull, Monster Energy, Hero, and Suzuki, including campaigns that generated 10,00,000+ views.", S["bullet"]),
        Paragraph(f"<font color='{ACCENT_HEX}'><b>&rarr;</b></font>&nbsp;&nbsp;<b>Strict Quality Assurance:</b> Enforcing flawless color grading (DaVinci Resolve), audio mastering, and aspect-ratio specific framing (16:9, 9:16 reels) before client delivery.", S["bullet"]),
        Paragraph(f"<font color='{ACCENT_HEX}'><b>&rarr;</b></font>&nbsp;&nbsp;<b>Turnaround & Artist Reels:</b> Delivered same-night festival and concert edits for 100+ national and international artists across premier institutional stages (IITs, IIMs, DU).", S["bullet"]),
        Paragraph("I am currently based in Mumbai, equipped with my own dedicated high-performance editing and grading workstation, and available to take full ownership of your post-production pipeline immediately.", S["body"]),
        Paragraph("My complete resume is attached, and you can view my showreel and portfolio at the links above. I would welcome the opportunity to discuss how I can elevate and streamline Bling Ping’s post-production operations.", S["body"]),
        Paragraph("Sincerely,", S["sign"]),
        Paragraph("Mohd Hayaat Ali", S["sign_name"]),
        Paragraph("+91-7905194153 | mohdhayaat1@outlook.com", S["contact"])
    ]

    doc = BaseDocTemplate(str(out_path), pagesize=A4, title="Mohd Hayaat Ali - Cover Letter - Bling Ping", author="Mohd Hayaat Ali",
                          leftMargin=.75 * inch, rightMargin=.75 * inch,
                          topMargin=.6 * inch, bottomMargin=.6 * inch)
    doc.addPageTemplates([PageTemplate(id="p", frames=[
        Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f",
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=furniture)])
    doc.build(story)
    print(f"OK {out_path} [Cover Letter PDF built]")

if __name__ == "__main__":
    build_cover_letter(Path("Job Hunt/resumes/Mohd_Hayaat_Ali_Cover_Letter_Bling_Ping.pdf"))
