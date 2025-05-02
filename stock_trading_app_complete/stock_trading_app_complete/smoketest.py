#!/usr/bin/env python3
"""
smoketest.py

Basic “smoke” test: start up the Flask app, hit each critical endpoint,
and verify we get a 200 and minimal expected JSON.
"""

import os
# Set testing environment values before importing the app
os.environ.setdefault("ALPHA_VANTAGE_API_KEY", "demo")
os.environ.setdefault("SECRET_KEY", "test_secret")

import sys
from app import create_app, db
# Ensure SQLAlchemy sees your user table
import models.user_model

def run_smoke_tests():
    # Create and configure the app for testing
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    # Build the in-memory database schema
    with app.app_context():
        db.drop_all()
        db.create_all()

    client = app.test_client()

    print("\n🧪 Running smoke tests...\n")

    # 1. Healthcheck
    rv = client.get("/healthcheck")
    assert rv.status_code == 200, f"/healthcheck returned {rv.status_code}"
    assert rv.get_json() is not None, "/healthcheck did not return JSON"
    print("✔️ /healthcheck ok")

    # 2. Create account
    rv = client.post(
        "/create-account",
        json={"username": "smoketest", "password": "pass1234"}
    )
    assert rv.status_code == 200, f"/create-account returned {rv.status_code}"
    print("✔️ /create-account ok")

    # 2a. Duplicate account creation should be rejected
    rv = client.post(
        "/create-account",
        json={"username": "smoketest", "password": "pass1234"}
    )
    assert rv.status_code == 400, f"/create-account duplicate returned {rv.status_code}"
    print("✔️ /create-account duplicate ok")

    # 3. Login
    rv = client.post(
        "/login",
        json={"username": "smoketest", "password": "pass1234"}
    )
    assert rv.status_code == 200, f"/login returned {rv.status_code}"
    print("✔️ /login ok")

    # 4. Portfolio operations
    rv = client.post("/portfolio/buy", json={"symbol": "AAPL", "quantity": 1})
    assert rv.status_code == 200, f"/buy-stock returned {rv.status_code}"
    print("✔️ /buy-stock ok")

    rv = client.post("/portfolio/sell", json={"symbol": "AAPL", "quantity": 1})
    assert rv.status_code == 200, f"/sell-stock returned {rv.status_code}"
    print("✔️ /sell-stock ok")

    rv = client.get("/portfolio")
    assert rv.status_code == 200, f"/portfolio returned {rv.status_code}"
    print("✔️ /portfolio ok")

    rv = client.get("/stock/lookup", query_string={"symbol": "AAPL"})
    assert rv.status_code == 200, f"/lookup-stock returned {rv.status_code}"
    print("✔️ /lookup-stock ok")

    rv = client.get("/portfolio/value")
    assert rv.status_code == 200, f"/portfolio-value returned {rv.status_code}"
    print("✔️ /portfolio-value ok")

    rv = client.delete("/portfolio/clear")
    assert rv.status_code == 200, f"/portfolio/clear returned {rv.status_code}"
    print("✔️ /portfolio/clear ok")

    # 5. Update password
    rv = client.put("/update-password", json={"new_password": "newpass5678"})
    assert rv.status_code == 200, f"/update-password returned {rv.status_code}"
    print("✔️ /update-password ok")

    # 6. Logout
    rv = client.post("/logout")
    assert rv.status_code == 200, f"/logout returned {rv.status_code}"
    print("✔️ /logout ok")

    print("\n🎉 All smoke tests passed!\n")

if __name__ == "__main__":
    try:
        run_smoke_tests()
    except AssertionError as e:
        print(f"\n❌ Smoke test failed: {e}\n")
        sys.exit(1)
    sys.exit(0)