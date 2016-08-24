#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate dummy data for testing purposes


'content' table::

    id varchar primary_key unique,
    created timestamp,      -- creation timestamp
    email varchar,          -- creator email
    username varchar,       -- creator username
    ipaddr varchar,         -- creator IP address
    path varchar,           -- file path relative to upload root
    size integer,           -- file size in bytes
    bin varchar,            -- bin ID
    votes integer,          -- number of votes
    category varchar        -- category name

Migrations are not run, so you'll need to start the app once.
"""

from __future__ import unicode_literals

import sys
import time
import uuid
import random
from datetime import timedelta

from squery_lite.squery import Database, Connection
from broadcast.util.helpers import utcnow


FILECHARS = ('abcdefghijklmnopqrstuvwxyz'
             'あいうえおかきくけこさしすせそ'
             'абвгдђежѕијклљмнопрстћуфхцчџш'
             '0123456789'
             '-_*()')
VOTE_SELECTION = [-2, -2, -1, -1, -1, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 5]
FILENAME_LENGTH_RANGE = (4, 20)  # chars
FILE_SIZE_RANGE = (4, 2048)  # KB
AGE_RANGE = (0, 3)  # days


def dummy_filename():
    chars = ''
    length = random.randint(*FILENAME_LENGTH_RANGE)
    for _ in range(length):
        chars += random.choice(FILECHARS)
    return chars


def dummy_size():
    return random.randint(*FILE_SIZE_RANGE)


def dummy_ts():
    return utcnow() - timedelta(
        random.randint(*AGE_RANGE),
        random.randint(0, 24))


def dummy_votes():
    return random.choice(VOTE_SELECTION)


def dummy_files(count=200):
    for i in range(count):
        yield {
            'id': uuid.uuid4().hex,
            'created': dummy_ts(),
            'username': 'dummy',
            'email': 'dummy@example.com',
            'ipaddr': '127.0.0.1',
            'path': dummy_filename(),
            'size': dummy_size(),
            'votes': dummy_votes(),
        }


def main():
    main_cn = Connection('tmp/main.sqlite')
    main = Database(main_cn)
    start = time.time()
    with main.transaction() as cur:
        for data in dummy_files():
            q = main.Insert('content', cols=data.keys())
            cur.query(q, **data)
    end = time.time()
    print('Total time took: {}'.format(end - start))


if __name__ == '__main__':
    sys.exit(main())
