"""Shared pytest fixtures.

Ensures the project root is importable and DRY_RUN is forced on so no test can
ever hit Gmail / Sheets for real.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Force safety before any project import reads settings.
os.environ.setdefault("DRY_RUN", "true")
os.environ.setdefault("TRACKER_SPREADSHEET_ID", "")


SAMPLE_JD = (
    "Acme Labs is hiring a Senior Product Designer.\n"
    "You will own user flows, wireframing, prototyping in Figma, design systems, "
    "usability testing, accessibility and developer handoff for our B2B SaaS "
    "dashboard and payments product.\n"
    "Send your application to careers@acme.example."
)


@pytest.fixture(scope="session")
def sample_jd() -> str:
    return SAMPLE_JD


@pytest.fixture(scope="session")
def job(sample_jd):
    from src.jobs import build_job

    return build_job(text=sample_jd, url="https://acme.example/careers/pd",
                     company="Acme Labs", role="Senior Product Designer")


@pytest.fixture(scope="session")
def resume_data(job):
    from src.resume import ResumeBuilder

    return ResumeBuilder().tailor(job)
