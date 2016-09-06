#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate dummy data for testing purposes


'content' table::

    id varchar primary_key unique,
    created timestamp,      -- creation timestamp
    updated timestamp,      -- update timestamp
    email varchar,          -- creator email
    username varchar,       -- creator username
    ipaddr varchar,         -- creator IP address
    path varchar,           -- file path relative to upload root
    size integer,           -- file size in bytes
    bin varchar,            -- bin ID
    votes integer,          -- number of votes
    category varchar        -- category name

'votes' table::

    id integer primary_key,
    created timestamp,          -- time when vote was cast
    username text,              -- voter's username
    ipaddr text,                -- voter's IP address
    value integer,              -- vote value (usually +1, 0, or -1)
    content_id text,            -- content
    constraint uidcid unique (username, content_id) on conflict replace

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
USERCHARS = ('abcdefghijklmnopqrstuvwxyz')
FILENAME_LENGTH_RANGE = (4, 20)  # chars
USERNAME_LENGTH_RANGE = (4, 10)  # chars
FILE_SIZE_RANGE = (40, 100)  # KB
AGE_RANGE = (0, 3)  # days
VOTE_RANGE = (0, 10)  # votes per content


def dummy_string(chsource, length_range):
    chars = ''
    length = random.randint(*length_range)
    for _ in range(length):
        chars += random.choice(chsource)
    return chars


def dummy_filename():
    return dummy_string(FILECHARS, FILENAME_LENGTH_RANGE)


def dummy_username():
    return dummy_string(USERCHARS, USERNAME_LENGTH_RANGE)


def dummy_size():
    return random.randint(*FILE_SIZE_RANGE) * 1024


def dummy_ts():
    return utcnow() - timedelta(
        random.randint(*AGE_RANGE),
        random.randint(0, 24))


def dummy_votes(content_id, dummy_users):
    count = random.randint(*VOTE_RANGE)
    for _ in range(count):
        yield {
            'content_id': content_id,
            'username': random.choice(dummy_users),
            'ipaddr': '127.0.0.1',
            'value': random.choice([-1, 0, 1]),
            'created': dummy_ts(),
        }


def dummy_files(dummy_users, count=200):
    for i in range(count):
        fileid = uuid.uuid4().hex
        ts = dummy_ts()
        yield {
            'id': uuid.uuid4().hex,
            'created': ts,
            'updated': ts,
            'username': 'dummy',
            'email': 'dummy@example.com',
            'ipaddr': '127.0.0.1',
            'path': dummy_filename(),
            'size': dummy_size(),
            'votes': dummy_votes(fileid, dummy_users),
        }


def main():
    main_cn = Connection('tmp/main.sqlite')
    main = Database(main_cn)
    dummy_users = [dummy_username() for _ in range(50)]
    start = time.time()
    with main.transaction() as cur:
        for data in dummy_files(dummy_users):
            votes = data.pop('votes')
            vote_count = 0
            for v in votes:
                q = main.Insert('votes', cols=v.keys())
                cur.query(q, **v)
                vote_count += v['value']
            data['votes'] = vote_count
            q = main.Insert('content', cols=data.keys())
            cur.query(q, **data)
    end = time.time()
    print('Total time took: {}'.format(end - start))


if __name__ == '__main__':
    sys.exit(main())
