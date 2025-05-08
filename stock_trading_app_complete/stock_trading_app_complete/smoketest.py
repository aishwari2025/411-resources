#!/usr/bin/env python3
"""
smoketest.py

Basic “smoke” test: start up the Flask app, hit each critical endpoint,
and verify we get a 200 and minimal expected JSON.
"""

import os
# Provide a dummy API key for tests to satisfy external_api requirement
os.environ["ALPHA_VANTAGE_API_KEY"] = "demo"
os.environ.setdefault("SECRET_KEY", "test_secret")

import sys
from app import create_app, db
import models.user_model


def run_smoke_tests():
    app = create_app()
    # Use in-memory DB and testing mode so tests are isolated
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    # Reset the database schema
    with app.app_context():
        db.drop_all()
        db.create_all()

    client = app.test_client()

    print("\nRunning smoke tests...\n")

    # 1. Healthcheck
    rv = client.get("/healthcheck")
    assert rv.status_code == 200, f"/healthcheck returned {rv.status_code}"
    data = rv.get_json()
    assert data is not None, "/healthcheck did not return JSON"
    print("healthcheck ok")

    # 2. Create account
    rv = client.post(
        "/create-account",
        json={"username": "smoketest", "password": "pass1234"}
    )
    assert rv.status_code == 200, f"/create-account {rv.status_code}"
    print("create-account ok")

    # 3. Login
    rv = client.post(
        "/login",
        json={"username": "smoketest", "password": "pass1234"}
    )
    assert rv.status_code == 200, f"/login {rv.status_code}"
    print("login ok")

    # 4. Portfolio trading endpoints
    rv = client.post(
        "/portfolio/buy",
        json={"symbol": "AAPL", "quantity": 1}
    )
    assert rv.status_code == 200, f"/portfolio/buy returned {rv.status_code}"
    print("portfolio/buy ok")

    rv = client.post(
        "/portfolio/sell",
        json={"symbol": "AAPL", "quantity": 1}
    )
    assert rv.status_code == 200, f"/portfolio/sell returned {rv.status_code}"
    print("portfolio/sell ok")

    rv = client.get("/portfolio")
    assert rv.status_code == 200, f"/portfolio {rv.status_code}"
    print("portfolio ok")

    # 5. Stock lookup
    rv = client.get(
        "/stock/lookup",
        query_string={"symbol": "AAPL"}
    )
    assert rv.status_code == 200, f"/stock/lookup returned {rv.status_code}"
    print("stock/lookup ok")

    # 6. Portfolio total value
    rv = client.get("/portfolio/value")
    assert rv.status_code == 200, f"/portfolio/value returned {rv.status_code}"
    print("portfolio/value ok")

    # 7. Update password
    rv = client.put(
        "/update-password",
        json={"old_password": "pass1234", "new_password": "newpass5678"}
    )
    assert rv.status_code == 200, f"/update-password {rv.status_code}"
    print("update-password ok")

    # 8. Logout
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