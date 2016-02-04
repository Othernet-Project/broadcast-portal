"""
notifications.py: Send out notifications of newly submitted content to admins

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import datetime

from bottle_utils.i18n import dummy_gettext as _

from .broadcast import filter_items, cleanup
from .sendmail import send_multiple
from .squery import Database


def add_time(source, **kwargs):
    source_datetime = datetime.datetime.combine(datetime.date.today(), source)
    return (source_datetime + datetime.timedelta(**kwargs)).time()


def sub_time(source, **kwargs):
    source_datetime = datetime.datetime.combine(datetime.date.today(), source)
    return (source_datetime - datetime.timedelta(**kwargs)).time()


def is_sending_time(send_at):
    hour, minute = map(int, send_at.split(':'))
    send_at_time = datetime.time(hour, minute)
    start = sub_time(send_at_time, minutes=5)
    end = add_time(send_at_time, minutes=5)
    timestamp = datetime.datetime.now().time()
    return start <= timestamp <= end


def is_already_sent(db, broadcast_types):
    for item_type in broadcast_types:
        query = db.Select(sets=item_type,
                          where="notified > date('now', 'start of day')")
        db.query(query)
        if db.results:
            return True

    return False


def get_new_broadcast_entries(db, broadcast_types):
    return dict((item_type, filter_items(item_type, notified=None, db=db))
                for item_type in broadcast_types)


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
    debug = app.config['server.debug']
    db_conn = app.config['database.connections']['main']
    db = Database(db_conn, debug=debug)
    broadcast_types = app.config['app.broadcast_types']
    # check if we're within sending time range
    if not is_sending_time(app.config['notifications.send_at']):
        return
    # check if we already sent it today
    if is_already_sent(db, broadcast_types):
        return

    # remove orphans before sending notifications
    for item_type in broadcast_types:
        cleanup(item_type, db=db, config=app.config)

    broadcast_entries = get_new_broadcast_entries(db, broadcast_types)
    recipients = app.config['notifications.recipients']
    send_multiple([(email, email) for email in recipients],
                  _("Notification"),
                  text='email/notification',
                  data=dict(**broadcast_entries),
                  config=app.config)
    mark_notified(broadcast_entries, db)
