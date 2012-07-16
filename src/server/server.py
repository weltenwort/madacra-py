from gevent import monkey
monkey.patch_all(select=False)

from flask.ext.script import Command, Option
from socketio.server import SocketIOServer
import werkzeug.serving


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

    def handle(self, app, host, port):
        @werkzeug.serving.run_with_reloader
        def foo():
            server = SocketIOServer(
                    (host, port),
                    app,
                    namespace="socket.io",
                    policy_server=False
                    )
            server.serve_forever()
