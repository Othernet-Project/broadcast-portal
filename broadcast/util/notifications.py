"""
notifications.py: Send out notifications of newly submitted content to admins

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import datetime

from bottle_utils.i18n import dummy_gettext as _

from .broadcast import filter_items
from .email import send_multiple
from .squery import Database


def is_sending_time(send_at):
    return True


def get_new_broadcast_entries(db):
    return dict(content=filter_items('content', notified=None, db=db),
                twitter=filter_items('twitter', notified=None, db=db))


def mark_notified(broadcast_entries, db):
    notified = datetime.datetime.now()
    for entry_type, entries in broadcast_entries.items():
        entry_ids = [entry.id for entry in entries]
        query = db.Update(entry_type,
                          notified='?',
                          where=db.sqlin.__func__('id', entry_ids))
        args = [notified] + entry_ids
        db.query(query, *args)


def send_notifications(app):
    if not is_sending_time(app.config['notifications.send_at']):
        return

    debug = app.config['server.debug']
    db_conn = app.config['database.connections']['main']
    db = Database(db_conn, debug=debug)
    broadcast_entries = get_new_broadcast_entries(db)
    recipients = app.config['notifications.recipients']
    send_multiple([(email, email) for email in recipients],
                  _("Notification"),
                  text='email/notification',
                  data=dict(**broadcast_entries),
                  config=app.config)
    mark_notified(broadcast_entries, db)
