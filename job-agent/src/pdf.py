"""PDF rendering via ReportLab.

Two entry points:
    * :func:`render_resume_pdf`  — structured :class:`~src.resume.ResumeData` -> PDF.
    * :func:`render_text_pdf`    — a block of text (e.g. a cover letter) -> PDF.

ReportLab is used (rather than a DOCX->PDF converter) so PDFs are produced with
no external binaries, Word, or LibreOffice — it works identically on any OS.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from .logger import get_logger

if TYPE_CHECKING:  # avoid a hard import cycle at runtime
    from .resume import ResumeData

log = get_logger("pdf")


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "NameStyle", parent=base["Title"], fontSize=20, spaceAfter=2,
            textColor="#111111", alignment=TA_LEFT,
        ),
        "headline": ParagraphStyle(
            "Headline", parent=base["Normal"], fontSize=11, textColor="#444444",
            spaceAfter=6,
        ),
        "contact": ParagraphStyle(
            "Contact", parent=base["Normal"], fontSize=9, textColor="#555555",
            spaceAfter=1,
        ),
        "section": ParagraphStyle(
            "SectionHeading", parent=base["Heading2"], fontSize=12,
            textColor="#1a1a1a", spaceBefore=10, spaceAfter=4,
        ),
        "subhead": ParagraphStyle(
            "SubHead", parent=base["Normal"], fontSize=10.5, spaceBefore=4,
            spaceAfter=2, textColor="#222222", leading=13,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["Normal"], fontSize=10, leading=13, spaceAfter=3,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["Normal"], fontSize=10, leading=13,
        ),
    }


def _doc(out_path: Path) -> SimpleDocTemplate:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    return SimpleDocTemplate(
        str(out_path),
        pagesize=LETTER,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
        title=out_path.stem,
    )


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )


def render_resume_pdf(data: "ResumeData", out_path: Path) -> Path:
    """Render a :class:`ResumeData` to a polished one/two-column-free PDF."""
    styles = _styles()
    story: list = []

    if data.name:
        story.append(Paragraph(_escape(data.name), styles["name"]))
    if data.headline:
        story.append(Paragraph(_escape(data.headline), styles["headline"]))
    for line in data.contact_lines:
        story.append(Paragraph(_escape(line), styles["contact"]))
    story.append(Spacer(1, 6))

    for section in data.sections:
        story.append(Paragraph(_escape(section.title).upper(), styles["section"]))
        bullets: list = []

        def flush_bullets() -> None:
            if bullets:
                story.append(
                    ListFlowable(
                        list(bullets), bulletType="bullet", start="•",
                        leftIndent=12,
                    )
                )
                bullets.clear()

        for block in section.blocks:
            if block.kind == "bullet":
                bullets.append(
                    ListItem(
                        Paragraph(_escape(block.text), styles["bullet"]),
                        value="•",
                    )
                )
            else:
                flush_bullets()
                style = styles["subhead"] if block.kind == "subhead" else styles["body"]
                text = block.text
                if block.kind == "subhead":
                    text = f"<b>{_escape(text)}</b>"
                else:
                    text = _escape(text)
                story.append(Paragraph(text, style))
        flush_bullets()

    _doc(out_path).build(story)
    log.info("Wrote resume PDF -> %s", out_path)
    return out_path


def render_text_pdf(text: str, out_path: Path, *, title: str | None = None) -> Path:
    """Render a plain-text document (paragraphs + '- ' bullets) to PDF."""
    styles = _styles()
    story: list = []
    if title:
        story.append(Paragraph(_escape(title), styles["name"]))
        story.append(Spacer(1, 6))

    for raw in text.split("\n"):
        line = raw.rstrip()
        if not line.strip():
            story.append(Spacer(1, 6))
            continue
        if line.lstrip().startswith(("- ", "* ")):
            content = line.lstrip()[2:]
            story.append(
                ListFlowable(
                    [ListItem(Paragraph(_escape(content), styles["body"]), value="•")],
                    bulletType="bullet", start="•", leftIndent=12,
                )
            )
        else:
            story.append(Paragraph(_escape(line), styles["body"]))

    _doc(out_path).build(story)
    log.info("Wrote text PDF -> %s", out_path)
    return out_path
