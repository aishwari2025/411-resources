import pytest
from app import create_app, db

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def auth_headers(client):
    client.post("/create-account", json={"username": "auto", "password": "pass"})
    client.post("/login", json={"username": "auto", "password": "pass"})
    return {"Content-Type": "application/json"}
