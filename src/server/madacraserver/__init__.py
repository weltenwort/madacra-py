# vim: set fileencoding=utf-8 :
import logging
from logging.handlers import WatchedFileHandler

from flask import Flask
from flask.ext.assets import Environment, Bundle


def create_app(config_filename=None):
    from db import db_manager
    #from server.login import login_manager

    app = Flask(__name__, instance_relative_config=True)
    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

    app.config.from_pyfile("default_settings.py")
    if config_filename is not None:
        app.config.from_pyfile(config_filename)
    app.config.from_envvar('MADACRA_SERVER_SETTINGS', silent=True)

    if not app.debug:
        file_handler = WatchedFileHandler(app.config["LOG_FILENAME"])
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

    assets = Environment(app)

    js_lib_assets = Bundle(
            "scripts/jquery-1.7.2.min.js",
            #"scripts/jquery-ui-1.8.16.custom.min.js",
            #"scripts/bootstrap.min.js",
            "scripts/angular-1.0.1.min.js",
            "scripts/sugar-1.2.5.min.js",
            "scripts/socket.io.min.js",
            #"scripts/jquery.couch.js",
            output="madacra_lib.js",
            )
    js_app_assets = Bundle(
            "lib/*.coffee",
            filters=["coffeescript", "rjsmin"],
            output="madacra_app.js",
            )
    #css_lib_assets = Bundle(
            ##"stylesheets/jquery-ui-1.8.16.custom.css",
            #filters=["cssmin", ],
            #output="madacra_lib.css",
            #)
    css_app_assets = Bundle(
            "stylesheets/madacra.less",
            filters=["less", "cssmin"],
            output="madacra_app.css",
            )
    assets.register("js_lib", js_lib_assets)
    assets.register("js_app", js_app_assets)
    #assets.register("css_lib", css_lib_assets)
    assets.register("css_app", css_app_assets)

    db_manager.init_app(app)
    #login_manager.setup_app(app)

    from views.index import index_blueprint
    from views.socket import socketio_blueprint
    app.register_blueprint(index_blueprint)
    app.register_blueprint(socketio_blueprint, url_prefix="/socket.io")
    #app.register_blueprint(blueprint_frontend)
    #app.register_blueprint(blueprint_entry, url_prefix="/entry")
    #app.register_blueprint(blueprint_filter, url_prefix="/filter")
    #app.register_blueprint(blueprint_pinboard, url_prefix="/pinboards")

    return app
