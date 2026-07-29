"""Tests for cover letter, email and PDF generation."""

from __future__ import annotations

from src.coverletter import CoverLetterBuilder, build_highlights
from src.emailer import EmailBuilder, subject_for
from src.pdf import render_resume_pdf, render_text_pdf


def test_cover_letter_mentions_company_and_role(job, resume_data):
    text = CoverLetterBuilder().render(job, resume_data)
    assert job.company in text
    assert job.role in text
    assert "Sincerely" in text


def test_cover_letter_builds_all_formats(job, resume_data):
    out = CoverLetterBuilder().build(job, resume_data)
    for key in ("md", "docx", "pdf"):
        assert out[key].exists(), f"{key} missing"


def test_highlights_prefer_quantified_bullets(job, resume_data):
    highlights = build_highlights(job, resume_data)
    assert highlights
    assert any(any(ch.isdigit() for ch in h) for h in highlights)


def test_email_subject_format(job):
    assert subject_for(job) == f"Application for {job.role}"


def test_email_builds_md_and_html(job, resume_data):
    out = EmailBuilder().build(job, resume_data)
    assert out["md"].exists()
    assert out["html"].exists()
    html = out["html"].read_text(encoding="utf-8")
    assert "<html" in html.lower()
    assert job.role in str(out["text_body"])


def test_render_resume_pdf(tmp_path, resume_data):
    out = render_resume_pdf(resume_data, tmp_path / "r.pdf")
    assert out.exists() and out.stat().st_size > 500


def test_render_text_pdf(tmp_path):
    out = render_text_pdf("Hello\n\n- one\n- two\n", tmp_path / "t.pdf")
    assert out.exists() and out.stat().st_size > 400
