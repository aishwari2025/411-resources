def test_lookup(client, auth_headers,monkeypatch):
    """
    test the /stock/lookup endpoint with a mocked external API response.

    this test verifies that the route correctly returns a JSON response
    containing the expected stock symbol when the external API call is mocked.

    args:
        client: Flask test client fixture.
        auth_headers: Fixture providing authentication headers for a logged-in user.
        monkeypatch: Pytest fixture used to override the 'external_api.lookup' function.

    asserts:
        - That the key "01. symbol" exists in the JSON response from the route.
    """
    monkeypatch.setattr("external_api.lookup", lambda symbol: {"01. symbol": "MSFT"})
    res = client.get("/stock/lookup?symbol=MSFT", headers=auth_headers)
    print(res.get_json())
    assert "01. symbol" in res.json
