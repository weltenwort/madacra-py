# vim: set fileencoding=utf-8 :
import hashlib
import os

from . import db


class User(db.Document):
    """User model."""
    username = db.StringField(required=True, unique=True)
    _password = db.StringField(db_field="password", required=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, password):
        h = hashlib.sha256()
        h.update(os.urandom(256))
        salt = h.hexdigest()
        self._password = salt + self._hash_password(password, salt=salt)

    @property
    def salt(self):
        return self._password[:64]

    def _hash_password(self, password, salt=None):
        if salt is None:
            salt = self.salt
        h = hashlib.sha256()
        h.update(salt)
        h.update(password)
        return h.hexdigest()

    def check_password(self, password):
        return self.salt + self._hash_password(password) == self._password

    def get_id(self):
        return self.id
