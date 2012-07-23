# vim: set fileencoding=utf-8 :
import logging

import trafaret as t

from base import MadacraNamespace
from ..db.user import user_manager


class IdentityNamespace(MadacraNamespace):
    def initialize(self):
        print("id namespace initialized", self.session)

    def recv_connect(self):
        print("id connected")

    def on_login(self, data):
        try:
            safe_data = t.Dict({
                u"username": t.String,
                u"password": t.String,
                }).check(data)
        except t.DataError:
            logging.exception("Received invalid data: {}".format(data))
            return

        user_id = user_manager.check_login(safe_data[u"username"], safe_data[u"password"])

        if user_id is not None:
            self.session["user_id"] = user_id
            self.emit("changed", {
                "token": user_manager.create_identity_cookie(user_id),
                })
