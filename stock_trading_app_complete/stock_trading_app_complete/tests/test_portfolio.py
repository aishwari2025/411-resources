def test_buy_and_view(client, auth_headers):
    client.post("/portfolio/buy", headers=auth_headers, json={"symbol": "AAPL", "quantity": 2})
    res = client.get("/portfolio", headers=auth_headers)
    assert res.status_code == 200
    assert "AAPL" in res.json

def test_clear(client, auth_headers):
    client.delete("/portfolio/clear", headers=auth_headers)
    res = client.get("/portfolio", headers=auth_headers)
    assert res.json == {}
