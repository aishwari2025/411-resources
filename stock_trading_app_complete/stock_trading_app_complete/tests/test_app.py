import json
import pytest

def test_healthcheck(client):
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_buy_stock_unauthorized(client):
    response = client.post("/portfolio/buy", json={"symbol": "AAPL", "quantity": 5})
    assert response.status_code == 401
    assert response.is_json
    assert "Unauthorized" in response.get_json().get("error", "")

def test_get_holding_unauthorized(client):
    response = client.get("/portfolio/holding/AAPL")
    assert response.status_code == 400
    assert response.is_json
    assert "Unauthorized" in response.get_json().get("error", "")

def test_clear_portfolio_unauthorized(client):
    response = client.delete("/portfolio/clear")
    assert response.status_code == 401
    assert response.is_json
    assert "Unauthorized" in response.get_json().get("error", "")

