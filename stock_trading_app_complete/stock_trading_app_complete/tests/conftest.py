import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session
@pytest.fixture
def auth_headers(client):
    client.post("/create-account", json={"username": "testuser", "password": "testpass"})
    
    response = client.post("/login", json={"username": "testuser", "password": "testpass"})
    
    cookie = response.headers.get("Set-Cookie")
    if cookie:
       
        return {"Cookie": cookie}
    else:
        return {}