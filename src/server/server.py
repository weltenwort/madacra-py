from gevent import monkey
monkey.patch_all()

from flask import current_app
from flask.ext.script import Command, Option
from socketio.server import SocketIOServer


class RunSocketIOServer(Command):
    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port

    def get_options(self):
        options = [
                Option("-t", "--host", dest="host", default=self.host),
                Option("-p", "--port", dest="port", default=self.port, type=int),
                ]

        return options

    def run(self, host, port):
        app = current_app
        server = SocketIOServer(
                (host, port),
                app,
                namespace=app.config["SOCKETIO_NAMESPACE"],
                policy_server=False
                )
        server.serve_forever()
