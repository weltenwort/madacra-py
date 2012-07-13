# vim: set fileencoding=utf-8 :
from flask.ext.pymongo import PyMongo


class CollectionIndex(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __eq__(self, other):
        return self.args == other.args and self.kwargs == other.kwargs

    def ensure_index(self, collection):
        collection.ensure_index(*self.args, **self.kwargs)


class CollectionManager(object):
    manager = None
    name = None
    indices = set()

    def __init__(self, name=None):
        self.register_with_manager(self.manager)
        if name is not None:
            self.name = name

    def register_with_manager(self, manager):
        manager.register_collection_manager(self.name, self)

    @property
    def collection(self):
        return self.manager.db[self.name]

    def ensure_indices(self):
        for index in set(self.indices):
            if isinstance(index, CollectionIndex):
                index.ensure_index(self.collection)
            else:
                raise TypeError("Expected CollectionIndex, found {}.".format(type(index)))


class MongoManager(PyMongo):
    def __init__(self, app=None, config_prefix='MONGO', collection_manager_class=CollectionManager):
        self.app = None
        super(MongoManager, self).__init__(app, config_prefix)
        self.collection_manager_class = type("Bound{}".format(collection_manager_class.__name__), (collection_manager_class, ), {"manager": self})
        self.collection_managers = {}

    def register_collection_manager(self, collection_name, collection_manager):
        if collection_name in self.collection_managers:
            raise KeyError("A manager for collection '{}' has already been registered.".format(collection_name))
        else:
            self.collection_managers[collection_name] = collection_manager
            if self.app is not None:
                with self.app.app_context():
                    collection_manager.ensure_indices()

    def init_app(self, app, config_prefix='MONGO'):
        super(MongoManager, self).init_app(app, config_prefix)
        with app.app_context():
            self.ensure_indices()
        self.app = app

    def ensure_indices(self):
        for collection_manager in self.collection_managers.itervalues():
            collection_manager.ensure_indices()

    def bind_collection(self, collection_manager_class):
        return type(collection_manager_class.__name__, (collection_manager_class, ), {"manager": self})

    @property
    def CollectionManager(self):
        return self.collection_manager_class

    CollectionIndex = CollectionIndex
