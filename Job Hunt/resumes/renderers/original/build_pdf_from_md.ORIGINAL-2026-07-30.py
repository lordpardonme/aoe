#!/usr/bin/env python3
"""
Dynamic, Brand-Aware & Creative-Adaptive PDF Resume Generator for Mohd Hayaat Ali.

Renders any *-resume.md file into a high-craft A4 PDF with custom brand colors,
spacious typography, ATS optimization, and creative/corporate layout modes.
"""
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Table, TableStyle

# Brand Color Presets
BRAND_PRESETS = {
    "fintech": "#0284C7",      # Sky Blue
    "healthcare": "#059669",   # Emerald Green
    "logistics": "#D97706",    # Amber Gold
    "creative": "#8B5CF6",     # Vivid Purple
    "marketplace": "#EC4899",  # Rose Pink
    "honeststudio": "#10B981", # Emerald
    "spotify": "#1DB954",      # Spotify Green
    "deloitte": "#86BC25",     # Deloitte Green
    "google": "#4285F4",       # Google Blue
    "redbull": "#DC0000",      # Red Bull Red
    "default": "#155E75"       # Deep Cyan / Slate
}

def parse_args(argv):
    spacious = "--spacious" in argv
    creative = "--creative" in argv
    corporate = "--corporate" in argv
    
    accent_hex = "#155E75" # Default
    if "--color" in argv:
        idx = argv.index("--color")
        if idx + 1 < len(argv):
            accent_hex = argv[idx + 1]
    elif "--brand" in argv:
        idx = argv.index("--brand")
        if idx + 1 < len(argv):
            brand_name = argv[idx + 1].lower()
            accent_hex = BRAND_PRESETS.get(brand_name, BRAND_PRESETS["default"])

    pos_args = []
    i = 0
    while i < len(argv):
        if argv[i] in ("--spacious", "--creative", "--corporate"):
            i += 1
        elif argv[i] in ("--color", "--brand"):
            i += 2
        else:
            pos_args.append(argv[i])
            i += 1

    md_path = Path(pos_args[0]).resolve() if len(pos_args) > 0 else Path("resume.md").resolve()
    out_path = Path(pos_args[1]).resolve() if len(pos_args) > 1 else Path("output.pdf").resolve()
    title = pos_args[2] if len(pos_args) > 2 else "Resume"

    return md_path, out_path, title, spacious, creative, corporate, accent_hex


MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
RAW_URL_RE = re.compile(r"(?<!href=\")(?<!color=\")(https?://[^\s)]+)")

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def inline(t, accent_hex):
    # 1. Parse markdown links [Text](URL) -> <link href="URL">Text</link>
    def md_link_repl(m):
        anchor_text = esc(m.group(1))
        url = m.group(2)
        return f'<link href="{url}" color="{accent_hex}"><u><b>{anchor_text}</b></u></link>'
    
    s = MD_LINK_RE.sub(md_link_repl, t)

    # 2. Bold **text**
    out = []
    for i, seg in enumerate(re.split(r"\*\*(.+?)\*\*", s)):
        if i % 2 == 1:
            out.append(f"<b>{seg}</b>")
        else:
            out.append(seg)
    s = "".join(out)

    # 3. Raw URLs if any remaining
    def raw_url_repl(m):
        u = m.group(1)
        disp = u.replace("https://", "").replace("http://", "").rstrip("/")
        return f'<link href="{u}" color="{accent_hex}"><u>{esc(disp)}</u></link>'
    
    return RAW_URL_RE.sub(raw_url_repl, s)


