def test_buy_and_view(client, auth_headers):
    """
    test buying a stock and viewing the updated portfolio.

    this test ensures that the /portfolio/buy endpoint correctly adds a stock
    to the user's in-memory portfolio, and that the /portfolio route returns
    the updated holdings.

    args:
        client: Flask test client fixture.
        auth_headers: fixture providing authentication headers for a logged-in user.

    asserts:
        - that the response from GET /portfolio returns status code 200.
        - that the portfolio contains the symbol "AAPL" after buying it.
    """
    client.post("/portfolio/buy", headers=auth_headers, json={"symbol": "AAPL", "quantity": 2})
    res = client.get("/portfolio", headers=auth_headers)
    assert res.status_code == 200
    assert "AAPL" in res.json

def test_clear(client, auth_headers):
    """
    test clearing the portfolio using the /portfolio/clear endpoint.

    this test checks that all holdings are removed from the user's portfolio
    after calling the clear route.

    args:
        client: Flask test client fixture.
        auth_headers: fixture providing authentication headers for a logged-in user.

    asserts:
        - that the portfolio is empty (i.e., {}) after clearing it.
    """
    client.delete("/portfolio/clear", headers=auth_headers)
    res = client.get("/portfolio", headers=auth_headers)
    assert res.json == {}
