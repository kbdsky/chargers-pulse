"""Unit tests for Mobile PWA API server."""

import pytest
from fastapi.testclient import TestClient
from newspulse.mobile.server import app

client = TestClient(app)


def test_mobile_root_serves_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "CHARGERS" in response.text
    assert "manifest.json" in response.text


def test_mobile_manifest():
    response = client.get("/manifest.json")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ChargersPulse - LA 차저스 브리핑"
    assert data["display"] == "standalone"


def test_mobile_service_worker():
    response = client.get("/service-worker.js")
    assert response.status_code == 200
    assert "chargers-pulse" in response.text


def test_mobile_briefing_api():
    response = client.get("/api/briefing")
    assert response.status_code == 200
    data = response.json()
    assert "briefing" in data
    assert "articles" in data
