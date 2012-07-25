# vim: set fileencoding=utf-8 :
from db.user import user_manager


def create_fixtures(app):
    with app.app_context():
        # create test users
        user_manager.create_user("user1", "password1")
