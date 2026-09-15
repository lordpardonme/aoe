"""Tests for Hive Server-Sent Events stream and Supervisor chat endpoints."""

from __future__ import annotations

import pytest
from starlette.testclient import TestClient

from src.hive import broadcast_hive_event, subscribe_hive_events
from src.web.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_supervisor_chat_status(client):
    res = client.post("/api/hive/chat", json={"message": "status report"})
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data
    assert "action" in data
    assert data["action"] == "status"
    assert "Scout" in data["reply"]


def test_supervisor_chat_fallback(client):
    res = client.post("/api/hive/chat", json={"message": "hello world"})
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data
    assert data["action"] == "default"


def test_hive_event_broadcasting():
    received = []
    def callback(event):
        received.append(event)

    subscribe_hive_events(callback)
    try:
        broadcast_hive_event("test_event", {"foo": "bar"})
        assert len(received) == 1
        assert received[0]["type"] == "test_event"
        assert received[0]["data"]["foo"] == "bar"
    finally:
        from src.hive import unsubscribe_hive_events
        unsubscribe_hive_events(callback)


def test_staging_office_html_served(client):
    res = client.get("/staging_office.html")
    assert res.status_code == 200
    assert "office-canvas" in res.text
    assert "AOE Operations Floor" in res.text
    assert "STAGING PREVIEW" in res.text
