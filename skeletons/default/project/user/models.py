# user/models.py
"""User models."""


import datetime

from .. import db, bcrypt


class User(db.Model):
    """User table."""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, first_name, last_name, email, password, admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def fullname(self):
        return " ".join([self.first_name, self.last_name])

    def __str__(self):
        return "User {0}: {1}".format(self.id, self.fullname())

    def __repr__(self):
        return "[{0} {1} id: {2}]".format(self.__class__.__name__,
                                          type(self), self.id)
