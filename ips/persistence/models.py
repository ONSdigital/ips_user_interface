import hashlib
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.id = hashlib.sha512(username.encode('ascii'))

    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User %r>' % self.username


