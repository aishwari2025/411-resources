import pytest


def test_create_account(client, session):
    """
    test user account creation via /create-account.

    sends a POST request to register a new user and verifies that the response
    status is 200, indicating success.

    asserts:
        - response status code is 200.
    """
    response = client.post("/create-account", json={"username": "test", "password": "123"})
    print(response.get_json())  # ← Helps debug if you still get 400
    assert response.status_code == 200


def test_login_logout(client):
    """
    test user login and logout flow.

    registers a new user, logs them in, and then logs them out. confirms that
    each step returns a 200 response.

    asserts:
        - login returns 200.
        - logout returns 200.
    """
    client.post("/create-account", json={"username": "test2", "password": "abc"})
    res = client.post("/login", json={"username": "test2", "password": "abc"})
    assert res.status_code == 200
    res = client.post("/logout")
    assert res.status_code == 200


def test_buy_and_get_holding(client,session, monkeypatch):
    """
    test buying a stock, retrieving the holding, and deleting it.

    - mocks stock price to return $100.
    - registers and logs in a new user.
    - buys 2 shares of TSLA.
    - verifies holding exists and matches expected values.
    - deletes the holding.
    - verifies the holding is removed.

    Asserts:
        - successful stock purchase (200).
        - holding exists with correct quantity and price.
        - deletion of holding (200).
        - subsequent GET returns 404.
    """
    # Stub the stock price fetch to always return 100.0
    monkeypatch.setattr('external_api.fetch_stock_price', lambda s: 100.0)

    # Register and log in a new user
    client.post('/create-account', json={'username': 'u3', 'password': 'pwd'})
    client.post('/login', json={'username': 'u3', 'password': 'pwd'})

    # Manually set session to simulate login
    from models.user_model import Users

    user = session.query(Users).filter_by(username="u3").first()
    self.holdings.setdefault(user, {})



    # Buy 2 shares of TSLA
    rv = client.post('/portfolio/buy', json={'symbol': 'TSLA', 'quantity': 2})
    assert rv.status_code == 200

    # Retrieve the single holding
    rv = client.get('/portfolio/holding/TSLA')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['quantity'] == 2
    assert data['avg_price'] == 100.0

    # Delete the holding
    rv = client.delete('/portfolio/holding/TSLA')
    assert rv.status_code == 200

    # Confirm that the holding is gone
    rv = client.get('/portfolio/holding/TSLA')
    assert rv.status_code == 404


def test_clear_portfolio(client, monkeypatch):
    """
    test clearing a portfolio after adding a stock.

    - mocks stock price to return $50.
    - registers and logs in a new user.
    - buys 1 share of GOOG.
    - clears the portfolio.
    - confirms all holdings are removed.

    asserts:
        - stock buy returns 200.
        - clear route returns expected message.
        - deleted holding is no longer accessible (404).
    """
    # Stub the stock price fetch
    monkeypatch.setattr('external_api.fetch_stock_price', lambda s: 50.0)

    # Register and log in a new user
    client.post('/create-account', json={'username': 'u4', 'password': 'pwd'})
    client.post('/login', json={'username': 'u4', 'password': 'pwd'})

    # Manually simulate login by setting session
    client.post('/login', json={'username': 'u4', 'password': 'pwd'})
  

    # Buy 1 share of GOOG
    rv = client.post('/portfolio/buy', json={'symbol': 'GOOG', 'quantity': 1})
    assert rv.status_code == 200

    # Clear the portfolio
    rv = client.delete('/portfolio/clear')
    assert rv.status_code == 200
    assert rv.get_json() == {'message': 'Portfolio cleared'}

    # Confirm no holdings remain
    rv = client.get('/portfolio/holding/GOOG')
    assert rv.status_code == 404
