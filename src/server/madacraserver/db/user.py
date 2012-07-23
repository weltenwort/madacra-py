# vim: set fileencoding=utf-8 :
import hashlib
import os

from decotrace import traced
from itsdangerous import Signer

from . import db_manager


class UserManager(db_manager.CollectionManager):
    name = "user"
    indices = [
            db_manager.CollectionIndex("username"),
            ]

    def hash_password(self, password, salt=None):
        if salt is None:
            h = hashlib.sha256()
            h.update(os.urandom(256))
            salt = h.hexdigest()
        h = hashlib.sha256()
        h.update(salt)
        h.update(password)
        return salt + h.hexdigest()

    def check_passwords(self, password, hashed_password):
        return self.hash_password(password, hashed_password[:64]) == hashed_password

    @traced
    def check_login(self, username, password):
        user = self.collection.find_one({"username": username})
        if user is not None and self.check_passwords(password, user["password"]):
            return str(user["_id"])
        else:
            return None

    @property
    def signer(self):
        if getattr(self, "_signer", None) is None:
            self._signer = Signer(self.manager.app.config["SECRET_KEY"])
        return self._signer

    def parse_identity_cookie(self, identity_cookie):
        return self.signer.unsign(identity_cookie)

    def create_identity_cookie(self, user_id):
        return self.signer.sign(user_id)


user_manager = UserManager()

#class User(Document):
    #"""User model."""
    #username = fields.StringField(required=True)
    #password = fields.StringField(required=True)

    #def set_password(self, password):
        #h = hashlib.sha256()
        #h.update(os.urandom(256))
        #salt = h.hexdigest()
        #self.password = salt + self._hash_password(password, salt=salt)

    #@property
    #def salt(self):
        #return self.password[:64]

    #def _hash_password(self, password, salt=None):
        #if salt is None:
            #salt = self.salt
        #h = hashlib.sha256()
        #h.update(salt)
        #h.update(password)
        #return h.hexdigest()

    #def check_password(self, password):
        #return self.salt + self._hash_password(password) == self.password

    #def get_id(self):
        #return self.id
