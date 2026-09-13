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
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether, PageTemplate,
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

import platform

def _detect_font_dir() -> Path:
    """Return the system font directory for the current OS."""
    system = platform.system()
    if system == "Windows":
        return Path("C:/Windows/Fonts")
    elif system == "Darwin":  # macOS
        return Path("/Library/Fonts")
    else:  # Linux and others
        return Path("/usr/share/fonts/truetype")

FONT_DIR = _detect_font_dir()
URL_RE = re.compile(r"(https?://[^\s)]+)")

# Local CV convention by market, researched 2026. photo: "never" is a hard block
# (bias exposure for the employer - a photo can get the CV binned unread),
# "expected" means omitting one reads as incomplete. branded=False means design
# creativity actively counts against you.
COUNTRY = {
    "us": {"photo": "never", "branded": True,  "note": "Resume, 1-2pp. No photo, DOB, marital status or nationality."},
    "ca": {"photo": "never", "branded": True,  "note": "As US."},
    "uk": {"photo": "no",    "branded": True,  "note": "CV, 2pp. Contact details only, no personal data."},
    "ie": {"photo": "no",    "branded": True,  "note": "As UK."},
    "nl": {"photo": "no",    "branded": True,  "note": "CV, 2pp, no photo."},
    "au": {"photo": "no",    "branded": True,  "note": "As UK."},
    "de": {"photo": "expected", "branded": True,
           "note": "Lebenslauf. Headshot top-right ~35x45mm. Tabular reverse-chron. AGG makes it optional in law; expectation persists."},
    "fr": {"photo": "expected", "branded": True,  "note": "Photo customary."},
    "ae": {"photo": "expected", "branded": True,
           "note": "Include nationality and visa status. Detailed role descriptions expected."},
    "sa": {"photo": "expected", "branded": True,  "note": "As UAE."},
    "om": {"photo": "expected", "branded": True,  "note": "As UAE."},
    "qa": {"photo": "expected", "branded": True,  "note": "As UAE."},
    "jp": {"photo": "expected", "branded": False,
           "note": "Rirekisho (fixed standard form) + shokumu keirekisho (work history). "
                   "Design creativity is NOT appreciated - never send a branded resume. "
                   "Some international firms waive the photo; follow the posting."},
    "in": {"photo": "optional", "branded": True,  "note": "1-2pp. Workspace default."},
}


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
    country = (opt("--country") or "").lower().strip()
    photo = opt("--photo")

    pos, i = [], 0
    while i < len(argv):
        if argv[i] in ("--ats",):
            i += 1
        elif argv[i] in ("--accent", "--preset", "--font", "--country", "--photo"):
            i += 2
        else:
            pos.append(argv[i]); i += 1
    if len(pos) < 3:
        sys.exit("usage: build_branded_pdf.py <resume.md> <out.pdf> \"<title>\" "
                 "[--accent '#RRGGBB' | --preset name] [--font grotesque|condensed|clean] "
                 "[--country us|uk|de|ae|jp|in|...] [--photo headshot.jpg] [--ats]")

    # Local-convention enforcement. These refuse rather than silently "fix",
    # because both failure modes are invisible once the mail has gone.
    if country:
        rules = COUNTRY.get(country)
        if not rules:
            print(f"note: no CV convention on file for '{country}' - defaulting to "
                  f"no photo, neutral 2-page format. Verify before sending.")
        else:
            print(f"country {country}: {rules['note']}")
            if not rules["branded"] and not ats:
                sys.exit(f"REFUSED: {country} does not accept design-led CVs. "
                         f"Re-run with --ats (and see the note above).")
            if photo and rules["photo"] == "never":
                sys.exit(f"REFUSED: a photo on a {country} application is a bias risk "
                         f"for the employer and can get the CV binned unread. Drop --photo.")
            if not photo and rules["photo"] == "expected":
                print(f"WARNING: {country} expects a headshot and none was supplied. "
                      f"This CV will read as incomplete.")

    if photo and not Path(photo).exists():
        sys.exit(f"photo not found: {photo}")

    return Path(pos[0]), Path(pos[1]), pos[2], accent, pairing, ats, country, (Path(photo) if photo else None)


