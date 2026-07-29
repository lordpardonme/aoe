#!/usr/bin/env python3
"""
Render a *-resume.md file into a styled A4 PDF matching the workspace resume
format (same visual system as create_digital_regenesys_product_designer_pdf.py).

Usage:
    python build_pdf_from_md.py <resume.md> <output.pdf> "<pdf title>"

Expected markdown structure:
    # Name
    ## Title line
    contact line(s) before the first '## '
    ## Professional Summary            -> paragraph(s)
    ## Core Skills                     -> **Label:** text paragraphs
    ## Professional Experience         -> ### Role | meta lines, then '- ' bullets
    ## Selected Live Work / Selected Work -> '- ' bullets (URLs auto-linked)
    ## Tools                           -> paragraph
    ## Education                       -> paragraph
"""
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate

INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#56616B")
ACCENT = colors.HexColor("#155E75")

base = getSampleStyleSheet()
S = {
    "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=23, leading=26, textColor=INK),
    "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.4, leading=13.1, textColor=ACCENT, spaceAfter=4),
    "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.65, leading=11.1, textColor=MUTED),
    "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10.8, leading=13.0, textColor=ACCENT, spaceBefore=6.2, spaceAfter=2),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.45, leading=11.05, textColor=INK, spaceAfter=2.0),
    "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.1, leading=11.0, textColor=INK, spaceBefore=3.0),
    "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=8.05, leading=9.8, textColor=MUTED, spaceAfter=1.6),
    "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=7.95, leading=10.55, leftIndent=12, firstLineIndent=-8, spaceAfter=1.25, textColor=INK),
}

URL_RE = re.compile(r"(https?://[^\s)]+)")


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(t):
    # bold **x**, then escape, then linkify (links added after escape via placeholder)
    # handle bold first on raw, escape segments
    out = []
    for i, seg in enumerate(re.split(r"\*\*(.+?)\*\*", t)):
        if i % 2 == 1:
            out.append(f"<b>{esc(seg)}</b>")
        else:
            out.append(esc(seg))
    s = "".join(out)
    # linkify (URLs have no < > & that survive as markup issues except &)
    def repl(m):
        u = m.group(1).replace("&amp;", "&")
        disp = u.replace("https://", "").replace("http://", "").rstrip("/")
        return f'<link href="{u}" color="#155E75">{esc(disp)}</link>'
    return URL_RE.sub(repl, s)


def main():
    md_path, out_path, title = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    lines = md_path.read_text(encoding="utf-8").splitlines()
    story = []
    section = None
    i = 0
    n = len(lines)
    # Header: name, title, contacts
    while i < n and not lines[i].startswith("# "):
        i += 1
    story.append(Paragraph(esc(lines[i][2:].strip()), S["name"]))
    i += 1
    while i < n and not lines[i].startswith("## "):
        i += 1
    story.append(Paragraph(inline(lines[i][3:].strip()).upper().replace("<B>", "<b>").replace("</B>", "</b>").replace("<LINK", "<link").replace("</LINK>", "</link>"), S["title"]))
    i += 1
    # contacts until next '## '
    while i < n and not lines[i].startswith("## "):
        if lines[i].strip():
            story.append(Paragraph(inline(lines[i].strip().rstrip("  ")), S["contact"]))
        i += 1

    def sec(t):
        story.append(Paragraph(esc(t), S["section"]))
        story.append(HRFlowable(width="100%", thickness=.65, color=colors.HexColor("#C8D4D5"), spaceAfter=3))

    while i < n:
        ln = lines[i]
        if ln.startswith("## "):
            section = ln[3:].strip()
            sec(section)
        elif ln.startswith("### "):
            story.append(Paragraph(inline(ln[4:].strip()), S["role"]))
        elif ln.startswith("- "):
            story.append(Paragraph("-&nbsp;&nbsp;" + inline(ln[2:].strip()), S["bullet"]))
        elif ln.strip():
            # meta line under a role (contains '|' and a year) vs body paragraph
            txt = ln.strip()
            if section == "Professional Experience" and "|" in txt and re.search(r"\d{4}", txt):
                story.append(Paragraph(inline(txt), S["meta"]))
            else:
                story.append(Paragraph(inline(txt), S["body"]))
        i += 1

    SimpleDocTemplate(
        str(out_path), pagesize=A4,
        leftMargin=.55 * inch, rightMargin=.55 * inch,
        topMargin=.45 * inch, bottomMargin=.45 * inch,
        title=title,
    ).build(story)
    print("OK", out_path)


if __name__ == "__main__":
    main()
