"""Application email generation (Jinja2 -> Markdown + HTML)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .config import EMAILS_DIR, TEMPLATES_DIR
from .coverletter import build_context
from .jobs import JobDescription
from .logger import get_logger
from .resume import ResumeData
from .utils import slugify

log = get_logger("emailer")


def subject_for(job: JobDescription) -> str:
    """Return the email subject line: ``Application for <Role>``."""
    return f"Application for {job.role}"


def _markdown_to_html(text: str) -> str:
    """Minimal, dependency-free Markdown -> HTML for email bodies.

    Supports paragraphs and ``- `` bullet lists — enough for our templates.
    """
    html_lines: list[str] = []
    in_list = False
    for raw in text.split("\n"):
        line = raw.rstrip()
        if line.strip().startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"  <li>{_inline(line.strip()[2:])}</li>")
        elif not line.strip():
            if in_list:
                html_lines.append("</ul>")
                in_list = False
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<p>{_inline(line)}</p>")
    if in_list:
        html_lines.append("</ul>")
    body = "\n".join(html_lines)
    return (
        '<!DOCTYPE html>\n<html><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1"></head>'
        '<body style="font-family:Arial,Helvetica,sans-serif;font-size:14px;'
        'line-height:1.5;color:#222;">\n'
        f"{body}\n</body></html>\n"
    )


def _inline(text: str) -> str:
    esc = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Linkify bare URLs.
    return re.sub(
        r"(https?://[^\s<]+)",
        r'<a href="\1">\1</a>',
        esc,
    )


class EmailBuilder:
    """Render and persist the application email in Markdown + HTML."""

    def __init__(self, templates_dir: Path | None = None) -> None:
        self.templates_dir = templates_dir or TEMPLATES_DIR
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(enabled_extensions=(), default=False),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

    def render_markdown(self, job: JobDescription, resume: ResumeData) -> str:
        template = self.env.get_template("email.md")
        text = template.render(**build_context(job, resume))
        return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    def build(self, job: JobDescription, resume: ResumeData) -> Dict[str, object]:
        """Produce .md + .html email bodies. Returns paths, subject and bodies."""
        slug = slugify(job.company)
        markdown = self.render_markdown(job, resume)
        html = _markdown_to_html(markdown)

        md_path = EMAILS_DIR / f"{slug}_email.md"
        html_path = EMAILS_DIR / f"{slug}_email.html"
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(markdown, encoding="utf-8")
        html_path.write_text(html, encoding="utf-8")
        log.info("Wrote email bodies -> %s , %s", md_path, html_path)

        return {
            "md": md_path,
            "html": html_path,
            "subject": subject_for(job),
            "text_body": markdown,
            "html_body": html,
        }
