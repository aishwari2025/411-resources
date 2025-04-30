def test_create_account(client):
    response = client.post("/create-account", json={"username": "test", "password": "123"})
    assert response.status_code == 200

def test_login_logout(client):
    client.post("/create-account", json={"username": "test2", "password": "abc"})
    res = client.post("/login", json={"username": "test2", "password": "abc"})
    assert res.status_code == 200
    res = client.post("/logout")
    assert res.status_code == 200


def test_buy_and_get_holding(client, monkeypatch):
    # Stub the stock price fetch to always return 100.0
    monkeypatch.setattr('external_api.fetch_stock_price', lambda s: 100.0)

    # Register and log in a new user
    client.post('/create-account', json={'username': 'u3', 'password': 'pwd'})
    client.post('/login', json={'username': 'u3', 'password': 'pwd'})

    # Manually set session to simulate login
    with client.session_transaction() as sess:
        sess['user_id'] = 3  

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
    # Stub the stock price fetch
    monkeypatch.setattr('external_api.fetch_stock_price', lambda s: 50.0)

    # Register and log in a new user
    client.post('/create-account', json={'username': 'u4', 'password': 'pwd'})
    client.post('/login', json={'username': 'u4', 'password': 'pwd'})

    # Manually simulate login by setting session
    with client.session_transaction() as sess:
        sess['user_id'] = 4  

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
