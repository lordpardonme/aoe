"""Tests for Munder Difflin Hive multi-agent orchestration and MCP server."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.hive import CircuitBreaker, HiveCoordinator, TaskStatus
from src.mcp_server import TOOLS, handle_tool_call


SAMPLE_JD = """
Spotify is seeking a Senior Product Designer to lead design for Spotify for Artists.
Requirements:
- 5+ years of end-to-end product design experience across web and mobile.
- Deep expertise in Figma, design systems, and rapid prototyping.
- Strong track record of collaborating with cross-functional product and engineering teams.
- Passion for music and empowering creators worldwide.
"""


def test_mcp_tools_manifest():
    assert len(TOOLS) >= 4
    tool_names = [t["name"] for t in TOOLS]
    assert "aoe_run_hive_pipeline" in tool_names
    assert "aoe_list_leads" in tool_names
    assert "aoe_get_stats" in tool_names
    assert "aoe_scan_recruiter_replies" in tool_names


def test_mcp_get_stats():
    res = handle_tool_call("aoe_get_stats", {})
    assert "content" in res
    assert len(res["content"]) > 0
    data = json.loads(res["content"][0]["text"])
    assert "total_applications" in data
    assert "interview_rate" in data
    assert "resumes_generated" in data


def test_circuit_breaker_logic():
    cb = CircuitBreaker(failure_threshold=3)
    assert cb.state == "closed"
    assert not cb.is_blocked()

    cb.record_failure("err 1")
    assert cb.failures == 1
    assert cb.state == "closed"

    cb.record_failure("err 2")
    assert cb.failures == 2
    assert cb.state == "half-open"

    cb.record_failure("err 3")
    assert cb.failures == 3
    assert cb.state == "open"
    assert cb.is_blocked()

    # Success relieves pressure
    cb.record_success()
    assert cb.failures == 2


def test_hive_pipeline_execution():
    coordinator = HiveCoordinator()
    result = coordinator.run_pipeline(
        text=SAMPLE_JD,
        company="Spotify",
        role="Senior Product Designer"
    )

    assert result["status"] == "completed"
    tasks = result["tasks"]
    assert len(tasks) == 4

    roles = [t["role"] for t in tasks]
    assert "scout" in roles
    assert "resume_architect" in roles
    assert "copywriter" in roles
    assert "quality_reviewer" in roles

    for t in tasks:
        assert t["status"] == TaskStatus.COMPLETED.value

    artifacts = result["artifacts"]
    assert artifacts["company"] == "Spotify"
    assert artifacts["role"] == "Senior Product Designer"
    assert Path(artifacts["resume_pdf"]).exists()
    assert artifacts["wcag_aa_compliant"] is True
    assert artifacts["attention_score"] >= 0
    assert "Senior Product Designer" in artifacts["email_subject"]
    assert len(artifacts["followup_pitch"]) > 20
