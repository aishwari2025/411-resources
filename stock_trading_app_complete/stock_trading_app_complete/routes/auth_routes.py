"""
authentication routes for user account management.

this module defines endpoints for account creation, login, logout, and password updates.
uses Flask-Login for session-based authentication and SQLAlchemy for persistence.
"""

from flask import Blueprint, request, jsonify, session
from models.user_model import Users, db
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/create-account", methods=["POST"])
def create_account():
    """
    create a new user account with a username and password.

    request JSON:
        - username (str): the desired username.
        - password (str): the plain-text password.

    returns:
        - 200 OK if account is successfully created.
        - 400 Bad Request if the username already exists.
    """
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    if Users.query.filter_by(username=username).first():
        return {"message": "Username already exists"}, 400
    salt, hashed = Users._generate_hashed_password(password)
    user = Users(username=username, salt=salt, password=hashed)
    db.session.add(user)
    db.session.commit()
    return {"message": "Account created successfully"}, 200

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    authenticate a user and start a session.

    request JSON:
        - username (str): The username.
        - password (str): The plain-text password.

    returns:
        - 200 OK if credentials are valid and session started.
        - 401 Unauthorized if credentials are invalid.
    """
    data = request.get_json()
    user = Users.query.filter_by(username=data["username"]).first()
    if user and user.verify_password(data["password"]):
        login_user(user)
        return {"message": "Logged in successfully"}
    return {"message": "Invalid credentials"}, 401

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    log out the currently authenticated user.

    returns:
        - 200 OK with a confirmation message.
    """
    logout_user()
    return {"message": "Logged out"}

@auth_bp.route("/update-password", methods=["PUT"])
@login_required
def update_password():
    """
    update the password for the currently logged-in user.

    request JSON:
        - new_password (str): the new plain-text password.

    returns:
        - 200 OK if the password was successfully updated.
    """
    data = request.get_json()
    user = Users.query.get(session["_user_id"])
    salt, hashed = Users._generate_hashed_password(data["new_password"])
    user.salt = salt
    user.password = hashed
    db.session.commit()
    return {"message": "Password updated"}
