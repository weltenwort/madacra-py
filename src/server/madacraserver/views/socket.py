# vim: set fileencoding=utf-8 :
from flask import (
        Blueprint,
        current_app,
        request,
        )
from socketio import socketio_manage
from socketio.namespace import BaseNamespace

socketio_blueprint = Blueprint("socketio", __name__)


@socketio_blueprint.route("/<path:path>")
def view_socketio(path):
    socketio_manage(request.environ, {"": TempNamespace})


class TempNamespace(BaseNamespace):
    def initialize(self):
        print("namespace initialized")

    def recv_connect(self):
        print("connected")

    def on_test(self):
        print("testing")
