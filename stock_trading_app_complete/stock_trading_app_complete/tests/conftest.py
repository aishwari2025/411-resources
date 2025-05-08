"""
pytest fixtures for setting up the Flask application, database, and authenticated client.

these fixtures provide reusable components for testing:
- a Flask app instance with an in-memory database
- a test client for making HTTP requests
- a SQLAlchemy session bound to the app context
- authentication headers for simulating a logged-in user
"""

import pytest
from app import create_app, db

@pytest.fixture
def app():
    """
    fixture to create and configure a Flask app instance for testing.

    uses an in-memory SQLite database and initializes the schema before yielding.
    cleans up the session and drops all tables after tests complete.

    yields:
        Flask: the configured Flask application instance.
    """
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
    """
    fixture to provide a Flask test client for making HTTP requests.

    args:
        app (Flask): the test application instance.

    returns:
        FlaskClient: a test client bound to the app.
    """
    return app.test_client()

@pytest.fixture
def session(app):
    """
    fixture to provide a SQLAlchemy session scoped to the test app context.

    yields:
        session: the active SQLAlchemy session.
    """
    with app.app_context():
        yield db.session
@pytest.fixture
def auth_headers(client):
    """
    fixture to create a test user and return authenticated headers.

    performs user registration and login via the test client to simulate
    a logged-in session using cookies.

    args:
        client (FlaskClient): the Flask test client.

    returns:
        dict: a dictionary containing the 'Cookie' header if login succeeds,
              or an empty dictionary otherwise.
    """
    client.post("/create-account", json={"username": "testuser", "password": "testpass"})
    
    response = client.post("/login", json={"username": "testuser", "password": "testpass"})
    
    cookie = response.headers.get("Set-Cookie")
    if cookie:
       
        return {"Cookie": cookie}
    else:
        return {}