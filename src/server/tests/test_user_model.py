# vim: set fileencoding=utf-8 :
from madacraserver.db.user import userManager
from .common import MadacraTestCase


class UserModelTest(MadacraTestCase):
    def test_password(self):
        """UserManager.hash_password and UserManager.check_passwords work"""
        with self.app.app_context():
            user = {
                    "username": "Testuser1",
                    "password": userManager.hash_password("testpassword"),
                    }
            userManager.collection.save(user)

            fetched_user = userManager.collection.find_one({"username": "Testuser1"})
            self.assertTrue(userManager.check_passwords("testpassword", fetched_user["password"]))
            self.assertFalse(userManager.check_passwords("nottestpassword", fetched_user["password"]))
