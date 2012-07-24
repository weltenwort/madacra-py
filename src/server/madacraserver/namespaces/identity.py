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

    def on_login(self, data):
        try:
            safe_data = t.Dict({
                u"username": t.String,
                u"password": t.String,
                }).check(data)
        except t.DataError:
            self.emit("loginFailed", {
                "reason": "invalidRequest"
                })
            logging.exception("Received invalid data: {}".format(data))
            return

        user_id = user_manager.check_login(safe_data[u"username"], safe_data[u"password"])

        if user_id is not None:
            self.session["user_id"] = user_id
            message_hub.send_message("login:{}".format(user_id), {
                "user_id": user_id,
                })
            self.emit("loginSuccessful", {
                "token": user_manager.create_identity_cookie(user_id),
                })
        else:
            self.session["user_id"] = None
            self.emit("loginFailed", {})
