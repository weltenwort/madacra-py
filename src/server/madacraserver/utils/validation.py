# vim: set fileencoding=utf-8 :
import datetime

from bson.objectid import ObjectId as MongoObjectId
from dateutil import parser as dateutil_parser
from trafaret import (  # noqa
        Any,
        Bool,
        Call,
        Callable,
        catch_error,
        DataError,
        Dict,
        Enum,
        Float,
        Forward,
        Int,
        Key,
        List,
        Mapping,
        Null,
        Or,
        String,
        Trafaret,
        Type,
        guard,
        )


class NoKeyDefault(object):
    pass


class Key(Key):
    def __init__(self, name, default=NoKeyDefault, optional=False, to_name=None, trafaret=None):
        self.name = name
        self.to_name = to_name
        self.default = default
        self.optional = optional
        self.trafaret = trafaret or Any()

    @property
    def default(self):
        if callable(self._default) and self._default is not NoKeyDefault:
            return self._default()
        else:
            return self._default

    @default.setter # noqa
    def default(self, value):
        self._default = value

    def pop(self, data):
        if self.name in data or self.default is not NoKeyDefault:
            yield self.get_name(), catch_error(self.trafaret,
                    data.pop(self.name, self.default))
            raise StopIteration
        if not self.optional:
            yield self.name, DataError(error='is required')

    def make_optional(self):
        self.optional = True
        self.default = NoKeyDefault


class SerializableTrafaret(Trafaret):
    @classmethod
    def serialized(cls):
        return cls >> cls.serialize


class DateTime(SerializableTrafaret):
    def check_value(self, value):
        if isinstance(value, datetime.datetime):
            return value
        elif isinstance(value, basestring):
            return dateutil_parser.parse(value)
        elif value is None:
            return value
        else:
            self._failure("value should be a datetime or string")

    def __repr__(self):
        return "<DateTime>"

    @staticmethod
    def serialize(value):
        if isinstance(value, basestring):
            return value
        else:
            return value.isoformat()


class ObjectId(SerializableTrafaret):
    def check_and_return(self, value):
        if isinstance(value, MongoObjectId):
            return value
        elif isinstance(value, basestring):
            return MongoObjectId(value)
        elif isinstance(value, dict) and "$oid" in value:
            return MongoObjectId(value["$oid"])
        elif value is None:
            return value
        else:
            self._failure("value should be string or dict with $oid")

    def __repr__(self):
        return "<ObjectId>"

    @staticmethod
    def serialize(value):
        return str(value)
