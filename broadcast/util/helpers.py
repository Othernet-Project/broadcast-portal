import os
import time
import decimal
import datetime

import pytz
from bottle import request
from bottle_utils.i18n import dummy_gettext as _

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
def hdatetime(dt):
    diff = datetime.datetime.utcnow() - dt
    periods = (
        (diff.days / 365, _("year"), _("years")),
        (diff.days / 30, _("month"), _("months")),
        (diff.days / 7, _("week"), _("weeks")),
        (diff.days, _("day"), _("days")),
        (diff.seconds / 3600, _("hour"), _("hours")),
        (diff.seconds / 60, _("minute"), _("minutes")),
        (diff.seconds, _("second"), _("seconds")),
    )
    for (period, singular, plural) in periods:
        if period:
            unit = singular if period == 1 else plural
            return _("{period} {unit} ago").format(period=period, unit=unit)

    return _("just now")


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
