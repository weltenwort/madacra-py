# vim: set fileencoding=utf-8 :
#from db.user import user_manager


class SessionManager(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app


#@login_manager.user_loader
#def load_user(user_id):
    #user_manager.collection.find_one(user_id)
