"""
user model definition for authentication and account management.

this module defines the Users database model using SQLAlchemy and integrates
with Flask-Login for session-based user authentication. it includes utilities
for password hashing and verification.
"""

import hashlib
import os
from flask_login import UserMixin
from app import db, login_manager

class Users(db.Model, UserMixin):
    """
    SQLAlchemy model for application users.

    attributes:
        id (int): primary key user ID.
        username (str): unique username for login.
        salt (str): salt used in password hashing.
        password (str): hashed password.

    methods:
        _generate_hashed_password(password): generates a salt and hashed password.
        verify_password(password): verifies a plaintext password against stored hash.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    salt = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    @staticmethod
    def _generate_hashed_password(password: str):
        """
        generate a unique salt and hashed password from a plaintext password.

        args:
            password (str): the user's plaintext password.

        returns:
            tuple: A (salt, hashed_password) pair using SHA-256.
        """
        salt = os.urandom(16).hex()
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        return salt, hashed_password

    def verify_password(self, password: str) -> bool:
        """
        verify a given plaintext password against the stored hashed password.

        args:
            password (str): the plaintext password to verify.

        returns:
            bool: True if the password is correct, False otherwise.
        """
        return self.password == hashlib.sha256((password + self.salt).encode()).hexdigest()

@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login user loader callback.

    args:
        user_id (int): the user ID stored in the session.

    returns:
        Users: the user object corresponding to the ID, or None if not found.
    """
    return Users.query.get(int(user_id))
