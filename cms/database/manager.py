__author__ = 'Gareth Coles'

import datetime
import calendar

import pymongo
from pymongo.collection import ObjectId

from cms.singleton import Singleton


class DatabaseManager(object):
    __metaclass__ = Singleton

    client = None
    db = None
    schemas = {}

    def __init__(self, config):
        self.config = config

    def setup(self):
        if self.client is not None and self.db is not None:
            raise AlreadySetUpError()

        if self.config.get("default", True):
            client = pymongo.MongoClient()
            db = client[self.config.get("db", "cms")]
        else:
            auth = self.config.get("authentication", None)

            if auth is None or not auth.get("use", False):
                uri = "mongodb://%s:%s/%s" % (
                    self.config.get("host", "localhost"),
                    self.config.get("port", 27017),
                    self.config.get("db", "cms")
                )
            else:
                uri = "mongodb://%s:%s@%s:%s/%s" % (
                    auth["username"],
                    auth["password"],
                    self.config.get("host", "localhost"),
                    self.config.get("port", 27017),
                    self.config.get("db", "cms")
                )

            client = pymongo.MongoClient(uri)
            db = client[self.config.get("db", "cms")]

        self.client = client
        self.db = db

    def stringify(self, _in):
        """
        :type _in: dict, list
        """

        if isinstance(_in, dict):
            for key in _in.keys():
                if isinstance(_in[key], ObjectId):
                    _in[key] = str(_in[key])
                elif isinstance(_in[key], datetime.datetime):
                    _in[key] = calendar.timegm(_in[key].utctimetuple())
                elif isinstance(_in[key], list):
                    _in[key] = self.stringify(_in[key])
                elif isinstance(_in[key], dict):
                    _in[key] = self.stringify(_in[key])
                else:
                    continue

        elif isinstance(_in, list):
            done = []
            for element in _in:
                if isinstance(element, ObjectId):
                    done.append(str(element))
                elif isinstance(element, datetime.datetime):
                    done.append(calendar.timegm(element.utctimetuple()))
                elif isinstance(element, list):
                    done.append(self.stringify(element))
                elif isinstance(element, dict):
                    done.append(self.stringify(element))
                else:
                    done.append(element)
            _in = done

        return _in

    def add_schema(self, collection, schema):
        self.schemas[collection] = schema

    def get_collection(self, collection):
        return Collection(self.db[collection],
                          self.schemas.get(collection, None))


class Collection(object):
    coll = None
    schema = None

    def __init__(self, collection, schema=None):
        self.coll = collection
        self.schema = schema

    def __getattribute__(self, item):
        try:
            # Check whether we defined our own attribute
            return object.__getattribute__(self, item)
        except AttributeError:
            # If not, check if it exists on the collection
            return self.coll.__getattribute__(item)

    def insert(self, data):
        if self.schema is None:
            return self.coll.insert(data)

        if not self.schema.validate(data):
            raise ValidationError()

        return self.coll.insert(data)

    def update(self, criteria, data, *args, **kwargs):
        if self.schema is None:
            return self.coll.update(criteria, data, *args, **kwargs)

        if not self.schema.validate(data):
            raise ValidationError()

        return self.coll.update(criteria, data, *args, **kwargs)


class AlreadySetUpError(Exception):
    message = "MongoDB has already been configured"


class ValidationError(Exception):
    message = "Data does not pass schema validation"
