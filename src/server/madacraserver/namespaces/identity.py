# vim: set fileencoding=utf-8 :
import logging

import trafaret as t

from base import MadacraNamespace
from ..db.user import user_manager
from ..messaging import (
        message_hub,
        MessageReactor,
        )


class IdentityNamespace(MadacraNamespace):
    def initialize(self):
        print("id namespace initialized", self.session)
        self.reactor = self.add_job(MessageReactor.from_hub(message_hub))
        self.reactor.start()

    def login_user(self, user_id):
        self.session["user_id"] = user_id
        message_hub.send_message("identity:loginSuccessful:{}".format(user_id), {
            "user_id": user_id,
            })
        self.emit("loginSuccessful", {
            "token": user_manager.create_identity_cookie(user_id),
            })

    def logout_user(self):
        old_user_id = self.session["user_id"]
        self.session["user_id"] = None
        if old_user_id is not None:
            message_hub.send_message("identity:logoutSuccessful:{}".format(old_user_id), {
                "user_id": old_user_id,
                })
            self.emit("logoutSuccessful", {})

    def on_login(self, data):
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

        user_id = user_manager.check_login(safe_data["username"], safe_data["password"])

        if user_id is not None:
            self.login_user(user_id)
        else:
            self.logout_user()
            message_hub.send_message("identity:loginFailed:{}".format(safe_data["username"]), {
                "username": safe_data["username"],
                })
            self.emit("loginFailed", {
                "reason": "invalidCredentials",
                })

    def on_logout(self, data):
        self.logout_user()

    def on_signup(self, data):
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

        user_id = user_manager.create_user(safe_data["username"], safe_data["password"])

        if user_id is not None:
            message_hub.send_message("identity:signupSuccessful:{}".format(user_id), {
                "user_id": user_id,
                "username": safe_data["username"],
                })
            self.login_user(user_id)
        else:
            self.logout_user()
            message_hub.send_message("identity:signupFailed:{}".format(safe_data["username"]), {
                "username": safe_data["username"],
                })
            self.emit("signupFailed", {
                "reason": "invalidUsername",
                })
