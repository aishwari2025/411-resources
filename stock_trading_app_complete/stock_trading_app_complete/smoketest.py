#!/usr/bin/env python3
"""
smoketest.py

Basic smoke test: start the Flask app, exercise auth and portfolio routes,
and verify we get expected HTTP 200 (or 404) responses.
"""

import os
# Dummy credentials and API/secret keys
os.environ["ALPHA_VANTAGE_API_KEY"] = "demo"
os.environ["SECRET_KEY"] = "test_secret"

import sys
from unittest import mock

# We'll need to patch the external API calls
@mock.patch('external_api.fetch_stock_price', return_value=100.0)
def run_smoke_tests(mock_fetch_stock_price):
    from app import create_app
    from app import db
    # Ensure model tables are registered
    import models.user_model
    from models.user_model import Users
    from models.portfolio_model import portfolio_model

    app = create_app()
    # Use in-memory DB for isolation
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })
    
    # Create all tables
    with app.app_context():
        db.drop_all()
        db.create_all()
    
    # Create a test client that preserves the session across requests
    client = app.test_client(use_cookies=True)

    print("\nRunning smoke tests...\n")

    # 1. Healthcheck
    rv = client.get("/healthcheck")
    assert rv.status_code == 200, f"/healthcheck {rv.status_code}"
    print("healthcheck ok")

    # 2. Create user
    rv = client.post("/create-account", json={
        "username": "smoketest", "password": "pass1234"
    })
    assert rv.status_code == 200, f"/create-account {rv.status_code}"
    print("create-account ok")

    # 3. Login
    rv = client.post("/login", json={
        "username": "smoketest",
        "password": "pass1234"
    })
    assert rv.status_code == 200, f"/login {rv.status_code}"
    print("login ok")
    
    # Get user ID for session
    with app.app_context():
        user = Users.query.filter_by(username="smoketest").first()
        user_id = user.id
    
    # Create a session with the user ID
    with client.session_transaction() as session:
        session['user_id'] = user_id

    # 4. Buy stock
    rv = client.post("/portfolio/buy", json={
        "symbol": "MSFT", "quantity": 1
    })
    assert rv.status_code == 200, f"/portfolio/buy {rv.status_code}"
    print("portfolio/buy ok")

    # 5. Get holding
    rv = client.get("/portfolio/holding/MSFT")
    assert rv.status_code == 200, f"/portfolio/holding/MSFT {rv.status_code}"
    print("portfolio/holding/MSFT ok")

    # 6. Delete holding
    rv = client.delete("/portfolio/holding/MSFT")
    assert rv.status_code == 200, f"/portfolio/holding/MSFT DELETE {rv.status_code}"
    print("portfolio/holding/MSFT DELETE ok")

    # 7. Clear portfolio (should still succeed)
    rv = client.delete("/portfolio/clear")
    assert rv.status_code == 200, f"/portfolio/clear {rv.status_code}"
    print("portfolio/clear ok")

    # 8. Update password
    rv = client.put("/update-password", json={
        "new_password": "newpass5678"
    })
    assert rv.status_code == 200, f"/update-password {rv.status_code}"
    print("update-password ok")

    # 9. Logout
    rv = client.post("/logout")
    assert rv.status_code == 200, f"/logout {rv.status_code}"
    print("logout ok")

    print("\nAll smoke tests passed!\n")

if __name__ == "__main__":
    try:
        run_smoke_tests()
    except AssertionError as e:
        print(f"\nSmoke test failed: {e}\n")
        sys.exit(1)
    sys.exit(0)