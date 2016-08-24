"""
sqery.py: Helpers for working with databases

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import print_function

import os
import logging
from functools import wraps

from bottle import request
from bottle_utils.common import to_unicode
from squery_lite.squery import Database, Connection

from ..app.exts import container as exts


def ilike(s1, s2):
    """
    Case-isensitive version of the LIKE expression
    """
    s1 = to_unicode(s1).lower()
    s2 = to_unicode(s2).lower()
    if s2.startswith('%') and s2.endswith('%'):
        return s2 in s1
    if s2.startswith('%'):
        return s1.endswith(s2)
    return s1.startswith(s2)


def ulower(s):
    """
    Convert a string to lower-case (like SQLite's lower() but with unicode)
    """
    return to_unicode(s).lower()


class IsCandidate(object):
    """
    Custom function that determines whether an item is a bin candidate
    """
    def __init__(self, limit):
        self.limit = limit
        self.total = 0

    def __call__(self, size, votes):
        if votes < 1:
            return 0
        self.total += size
        return self.total <= self.limit


class DatabaseContainer(object):
    def __init__(self, dbdict={}):
        self.dbdict = dbdict

    def append(self, name, db):
        self.dbdict[name] = db

    def __getattr__(self, name):
        return self.dbdict[name]

    def __getitem__(self, name):
        return self.dbdict[name]

    def __iter__(self):
        return iter(self.dbdict.items())


def database_plugin():
    def plugin(callback):
        @wraps(callback)
        def wrapper(*args, **kwargs):
            request.db = exts.db
            return callback(*args, **kwargs)
        return wrapper
    plugin.name = 'squery'
    return plugin


def pre_init():
    logging.info('Connecting to databases')
    config = exts.config
    bin_limit = config['bin.capacity']
    exts.db = DatabaseContainer()
    dbdir = config['database.path']
    for name in config['database.names']:
        dbpath = os.path.join(dbdir, name + '.sqlite')
        conn = Connection(dbpath,
                          funcs=[ilike, ulower, IsCandidate(bin_limit)])
        exts.db.append(name, Database(conn, debug=exts.debug))


def post_stop():
    def do_stop():
        logging.info('Closing database connections')
        for name, db in exts.db:
            db.close()
    return do_stop
