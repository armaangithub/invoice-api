"""Unit tests for invoice API endpoints."""

import json
import pytest
from app import app


@pytest.fixture
def client():
    """Create test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test health endpoint returns 200."""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "ok"


def test_list_invoices_empty(client):
    """Test listing invoices when none exist."""
    response = client.get("/invoices")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["total"] == 0


def test_create_invoice(client):
    """Test creating a new invoice."""
    response = client.post(
        "/invoices",
        data=json.dumps({"amount": 100.50, "description": "Test invoice"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["amount"] == 100.50
    assert data["status"] == "pending"


def test_create_invoice_missing_amount(client):
    """Test creating invoice without amount returns 400."""
    response = client.post(
        "/invoices",
        data=json.dumps({"description": "No amount"}),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_get_invoice_not_found(client):
    """Test getting non-existent invoice returns 404."""
    response = client.get("/invoices/nonexistent")
    assert response.status_code == 404
