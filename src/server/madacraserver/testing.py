# vim: set fileencoding=utf-8 :
from db.user import user_manager


def create_fixtures(app):
    with app.app_context():
        # create test users
        user_manager.collection.update({
            u"username": "user1",
            },
            {
            u"username": "user1",
            u"password": user_manager.hash_password("password1"),
            }, upsert=True)
