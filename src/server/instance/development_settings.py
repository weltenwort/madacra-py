# vim: set fileencoding=utf-8 :
import os

base_path = os.path.dirname(__file__)

DEBUG = True
TESTING = True
ASSETS_DEBUG = False
ASSETS_CACHE = False
ASSETS_MANIFEST = "file"
ASSETS_AUTO_BUILD = False
SECRET_KEY = '2gfOb@tiNQ;d5Mla[HKWMlTfgge.0Cjp'
LOG_FILENAME = "madacra_server.log"
SOCKETIO_NAMESPACE = "madacra"
MONGO_HOST = "localhost"
MONGO_DBNAME = "madacra"
