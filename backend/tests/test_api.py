"""
Integration and End-to-End API Route Tests using FastAPI TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_check_endpoint(client):
    """Verify /health and /api/health status, service metadata, and model identifier."""
    for path in ["/health", "/api/health"]:
        response = client.get(path)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "llama" in data["model"]


def test_root_spa_serving(client):
    """Verify that GET / correctly serves the compiled frontend SPA."""
    response = client.get("/")
    assert response.status_code == 200
    assert "<!doctype html>" in response.text.lower() or "<html" in response.text.lower()


def test_synthesize_blueprint_happy_path(client):
    """Verify POST /api/blueprint synthesis and financial integrity."""
    payload = {
        "event_type": "Milestone Birthday",
        "location": "Downtown Brooklyn Industrial Loft",
        "guest_count": 80,
        "currency": "USD",
        "total_budget": 24000.0,
        "weeks_to_event": 16,
        "sensory_theme": "Industrial Loft, Neo-Tokyo, Modular Synth",
        "operational_constraints": "Curfew at 1 AM."
    }
    response = client.post("/api/blueprint", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Schema integrity checks
    assert "event_summary" in data
    assert "sensory_concept" in data
    assert "financial_ledger" in data
    assert "timeline" in data
    assert "vendor_matrix" in data

    # Financial mathematical verification
    ledger = data["financial_ledger"]
    assert ledger["total_budget"] == 24000.0
    assert ledger["contingency_reserve"] == 2400.0
    assert ledger["allocated_budget"] == 21600.0
    assert ledger["cost_per_guest"] == 300.0
    assert len(ledger["items"]) > 0


def test_synthesize_blueprint_caching(client):
    """Verify that repeated identical blueprint requests are served from TTL cache."""
    payload = {
        "event_type": "Civic Gala",
        "location": "Waterfront Greenhouse",
        "guest_count": 200,
        "currency": "USD",
        "total_budget": 60000.0,
        "weeks_to_event": 20,
        "sensory_theme": "Zero-waste botanical biophilia",
        "operational_constraints": None
    }
    # First request
    resp1 = client.post("/api/blueprint", json=payload)
    assert resp1.status_code == 200

    # Second request (cached)
    resp2 = client.post("/api/blueprint", json=payload)
    assert resp2.status_code == 200
    assert resp1.json() == resp2.json()


def test_synthesize_blueprint_validation_error(client):
    """Verify that invalid payloads (e.g. negative budget or missing required fields) return 422."""
    bad_payload = {
        "event_type": "Party",
        "total_budget": -100.0  # Invalid
    }
    response = client.post("/api/blueprint", json=bad_payload)
    assert response.status_code == 422


def test_legacy_alias_endpoint(client):
    """Verify /api/plan/all alias behaves identically to /api/blueprint."""
    payload = {
        "event_type": "Intimate Dinner",
        "location": "Private Dining Room",
        "guest_count": 25,
        "currency": "EUR",
        "total_budget": 5000.0,
        "weeks_to_event": 6,
        "sensory_theme": "Candlelight & Natural Wine",
        "operational_constraints": "Vegan only"
    }
    response = client.post("/api/plan/all", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["financial_ledger"]["cost_per_guest"] == 200.0
