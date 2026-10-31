"""
Security, Middleware & Rate Limiting Tests.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app, _request_timestamps


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_owasp_security_headers(client):
    """Verify that OWASP defense-in-depth response headers are returned on all endpoints."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers.get("x-content-type-options") == "nosniff"
    assert response.headers.get("x-frame-options") == "DENY"
    assert response.headers.get("referrer-policy") == "strict-origin-when-cross-origin"


def test_cors_preflight(client):
    """Verify CORS preflight handling for allowed origin."""
    headers = {
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type",
    }
    response = client.options("/api/blueprint", headers=headers)
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


def test_rate_limiter_protection(client):
    """Verify that hammering the synthesis endpoint trips the sliding-window rate limit (429)."""
    payload = {
        "event_type": "Test Gathering",
        "location": "Local Park",
        "guest_count": 50,
        "currency": "USD",
        "total_budget": 10000.0,
        "weeks_to_event": 10,
        "sensory_theme": "Picnic",
        "operational_constraints": None
    }

    # Clear history for clean test run
    _request_timestamps.clear()

    # Issue 30 allowable requests
    for _ in range(30):
        resp = client.post("/api/blueprint", json=payload)
        assert resp.status_code == 200

    # 31st request should be rejected with 429 Too Many Requests
    resp = client.post("/api/blueprint", json=payload)
    assert resp.status_code == 429
    assert "Rate limit exceeded" in resp.json()["detail"]

    # Clean up state after test
    _request_timestamps.clear()
