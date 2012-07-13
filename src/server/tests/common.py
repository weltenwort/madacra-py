# vim: set fileencoding=utf-8 :
import os
import unittest

from madacraserver import create_app
from madacraserver.db import db_manager


class MadacraTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_filename=os.path.join(os.path.dirname(__file__), "test_settings.py"))
        self.addCleanup(self._delete_db)

    def _delete_db(self):
        with self.app.app_context():
            db_manager.cx.drop_database(db_manager.db.name)
