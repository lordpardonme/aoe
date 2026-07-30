#!/usr/bin/env python3
"""
Brand-matched resume renderer. Generalised from the one-off nubo build.

Takes any *-resume.md and renders it in a target company's colours and type,
so the packet looks like it was made for them specifically.

    python build_branded_pdf.py <resume.md> <out.pdf> "<title>" --accent "#D9737F"
    python build_branded_pdf.py ... --preset nubo
    python build_branded_pdf.py ... --accent "#A100FF" --ats     # ATS-safe

WHEN TO USE WHICH MODE
  branded (default) - cafes, studios, agencies-as-employers, DTC brands, small
      creative teams. A human opens the PDF and design taste is part of the job.
  --ats             - large corporates, banks, anything with a real ATS, and
      recruitment agencies who reformat CVs into their own template. Drops the
      tinted cards and rules to flat, single-column, parser-safe text while
      keeping the accent colour on headings only.

Accent colour is the only thing you must get right; the page tint is derived
from it, and low-contrast accents are darkened automatically for legibility.
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

# Verified brand accents. Add as you research them - never guess a colour you
# have not actually seen on the company's own material.
PRESETS = {
    "nubo":      "#D9737F",  # sampled from their hiring post
    "ikea":      "#0058A3",  # IKEA blue, from their published brand identity
    "mono":      "#000000",  # flat black - agencies, ATS, anything that reformats
    "default":   "#155E75",
}

# Font pairings available from stock Windows fonts. display = heavy grotesque
# for the name/headings, body = humanist sans for reading.
PAIRINGS = {
    "grotesque": {"display": "ariblk.ttf", "body": "segoeui.ttf",
                  "bold": "segoeuib.ttf", "italic": "segoeuii.ttf", "light": "segoeuisl.ttf"},
    "condensed": {"display": "bahnschrift.ttf", "body": "segoeui.ttf",
                  "bold": "segoeuib.ttf", "italic": "segoeuii.ttf", "light": "segoeuisl.ttf"},
    "clean":     {"display": "segoeuib.ttf", "body": "segoeui.ttf",
                  "bold": "segoeuib.ttf", "italic": "segoeuii.ttf", "light": "segoeuisl.ttf"},
}

FONT_DIR = Path("C:/Windows/Fonts")
URL_RE = re.compile(r"(https?://[^\s)]+)")


def luminance(c):
    return 0.2126 * c.red + 0.7152 * c.green + 0.0722 * c.blue


def readable(c, limit=0.62):
    """Darken an accent until it is legible as text on a light page."""
    while luminance(c) > limit:
        c = colors.Color(c.red * 0.82, c.green * 0.82, c.blue * 0.82)
    return c


def tint(c, amount=0.88):
    """Derive the soft card wash from the accent."""
    return colors.Color(c.red + (1 - c.red) * amount,
                        c.green + (1 - c.green) * amount,
                        c.blue + (1 - c.blue) * amount)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def make_inline(accent_hex):
    def inline(t):
        out = []
        for i, seg in enumerate(re.split(r"\*\*(.+?)\*\*", t)):
            out.append(f"<b>{esc(seg)}</b>" if i % 2 else esc(seg))
        s = "".join(out)

        def repl(m):
            u = m.group(1).replace("&amp;", "&")
            disp = u.replace("https://", "").replace("http://", "").rstrip("/")
            return f'<link href="{u}" color="{accent_hex}"><b>{esc(disp)}</b></link>'
        return URL_RE.sub(repl, s)
    return inline


def parse_args(argv):
    def opt(name, default=None):
        return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else default

    ats = "--ats" in argv
    preset = opt("--preset")
    accent = opt("--accent") or PRESETS.get((preset or "").lower(), PRESETS["default"])
    pairing = opt("--font", "grotesque")

    pos, i = [], 0
    while i < len(argv):
        if argv[i] in ("--ats",):
            i += 1
        elif argv[i] in ("--accent", "--preset", "--font"):
            i += 2
        else:
            pos.append(argv[i]); i += 1
    if len(pos) < 3:
        sys.exit("usage: build_branded_pdf.py <resume.md> <out.pdf> \"<title>\" "
                 "[--accent '#RRGGBB' | --preset name] [--font grotesque|condensed|clean] [--ats]")
    return Path(pos[0]), Path(pos[1]), pos[2], accent, pairing, ats


def main():
    md_path, out_path, title, accent_hex, pairing, ats = parse_args(sys.argv[1:])

    fonts = PAIRINGS.get(pairing, PAIRINGS["grotesque"])
    pdfmetrics.registerFont(TTFont("Display", FONT_DIR / fonts["display"]))
    pdfmetrics.registerFont(TTFont("Body", FONT_DIR / fonts["body"]))
    pdfmetrics.registerFont(TTFont("BodyB", FONT_DIR / fonts["bold"]))
    pdfmetrics.registerFont(TTFont("BodyI", FONT_DIR / fonts["italic"]))
    pdfmetrics.registerFont(TTFont("BodyL", FONT_DIR / fonts["light"]))
    pdfmetrics.registerFontFamily("Body", normal="Body", bold="BodyB", italic="BodyI")

    RAW = colors.HexColor(accent_hex)
    ACCENT = readable(RAW)
    ACCENT_HEX = "#%02X%02X%02X" % (int(ACCENT.red * 255), int(ACCENT.green * 255), int(ACCENT.blue * 255))
    CARD = tint(RAW)
    PAGE = colors.white if ats else tint(RAW, 0.975)
    INK = colors.HexColor("#141414")
    MUTED = colors.HexColor("#6B6B6B")
    inline = make_inline(ACCENT_HEX)

    b = getSampleStyleSheet()["Normal"]
    S = {
        "name":    ParagraphStyle("name", parent=b, fontName="Display", fontSize=30, leading=32, textColor=INK),
        "title":   ParagraphStyle("title", parent=b, fontName="BodyB", fontSize=10.6, leading=14.5, textColor=ACCENT, spaceBefore=5),
        "contact": ParagraphStyle("contact", parent=b, fontName="Body", fontSize=8.8, leading=13.4, textColor=INK),
        "section": ParagraphStyle("section", parent=b, fontName="Display", fontSize=11.6, leading=13.4, textColor=INK, spaceBefore=10, spaceAfter=1),
        "body":    ParagraphStyle("body", parent=b, fontName="Body", fontSize=9.1, leading=12.8, textColor=INK, spaceAfter=4.4),
        "role":    ParagraphStyle("role", parent=b, fontName="BodyB", fontSize=9.8, leading=12.4, textColor=INK, spaceBefore=6.6),
        "meta":    ParagraphStyle("meta", parent=b, fontName="BodyL", fontSize=8.3, leading=10.6, textColor=ACCENT if not ats else MUTED, spaceAfter=3.0),
        "bullet":  ParagraphStyle("bullet", parent=b, fontName="Body", fontSize=8.95, leading=12.5,
                                  leftIndent=13, firstLineIndent=-13, spaceAfter=3.1, textColor=INK),
    }
    S["cardb"] = ParagraphStyle("cardb", parent=S["bullet"], spaceAfter=4.0)

    def rule():
        if ats:
            return [Spacer(1, 3)]
        t = Table([[""]], colWidths=[34], rowHeights=[2.4], hAlign="LEFT")
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ACCENT),
                               ("TOPPADDING", (0, 0), (-1, -1), 0),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
        return [t, Spacer(1, 7)]

    def card(flow, border=False, pad=13):
        if ats:  # no tinted containers - parsers choke on them
            return flow
        t = Table([[flow]], colWidths=["100%"])
        st = [("BACKGROUND", (0, 0), (-1, -1), CARD),
              ("LEFTPADDING", (0, 0), (-1, -1), pad), ("RIGHTPADDING", (0, 0), (-1, -1), pad),
              ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]
        if border:
            st.append(("LINEBELOW", (0, 0), (-1, -1), 2.2, ACCENT))
        t.setStyle(TableStyle(st))
        return t

    def furniture(canvas, doc):
        canvas.saveState()
        w, h = A4
        if not ats:
            canvas.setFillColor(PAGE); canvas.rect(0, 0, w, h, stroke=0, fill=1)
            canvas.setFillColor(ACCENT); canvas.rect(0, 0, w, 5.5, stroke=0, fill=1)
        canvas.setFont("Body", 7.6); canvas.setFillColor(MUTED)
        canvas.drawString(doc.leftMargin, 15, title)
        canvas.drawRightString(w - doc.leftMargin, 15, str(doc.page))
        canvas.restoreState()

    lines = md_path.read_text(encoding="utf-8").splitlines()
    story, i, n = [], 0, len(lines)

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
    story += ([card(head, border=True, pad=16), Spacer(1, 4)] if not ats else head + [Spacer(1, 8)])

    section, buf, role, pending = None, None, None, None

    def take():
        nonlocal pending
        p, pending = pending or [], None
        return p

    def flush_role():
        nonlocal role
        if role:
            story.append(KeepTogether(take() + role)); role = None

    def flush_card():
        nonlocal buf
        if buf:
            story.extend(take())
            c = card(buf)  # ATS mode returns the bare list, branded returns a Table
            story.extend(c) if isinstance(c, list) else story.append(c)
            buf = None

    while i < n:
        ln = lines[i]
        if ln.startswith("## "):
            flush_role(); flush_card(); story.extend(take())
            section = ln[3:].strip()
            pending = [Paragraph(esc(section).upper(), S["section"])] + rule()
            if "bring" in section.lower():
                buf = []
        elif ln.startswith("### "):
            flush_role()
            role = [Paragraph(inline(ln[4:].strip()), S["role"])]
        elif ln.startswith("- "):
            mark = "&bull;&nbsp;&nbsp;" if ats else f"<font color='{ACCENT_HEX}'><b>&rarr;</b></font>&nbsp;&nbsp;"
            p = Paragraph(mark + inline(ln[2:].strip()), S["cardb"] if buf is not None else S["bullet"])
            buf.append(p) if buf is not None else role.append(p) if role is not None else (story.extend(take()), story.append(p))
        elif ln.strip():
            txt = ln.strip()
            st = S["meta"] if (section == "Professional Experience" and "|" in txt and re.search(r"\d{4}", txt)) else S["body"]
            p = Paragraph(inline(txt), st)
            buf.append(p) if buf is not None else role.append(p) if role is not None else (story.extend(take()), story.append(p))
        i += 1
    flush_role(); flush_card(); story.extend(take())

    doc = BaseDocTemplate(str(out_path), pagesize=A4, title=title, author="Mohd Hayaat Ali",
                          leftMargin=.62 * inch, rightMargin=.62 * inch,
                          topMargin=.5 * inch, bottomMargin=.55 * inch)
    doc.addPageTemplates([PageTemplate(id="p", frames=[
        Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f",
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=furniture)])
    doc.build(story)
    print(f"OK {out_path}  [accent {ACCENT_HEX} | {pairing} | {'ATS-safe' if ats else 'branded'}]")


if __name__ == "__main__":
    main()
