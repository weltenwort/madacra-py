# vim: set fileencoding=utf-8 :
from db.campaign import campaign_manager
from db.user import user_manager


def create_fixtures(app):
    with app.app_context():
        # create test users
        user_manager.create_user("user1", "password1")
        user1_id = user_manager.collection.find_one({"username": "user1"})["_id"]
        if campaign_manager.collection.find({"creation_user_id": user1_id}).count() == 0:
            campaign_manager.create_campaign("A Campaign for Testing 1", user1_id)
