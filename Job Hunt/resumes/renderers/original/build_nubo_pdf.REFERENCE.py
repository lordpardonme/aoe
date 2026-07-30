#!/usr/bin/env python3
"""
One-off branded renderer for the nubo (eatnubo) application.

Deliberately NOT build_pdf_from_md.py - this is a nubo-only exception so the
shared renderer keeps producing the standard house format for every other role.

Design notes:
  - Palette sampled from nubo's own hiring post: blush pink cards, deep rose
    accent, near-black ink, warm cream page.
  - Type pairs a heavy tight grotesque (Arial Black) for the display/section
    voice against a clean humanist sans (Segoe UI) for reading - the same
    contrast nubo runs between their poster headings and card body copy.
    Poppins/Montserrat are not installed on this machine; these are the closest
    system equivalents and both embed cleanly.

Usage:
    python build_nubo_pdf.py <resume.md> <output.pdf> "<pdf title>"
"""
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

# --- nubo palette ---------------------------------------------------------
INK = colors.HexColor("#141414")   # near-black, as on their cards
ROSE = colors.HexColor("#D9737F")  # deep rose accent
BLUSH = colors.HexColor("#F9DCE0") # card / header pink
CREAM = colors.HexColor("#FDF8F4") # warm page ground
MUTED = colors.HexColor("#6B6B6B")

F = Path("C:/Windows/Fonts")
pdfmetrics.registerFont(TTFont("Display", F / "ariblk.ttf"))
pdfmetrics.registerFont(TTFont("Body", F / "segoeui.ttf"))
pdfmetrics.registerFont(TTFont("BodyB", F / "segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("BodyI", F / "segoeuii.ttf"))
pdfmetrics.registerFont(TTFont("BodyL", F / "segoeuisl.ttf"))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="BodyB", italic="BodyI")

b = getSampleStyleSheet()["Normal"]
S = {
    "name":    ParagraphStyle("name", parent=b, fontName="Display", fontSize=30, leading=32, textColor=INK),
    "title":   ParagraphStyle("title", parent=b, fontName="BodyB", fontSize=10.6, leading=14.5, textColor=ROSE, spaceBefore=5),
    "contact": ParagraphStyle("contact", parent=b, fontName="Body", fontSize=8.8, leading=13.4, textColor=INK),
    "section": ParagraphStyle("section", parent=b, fontName="Display", fontSize=11.6, leading=13.4, textColor=INK, spaceBefore=10, spaceAfter=1),
    "body":    ParagraphStyle("body", parent=b, fontName="Body", fontSize=9.1, leading=12.8, textColor=INK, spaceAfter=4.4),
    "role":    ParagraphStyle("role", parent=b, fontName="BodyB", fontSize=9.8, leading=12.4, textColor=INK, spaceBefore=6.6),
    "meta":    ParagraphStyle("meta", parent=b, fontName="BodyL", fontSize=8.3, leading=10.6, textColor=ROSE, spaceAfter=3.0),
    "bullet":  ParagraphStyle("bullet", parent=b, fontName="Body", fontSize=8.95, leading=12.5,
                              leftIndent=13, firstLineIndent=-13, spaceAfter=3.1, textColor=INK),
    "cardb":   ParagraphStyle("cardb", parent=b, fontName="Body", fontSize=8.95, leading=12.5,
                              leftIndent=13, firstLineIndent=-13, spaceAfter=4.0, textColor=INK),
}

URL_RE = re.compile(r"(https?://[^\s)]+)")


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(t):
    out = []
    for i, seg in enumerate(re.split(r"\*\*(.+?)\*\*", t)):
        out.append(f"<b>{esc(seg)}</b>" if i % 2 else esc(seg))
    s = "".join(out)

    def repl(m):
        u = m.group(1).replace("&amp;", "&")
        disp = u.replace("https://", "").replace("http://", "").rstrip("/")
        return f'<link href="{u}" color="#D9737F"><b>{esc(disp)}</b></link>'
    return URL_RE.sub(repl, s)


def rule(color=ROSE, thickness=2.4, space=7):
    """A short accent bar under a section heading, nubo-poster style."""
    t = Table([[""]], colWidths=[34], rowHeights=[thickness], hAlign="LEFT")
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), color),
                           ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return [t, Spacer(1, space)]


