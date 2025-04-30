from flask import Blueprint, request, jsonify, session
from models.user_model import Users, db
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/create-account", methods=["POST"])
def create_account():
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
    data = request.get_json()
    user = Users.query.filter_by(username=data["username"]).first()
    if user and user.verify_password(data["password"]):
        login_user(user)
        return {"message": "Logged in successfully"}
    return {"message": "Invalid credentials"}, 401

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return {"message": "Logged out"}

@auth_bp.route("/update-password", methods=["PUT"])
@login_required
def update_password():
    data = request.get_json()
    user = Users.query.get(session["_user_id"])
    salt, hashed = Users._generate_hashed_password(data["new_password"])
    user.salt = salt
    user.password = hashed
    db.session.commit()
    return {"message": "Password updated"}