def main():
    md_path, out_path, title, accent_hex, pairing, ats, country, photo = parse_args(sys.argv[1:])

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

    # Type scale. Deliberately roomy - a resume that reads easily beats one that
    # fits on fewer pages. Two to three pages is fine; cramping is not.
    b = getSampleStyleSheet()["Normal"]
    S = {
        "name":    ParagraphStyle("name", parent=b, fontName="Display", fontSize=31, leading=34, textColor=INK),
        "title":   ParagraphStyle("title", parent=b, fontName="BodyB", fontSize=11, leading=16, textColor=ACCENT, spaceBefore=7),
        "contact": ParagraphStyle("contact", parent=b, fontName="Body", fontSize=9.2, leading=14.6, textColor=INK),
        "section": ParagraphStyle("section", parent=b, fontName="Display", fontSize=12, leading=15, textColor=INK, spaceBefore=17, spaceAfter=2, keepWithNext=1),
        "body":    ParagraphStyle("body", parent=b, fontName="Body", fontSize=9.8, leading=15.0, textColor=INK, spaceAfter=7.5),
        "role":    ParagraphStyle("role", parent=b, fontName="BodyB", fontSize=10.4, leading=13.6, textColor=INK, spaceBefore=11),
        "meta":    ParagraphStyle("meta", parent=b, fontName="BodyL", fontSize=8.9, leading=12.0, textColor=ACCENT if not ats else MUTED, spaceAfter=5.0),
        "bullet":  ParagraphStyle("bullet", parent=b, fontName="Body", fontSize=9.5, leading=14.6,
                                  leftIndent=15, firstLineIndent=-15, spaceAfter=5.5, textColor=INK),
    }
    S["cardb"] = ParagraphStyle("cardb", parent=S["bullet"], spaceAfter=6.5)

    def rule():
        # keepWithNext on every piece so a heading can never strand itself at the
        # foot of a page while its content starts on the next one.
        if ats:
            s = Spacer(1, 4); s.keepWithNext = 1
            return [s]
        t = Table([[""]], colWidths=[34], rowHeights=[2.4], hAlign="LEFT")
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ACCENT),
                               ("TOPPADDING", (0, 0), (-1, -1), 0),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
        t.keepWithNext = 1
        # No keepWithNext on the trailing spacer: reportlab treats a keepWithNext
        # chain as one atomic block, which would stop the card below from
        # splitting and bounce the whole thing to the next page.
        return [t, Spacer(1, 9)]

    def card(flow, border=False, pad=17, split=True):
        if ats:  # no tinted containers - parsers choke on them
            return flow
        if not split:
            # Short blocks (the header) stay one cell so inner spaceBefore is
            # honoured and the lines don't collapse onto each other.
            t = Table([[flow]], colWidths=["100%"])
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CARD),
                                   ("LEFTPADDING", (0, 0), (-1, -1), pad),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), pad),
                                   ("TOPPADDING", (0, 0), (-1, -1), pad),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]
                                  + ([("LINEBELOW", (0, 0), (-1, -1), 2.2, ACCENT)] if border else [])))
            return t
        # One row per flowable, not one cell holding everything: a multi-row
        # table can break across a page and carry its background with it. A
        # single-cell card cannot split, so it leaps to the next page whole and
        # leaves a hole behind it.
        rows = [[f] for f in flow]
        t = Table(rows, colWidths=["100%"], splitByRow=1)
        st = [("BACKGROUND", (0, 0), (-1, -1), CARD),
              ("LEFTPADDING", (0, 0), (-1, -1), pad), ("RIGHTPADDING", (0, 0), (-1, -1), pad),
              ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
              ("TOPPADDING", (0, 0), (0, 0), pad), ("BOTTOMPADDING", (0, -1), (-1, -1), pad)]
        if border:
            st.append(("LINEBELOW", (0, -1), (-1, -1), 2.2, ACCENT))
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
    if photo:
        # Photo sits top-right, ~35x45mm as German/Gulf convention expects.
        pw, ph = 35 * mm * 0.78, 45 * mm * 0.78
        grid = Table([[head, Image(str(photo), width=pw, height=ph)]],
                     colWidths=["*", pw + 6], hAlign="LEFT")
        grid.setStyle(TableStyle([("VALIGN", (0, 0), (0, 0), "TOP"),
                                  ("VALIGN", (1, 0), (1, 0), "TOP"),
                                  ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                  ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                  ("TOPPADDING", (0, 0), (-1, -1), 0),
                                  ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
        head = [grid]
    story += ([card(head, border=True, pad=18, split=False), Spacer(1, 6)] if not ats else head + [Spacer(1, 10)])

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

    import os
    doc = BaseDocTemplate(str(out_path), pagesize=A4, title=title, author=os.environ.get("CANDIDATE_NAME", ""),
                          leftMargin=.78 * inch, rightMargin=.78 * inch,
                          topMargin=.65 * inch, bottomMargin=.65 * inch)
    doc.addPageTemplates([PageTemplate(id="p", frames=[
        Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f",
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=furniture)])
    doc.build(story)
    bits = [f"accent {ACCENT_HEX}", pairing, "ATS-safe" if ats else "branded"]
    if country:
        bits.append(f"country {country}")
    if photo:
        bits.append("photo")
    print(f"OK {out_path}  [{' | '.join(bits)}]")


if __name__ == "__main__":
    main()
