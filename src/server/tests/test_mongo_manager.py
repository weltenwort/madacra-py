# vim: set fileencoding=utf-8 :
from unittest import TestCase

from flask import Flask

from madacraserver.db.manager import (
        CollectionIndex,
        CollectionManager,
        MongoManager,
        )


class MongoManagerTest(TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update({
            "MONGO_HOST": "localhost",
            "MONGO_DBNAME": "madacra_manager_test",
            "TESTING": True,
            })
        self.manager = MongoManager()
        self.addCleanup(self._delete_db)

    def _delete_db(self):
        with self.app.app_context():
            self.manager.cx.drop_database(self.app.config["MONGO_DBNAME"])

    def test_manager_collection_manager_class(self):
        """MongoManager.CollectionManager property returns a bound
        collection manager suitable for subclassing"""
        manager = self.manager

        #@manager.bind_collection
        class TestManager(manager.CollectionManager):
            name = "test_collection"

        tm = TestManager()

        manager.init_app(self.app)

        with self.app.app_context():
            tm.collection.insert({u"attr1": u"value1"})
            self.assertEqual(len(list(tm.collection.find())), 1)

    def test_manager_collection_manager_registration(self):
        """MongoManager.bind_collection binds collection manager"""
        manager = self.manager

        @manager.bind_collection
        class TestManager(CollectionManager):
            name = "test_collection"

        tm = TestManager()

        manager.init_app(self.app)

        with self.app.app_context():
            tm.collection.insert({u"attr1": u"value1"})
            self.assertEqual(len(list(tm.collection.find())), 1)

    def test_manager_indices(self):
        """MongoManager.init_app ensures collection indices"""
        manager = self.manager

        class TestManager(manager.CollectionManager):
            name = "test_collection"
            indices = [
                    CollectionIndex("foo"),
                    CollectionIndex("bar"),
                    ]

        tm = TestManager()

        manager.init_app(self.app)

        with self.app.app_context():
            self.assertEqual(len(manager.db.test_collection.index_information()), 3)
