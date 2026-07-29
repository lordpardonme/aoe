"""Tests for resume parsing and tailoring (master is never modified)."""

from __future__ import annotations

import hashlib

from src.config import MASTER_RESUME
from src.resume import ResumeBuilder


def _digest(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_master_resume_exists():
    assert MASTER_RESUME.exists(), "run scripts/seed_master_resume.py"


def test_load_master_has_sections():
    data = ResumeBuilder().load_master()
    assert data.name
    titles = [s.title.lower() for s in data.sections]
    assert any("summary" in t for t in titles)
    assert any("experience" in t for t in titles)


def test_tailor_adds_key_skills_section(job):
    data = ResumeBuilder().tailor(job)
    titles = [s.title.lower() for s in data.sections]
    assert any("key skills" in t for t in titles)


def test_tailor_injects_role_into_summary(job):
    data = ResumeBuilder().tailor(job)
    summary = next(s for s in data.sections if "summary" in s.title.lower())
    lead = summary.blocks[0].text.lower()
    assert "senior product designer" in lead


def test_tailoring_does_not_modify_master(job):
    before = _digest(MASTER_RESUME)
    builder = ResumeBuilder()
    builder.build(job)  # writes to generated/, not the master
    after = _digest(MASTER_RESUME)
    assert before == after, "master resume must never be overwritten"


def test_build_writes_generated_docx(job):
    _data, path = ResumeBuilder().build(job)
    assert path.exists()
    assert path.suffix == ".docx"
    assert "acme_labs" in path.name
