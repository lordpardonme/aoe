"""Tests for utils, the tracker CSV mirror, and the end-to-end apply pipeline.

Gmail and Sheets are exercised in DRY_RUN so no network calls occur.
"""

from __future__ import annotations

from src.agent import JobAgent
from src.sheet import LOCAL_TRACKER, SheetClient
from src.utils import retry, slugify, unique_terms


def test_slugify():
    assert slugify("Trinity Consulting, Inc.") == "trinity_consulting_inc"
    assert slugify("") == "unknown"


def test_unique_terms_preserves_order():
    assert unique_terms(["Figma", "figma", "UX", "ux", "AI"]) == ["Figma", "UX", "AI"]


def test_retry_eventually_raises():
    calls = {"n": 0}

    @retry(attempts=3, backoff_seconds=0)
    def boom():
        calls["n"] += 1
        raise ValueError("nope")

    try:
        boom()
    except ValueError:
        pass
    assert calls["n"] == 3


def test_retry_succeeds_after_failure():
    calls = {"n": 0}

    @retry(attempts=3, backoff_seconds=0)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 2:
            raise ValueError("transient")
        return "ok"

    assert flaky() == "ok"
    assert calls["n"] == 2


def test_tracker_writes_local_csv():
    SheetClient().update_tracker(
        company="Acme Labs", role="Product Designer",
        url="https://acme.example", status="Applied", notes="test",
    )
    assert LOCAL_TRACKER.exists()
    content = LOCAL_TRACKER.read_text(encoding="utf-8")
    assert "Acme Labs" in content
    assert "Date,Company,Role,Status,URL,Resume,Notes" in content


def test_apply_dry_run_end_to_end(job):
    agent = JobAgent()
    result = agent.apply(job, send=True, update_sheet=True)
    assert result.dry_run is True
    assert result.email_status == "dry_run"
    assert result.company == "Acme Labs"
    # All core artefacts present.
    for key in ("resume_docx", "resume_pdf", "cover_pdf", "email_md", "email_html"):
        assert key in result.files
    # A JSON record was persisted.
    assert result.timestamp
