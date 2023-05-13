from datetime import datetime

from web import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    @classmethod
    def create_super_user(cls, **kwargs):
        kwargs.setdefault('is_admin', True)
        return cls(**kwargs)

    @classmethod
    def create_user(cls, **kwargs):
        kwargs.setdefault('is_admin', False)
        return cls(**kwargs)

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


def user_exists(email: str, password: str) -> User:
    """
    Check if a user exists in the database with the given email and password.

    Args:
        email (str): The email to check.
        password (str): The password to check.

    Returns:
        User: The user instance if found, or None if not found.
    """
    return User.query.filter_by(email=email, password=password).first()
