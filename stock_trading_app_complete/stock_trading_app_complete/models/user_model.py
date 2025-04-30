import hashlib
import os
from flask_login import UserMixin
from app import db, login_manager

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    salt = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    @staticmethod
    def _generate_hashed_password(password: str):
        salt = os.urandom(16).hex()
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        return salt, hashed_password

    def verify_password(self, password: str) -> bool:
        return self.password == hashlib.sha256((password + self.salt).encode()).hexdigest()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
