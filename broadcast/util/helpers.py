from __future__ import division

import os
import time
import decimal
import datetime

import pytz
from bottle import request
from bottle_utils.i18n import (
    dummy_gettext as _,
    dummy_ngettext as ngettext,
)

from ..app.exts import container as exts
from .gdrive import DriveClient
from .gsheet import SheetClient
from .template_helper import template_helper


def cleanup(table, db=None, config=None):
    db = exts.db.main
    config = config or request.app.config
    days = config['{0}.remove_orphans_after'.format(table)]
    where = "email IS NULL AND created < date('now', '-{0} days')".format(days)
    query = db.Delete(table, where=where)
    db.query(query)


def utcnow():
    return datetime.datetime.now(tz=pytz.utc)


def tomorrow():
    today = utcnow().date()
    return today + datetime.timedelta(1)


def to_timestamp(d):
    return int(time.mktime(d.timetuple()))


def upload_to_drive(item, config):
    if not config['google.enabled']:
        return
    dc = DriveClient(config['google.service_credentials_path'])
    upload_root = config['{}.upload_root'.format(item.type)]
    upload_path = os.path.join(upload_root, item.file_path)
    file_data = dc.upload(upload_path,
                          parent_id=config.get('google.parent_folder_id'))
    sc = SheetClient(config['google.service_credentials_path'])
    sc.insert(config['google.spreadsheet_id'],
              config['google.worksheet_index'],
              item.values() + [file_data['alternateLink'], file_data['id']])


@template_helper
def hamount(cent_amount, config=None):
    config = config or request.app.config
    currency = config['charge.currency']
    multiplier = config['charge.basic_monetary_unit_multiplier']
    basic_unit = decimal.Decimal(cent_amount) / multiplier
    return "{} {:,.2f}".format(currency, basic_unit)


@template_helper
def human_time(dt):
    diff = utcnow() - dt

    n = round(diff.days / 365)
    if n >= 1:
        return ngettext('{n} year ago', '{n} years ago', n).format(n=int(n))

    n = round(diff.days / 365)
    if n >= 1:
        return ngettext('{n} month ago', '{n} months ago', n).format(n=int(n))

    n = round(diff.days / 7)
    if n >= 1:
        return ngettext('{n} week ago', '{n} weeks ago', n).format(n=int(n))

    n = diff.days
    if n >= 1:
        return ngettext('{n} day ago', '{n} days ago', n).format(n=int(n))

    n = round(diff.seconds / 3600)
    if n >= 1:
        return ngettext('{n} hour ago', '{n} hours ago', n).format(n=int(n))

    n = round(diff.seconds / 60)
    if n >= 5:
        return ngettext('{n} minute ago', '{n} minutes ago', n).format(
            n=int(n))

    return _('just now')


@template_helper
def plan_period(charge):
    periods = {
        'bc_twitter_monthly': _('every month'),
        'bc_twitter_annual': _('every year'),
    }
    return periods[charge.plan]


@template_helper
def plan_price(item, charge):
    config = request.app.config
    price_map = config['{}.prices'.format(item.type)]
    return charge._match_price(price_map)


@template_helper
def from_ts(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


@template_helper
def protect_email(value, delimiter='@'):
    """
    Return the first portion of a passed in string delimited on the first
    occurrence of `delimiter`.
    """
    return ''.join(value.split(delimiter)[0])