def main():
    md_path, out_path, title, spacious, creative, corporate, accent_hex = parse_args(sys.argv[1:])
    
    if not md_path.exists():
        print(f"Error: File '{md_path}' not found.")
        sys.exit(1)

    lines = md_path.read_text(encoding="utf-8").splitlines()

    # Define Colors
    INK = colors.HexColor("#111827")
    MUTED = colors.HexColor("#4B5563")
    ACCENT = colors.HexColor(accent_hex)
    BG_LIGHT = colors.HexColor("#F9FAFB")

    # Typography & Styles
    base = getSampleStyleSheet()
    
    font_scale = 1.12 if spacious else 1.0
    lead_scale = 1.15 if spacious else 1.0
    space_scale = 1.8 if spacious else 1.0

    S = {
        "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=24 * font_scale, leading=27 * lead_scale, textColor=INK if not creative else ACCENT),
        "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11 * font_scale, leading=14 * lead_scale, textColor=ACCENT, spaceAfter=4 * space_scale),
        "contact": ParagraphStyle("contact", parent=base["Normal"], fontSize=8.8 * font_scale, leading=11.5 * lead_scale, textColor=MUTED),
        "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11.2 * font_scale, leading=13.5 * lead_scale, textColor=ACCENT, spaceBefore=7 * space_scale, spaceAfter=2.5 * space_scale),
        "body": ParagraphStyle("body", parent=base["Normal"], fontSize=8.5 * font_scale, leading=11.2 * lead_scale, textColor=INK, spaceAfter=2.5 * space_scale),
        "role": ParagraphStyle("role", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9.3 * font_scale, leading=11.5 * lead_scale, textColor=INK, spaceBefore=4 * space_scale),
        "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=8.2 * font_scale, leading=10.0 * lead_scale, textColor=MUTED, spaceAfter=2.0 * space_scale),
        "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontSize=8.1 * font_scale, leading=10.8 * lead_scale, leftIndent=12, firstLineIndent=-8, spaceAfter=1.5 * space_scale, textColor=INK)
    }

    story = []
    i = 0
    n = len(lines)

    # Parse Header
    while i < n and not lines[i].startswith("# "):
        i += 1
    name_text = lines[i][2:].strip() if i < n else "Resume"
    i += 1

    while i < n and not lines[i].startswith("## "):
        i += 1
    title_text = lines[i][3:].strip() if i < n else ""
    i += 1

    contact_lines = []
    while i < n and not lines[i].startswith("## "):
        if lines[i].strip():
            contact_lines.append(inline(lines[i].strip().rstrip("  "), accent_hex))
        i += 1

    # Render Header (Creative Card vs Classic Header)
    if creative:
        header_p1 = Paragraph(esc(name_text), S["name"])
        header_p2 = Paragraph(inline(title_text, accent_hex).upper(), S["title"])
        header_p3 = Paragraph("<br/>".join(contact_lines), S["contact"])
        
        card_table = Table([[header_p1], [header_p2], [header_p3]], colWidths=["100%"])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
            ('BOX', (0,0), (-1,-1), 1.5, ACCENT),
            ('PADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,-1), (-1,-1), 10),
        ]))
        story.append(card_table)
    else:
        story.append(Paragraph(esc(name_text), S["name"]))
        story.append(Paragraph(inline(title_text, accent_hex).upper(), S["title"]))
        for cl in contact_lines:
            story.append(Paragraph(cl, S["contact"]))

    def sec(t):
        story.append(Paragraph(esc(t).upper(), S["section"]))
        story.append(HRFlowable(width="100%", thickness=1.2 if creative else 0.65, color=ACCENT if creative else colors.HexColor("#CBD5E1"), spaceAfter=3))

    section = None
    while i < n:
        ln = lines[i]
        if ln.startswith("## "):
            section = ln[3:].strip()
            sec(section)
        elif ln.startswith("### "):
            story.append(Paragraph(inline(ln[4:].strip(), accent_hex), S["role"]))
        elif ln.startswith("- "):
            story.append(Paragraph("&bull;&nbsp;&nbsp;" + inline(ln[2:].strip(), accent_hex), S["bullet"]))
        elif ln.strip():
            txt = ln.strip()
            if section == "Professional Experience" and "|" in txt and re.search(r"\d{4}", txt):
                story.append(Paragraph(inline(txt, accent_hex), S["meta"]))
            else:
                story.append(Paragraph(inline(txt, accent_hex), S["body"]))
        i += 1

    side, tb = (.75, .60) if spacious else (.50, .40)
    doc = SimpleDocTemplate(
        str(out_path), pagesize=A4,
        leftMargin=side * inch, rightMargin=side * inch,
        topMargin=tb * inch, bottomMargin=tb * inch,
        title=title,
    )
    doc.build(story)
    print(f"OK [Brand Accent: {accent_hex} | Mode: {'Creative' if creative else 'Corporate'}] -> {out_path}")


if __name__ == "__main__":
    main()
