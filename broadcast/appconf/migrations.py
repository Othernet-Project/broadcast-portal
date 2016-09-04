"""
migrations.py: functions for managing migrations

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import logging

from squery_lite.migrations import migrate

from ..app.exts import container as exts


def pre_init():
    logging.info('Running database migrations')
    pkg = exts.config['database.migrations_package']
    for name, db in exts.db:
        migrate(db, pkg + '.' + name, exts.config)
