# vim: set fileencoding=utf-8 :
from flask import (
        Blueprint,
        current_app,
        request,
        )
from socketio import socketio_manage
from socketio.namespace import BaseNamespace

from ..namespaces import identity

socketio_blueprint = Blueprint("socketio", __name__)


@socketio_blueprint.route("/<path:path>")
def view_socketio(path):
    socketio_manage(request.environ, {
        "/identity": identity.IdentityNamespace
        },
        request=current_app._get_current_object(),
        )
