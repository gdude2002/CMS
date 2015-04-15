__author__ = 'Gareth Coles'

from datetime import datetime
from cms.database.schema.types import TypeAndMembershipCheckingSchema


schemas = {
    "post": TypeAndMembershipCheckingSchema({
        "markdown": basestring,
        "html": basestring,
        "title": basestring,
        "username": basestring,
        "slug": basestring,
        "author": basestring,
        "posted": datetime
    }),
    "page": TypeAndMembershipCheckingSchema({
        "markdown": basestring,
        "html": basestring,
        "title": basestring,
        "slug": basestring
    }),
    "user": TypeAndMembershipCheckingSchema({
        "username": basestring,
        "salt": basestring,
        "password": basestring,
        "avatar": basestring,
        "admin": bool
    }),
    "settings": TypeAndMembershipCheckingSchema({
        "name": basestring,
        "title": basestring,
        "theme": basestring
    }),
    "modules": TypeAndMembershipCheckingSchema({
        "type": basestring,
        "python": [None, basestring],
        "html": [None, basestring],
        "markdown": [None, basestring]
    }),
    "sessions": TypeAndMembershipCheckingSchema({
        "key": basestring,
        "username": basestring,
        "seen": datetime,
        "remember": bool
    })
}
