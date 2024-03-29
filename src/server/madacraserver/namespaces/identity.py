# vim: set fileencoding=utf-8 :
import logging

import itsdangerous

from base import MadacraNamespace
from ..db.user import user_manager
from ..messaging import (
        message_hub,
        MessageReactor,
        )
from ..utils import validation as t


class IdentityNamespace(MadacraNamespace):
    def initialize(self):
        print("id namespace initialized", self.session)
        self.reactor = self.add_job(MessageReactor.from_hub(message_hub))
        self.reactor.start()

    def login_user(self, user):
        """Store the current user in the session and emit the
        loginSuccessful event to the client and message hub."""
        self.user = user
        message_hub.send_message("identity:loginSuccessful:{}".format(user["_id"]), {
            "user_id": str(user["_id"]),
            "username": user["username"],
            })
        self.emit("loginSuccessful", {
            "token": user_manager.create_identity_cookie(user["_id"]),
            "username": user["username"],
            })

    def logout_user(self):
        """Remove any refernce to the current user from the session. If the
        user was logged in previously, emit the logoutSuccessful event to the
        client and message hub."""
        old_user = self.user
        self.user = None
        if old_user is not None:
            message_hub.send_message("identity:logoutSuccessful:{}".format(old_user["_id"]), {
                "user_id": str(old_user["_id"]),
                "username": str(old_user["username"]),
                })
            self.emit("logoutSuccessful", {})

    def on_login(self, data):
        """Sent by the client to request being logged in using username and
        password.

        Possible server responses:

        loginSuccessful
          sent when the user has been logged in successfully

        loginFailed
          sent when the user could not be loggen in successfully
        """
        try:
            safe_data = t.Dict({
                t.Key(u"username") >> "username": t.String,
                t.Key(u"password") >> "password": t.String,
                }).check(data)
        except t.DataError:
            self.emit("loginFailed", {
                "reason": "invalidRequest"
                })
            logging.exception("Received invalid data: {}".format(data))
            return

        user = user_manager.check_login(safe_data["username"], safe_data["password"])

        if user is not None:
            self.login_user(user)
        else:
            self.logout_user()
            message_hub.send_message("identity:loginFailed:{}".format(safe_data["username"]), {
                "username": safe_data["username"],
                })
            self.emit("loginFailed", {
                "reason": "invalidCredentials",
                "username": safe_data["username"],
                "password": safe_data["password"],
                })

    def on_logout(self, data):
        """Sent by the client to request being logged out."""
        self.logout_user()

    def on_identify(self, data):
        """Sent by the client to request being logged in using an
        authentication token."""
        try:
            safe_data = t.Dict({
                t.Key(u"token") >> "token": t.String,
                }).check(data)
        except t.DataError:
            self.emit("signupFailed", {
                "reason": "invalidRequest"
                })
            logging.exception("Received invalid data: {}".format(data))
            return

        try:
            user_id = t.ObjectId().check(user_manager.parse_identity_cookie(safe_data["token"]))
            user = user_manager.collection.find_one(user_id)
            message_hub.send_message("identity:identificationSuccessful:{}".format(user["_id"]), {
                "user_id": str(user["_id"]),
                "username": user["username"],
                })
            self.login_user(user)
        except itsdangerous.BadSignature:
            message_hub.send_message("identity:identificationFailed", {})
            self.emit("identificationFailed", {
                "reason": "badSignature",
                "token": safe_data["token"],
                })

    def on_signup(self, data):
        """Sent by the client to request creation of a new user account."""
        try:
            safe_data = t.Dict({
                t.Key(u"username") >> "username": t.String,
                t.Key(u"password") >> "password": t.String,
                }).check(data)
        except t.DataError:
            self.emit("signupFailed", {
                "reason": "invalidRequest"
                })
            logging.exception("Received invalid data: {}".format(data))
            return

        user = user_manager.create_user(safe_data["username"], safe_data["password"])

        if user is not None:
            message_hub.send_message("identity:signupSuccessful:{}".format(user["_id"]), {
                "user_id": str(user["_id"]),
                "username": user["username"],
                })
            self.login_user(user)
        else:
            self.logout_user()
            message_hub.send_message("identity:signupFailed:{}".format(safe_data["username"]), {
                "username": safe_data["username"],
                })
            self.emit("signupFailed", {
                "reason": "invalidUsername",
                "username": safe_data["username"],
                })