def card(flowables, bg=BLUSH, border=None, pad=13):
    t = Table([[flowables]], colWidths=["100%"])
    style = [("BACKGROUND", (0, 0), (-1, -1), bg),
             ("LEFTPADDING", (0, 0), (-1, -1), pad),
             ("RIGHTPADDING", (0, 0), (-1, -1), pad),
             ("TOPPADDING", (0, 0), (-1, -1), pad),
             ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]
    if border:
        style.append(("LINEBELOW", (0, 0), (-1, -1), 2.2, border))
    t.setStyle(TableStyle(style))
    return t


def page_furniture(canvas, doc):
    """Cream ground on every page, plus a rose footer bar with the page number."""
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, w, h, stroke=0, fill=1)
    canvas.setFillColor(ROSE)
    canvas.rect(0, 0, w, 5.5, stroke=0, fill=1)
    canvas.setFont("Body", 7.6)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.72 * inch, 15, "Mohd Hayaat Ali  ·  360° Marketing Head  ·  nubo")
    canvas.drawRightString(w - 0.72 * inch, 15, f"{doc.page}")
    canvas.restoreState()


def main():
    md_path, out_path, title = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    lines = md_path.read_text(encoding="utf-8").splitlines()
    story, i, n = [], 0, len(lines)

    # ---- header block (name / role / contacts) on a blush card -----------
    while i < n and not lines[i].startswith("# "):
        i += 1
    head = [Paragraph(esc(lines[i][2:].strip()), S["name"])]
    i += 1
    while i < n and not lines[i].startswith("## "):
        i += 1
    head.append(Paragraph(inline(lines[i][3:].strip()).upper(), S["title"]))
    i += 1
    while i < n and not lines[i].startswith("## "):
        if lines[i].strip():
            head.append(Paragraph(inline(lines[i].strip()), S["contact"]))
        i += 1
    story += [card(head, bg=BLUSH, border=ROSE, pad=16), Spacer(1, 4)]

    # ---- body ------------------------------------------------------------
    section = None
    buf = None      # collects the highlighted "What I'd Bring" card
    role = None     # collects one job block so it never splits across pages
    pending = None  # a section heading held back until its first content

    def take_pending():
        nonlocal pending
        p, pending = pending or [], None
        return p

    def flush_role():
        nonlocal role
        if role:
            # heading (if any) travels with the first job block, so a section
            # title can never be left stranded at the foot of a page
            story.append(KeepTogether(take_pending() + role))
            role = None

    def flush_card():
        nonlocal buf
        if buf:
            story.extend(take_pending())
            story.append(card(buf, bg=BLUSH))
            buf = None

    def emit(p):
        story.extend(take_pending())
        story.append(p)

    while i < n:
        ln = lines[i]
        if ln.startswith("## "):
            flush_role()
            flush_card()
            story.extend(take_pending())
            section = ln[3:].strip()
            pending = [Paragraph(esc(section).upper(), S["section"])] + rule()
            if section.lower().startswith("what i'd bring"):
                buf = []
        elif ln.startswith("### "):
            flush_role()
            role = [Paragraph(inline(ln[4:].strip()), S["role"])]
        elif ln.startswith("- "):
            p = Paragraph("<font color='#D9737F'><b>&rarr;</b></font>&nbsp;&nbsp;" + inline(ln[2:].strip()),
                          S["cardb"] if buf is not None else S["bullet"])
            buf.append(p) if buf is not None else role.append(p) if role is not None else emit(p)
        elif ln.strip():
            txt = ln.strip()
            st = S["meta"] if (section == "Professional Experience" and "|" in txt and re.search(r"\d{4}", txt)) else S["body"]
            p = Paragraph(inline(txt), st)
            buf.append(p) if buf is not None else role.append(p) if role is not None else emit(p)
        i += 1
    flush_role()
    flush_card()
    story.extend(take_pending())

    doc = BaseDocTemplate(str(out_path), pagesize=A4, title=title, author="Mohd Hayaat Ali",
                          leftMargin=.62 * inch, rightMargin=.62 * inch,
                          topMargin=.5 * inch, bottomMargin=.55 * inch)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="nubo", frames=[frame], onPage=page_furniture)])
    doc.build(story)
    print("OK", out_path)


if __name__ == "__main__":
    main()
