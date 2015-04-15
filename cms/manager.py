__author__ = 'Gareth Coles'

import cyclone.web
import sys
import yaml

from twisted.internet import reactor
from twisted.python import log

from cms.database.manager import DatabaseManager
from cms.database.schema.definitions import schemas


class Manager(object):
    application = None
    db = None
    database_config = None

    def __init__(self):
        self.database_config = yaml.load(open("config/database.yml", "r"))
        self.db = DatabaseManager(self.database_config.get("mongo", {}))

        for key, value in schemas.iteritems():
            self.db.add_schema(key, value)

        self.db.setup()

        self.application = cyclone.web.Application([
            (r"/", MainHandler)
        ])
        log.startLogging(sys.stdout)

        reactor.listenTCP(8888, self.application)

    def run(self):
        reactor.run()


class MainHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
