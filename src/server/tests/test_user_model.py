# vim: set fileencoding=utf-8 :
from madacraserver.db.user import user_manager
from .common import MadacraTestCase


class UserModelTest(MadacraTestCase):
    model = 1
    user = 1

    def test_password(self):
        """UserManager.hash_password and UserManager.check_passwords work"""
        with self.app.app_context():
            user = {
                    "username": "Testuser1",
                    "password": user_manager.hash_password("testpassword"),
                    }
            user_manager.collection.save(user)

            fetched_user = user_manager.collection.find_one({"username": "Testuser1"})
            self.assertTrue(user_manager.check_passwords("testpassword", fetched_user["password"]))
            self.assertFalse(user_manager.check_passwords("nottestpassword", fetched_user["password"]))

    def test_check_login(self):
        """UserManager.check_login returns user or None"""
        with self.app.app_context():
            user = {
                    "username": "Testuser1",
                    "password": user_manager.hash_password("testpassword"),
                    }
            user_manager.collection.save(user)

            self.assertNotEqual(user_manager.check_login("Testuser1", "testpassword"), None)
            self.assertEqual(user_manager.check_login("Testuser2", "testpassword"), None)
            self.assertEqual(user_manager.check_login("Testuser1", "nottestpassword"), None)

    def test_identity_token(self):
        """UserManager can create and parse signed identity tokens"""
        token = user_manager.create_identity_cookie("userid1")
        self.assertEqual(user_manager.parse_identity_cookie(token), "userid1")
