def test_lookup(client, auth_headers,monkeypatch):
    monkeypatch.setattr('external_api.lookup', lambda symbol: {"01. symbol": "MSFT"})
    res = client.get("/stock/lookup?symbol=MSFT", headers=auth_headers)
    assert "01. symbol" in res.json
