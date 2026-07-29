"""Tests for job-description parsing and keyword extraction."""

from __future__ import annotations

from src.jobs import build_job, extract_keywords, guess_company, guess_role


def test_extract_keywords_finds_design_terms(sample_jd):
    kws = extract_keywords(sample_jd)
    joined = " ".join(kws).lower()
    assert "figma" in joined
    assert "design system" in joined or "design systems" in joined
    assert "usability testing" in joined


def test_build_job_uses_overrides(sample_jd):
    job = build_job(text=sample_jd, company="Acme Labs", role="Senior Product Designer")
    assert job.company == "Acme Labs"
    assert job.role == "Senior Product Designer"


def test_build_job_extracts_contact_email(sample_jd):
    job = build_job(text=sample_jd)
    assert job.contact_email == "careers@acme.example"


def test_guess_role_from_labeled_text():
    text = "Position: Motion Designer\nSome description here."
    assert guess_role(text) == "Motion Designer"


def test_guess_company_from_url_when_no_hint():
    company = guess_company("A job", url="https://acmecorp.com/jobs/1", hint=None)
    assert company.lower().startswith("acmecorp")


def test_keywords_are_deduped(sample_jd):
    kws = extract_keywords(sample_jd)
    assert len(kws) == len({k.lower() for k in kws})
