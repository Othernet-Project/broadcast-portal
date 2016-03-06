import datetime
import decimal
import functools
import os

from bottle import request, redirect, abort
from bottle_utils.i18n import dummy_gettext as _

from .models.charges import Charge
from .models.items import BaseItem
from .util.gdrive import DriveClient
from .util.gsheet import SheetClient
from .util.sendmail import send_mail
from .util.template_helper import template_helper


def fetch_item(func):
    @functools.wraps(func)
    def wrapper(**kwargs):
        item_type = kwargs.pop('item_type', None)
        item_id = kwargs.pop('item_id', None)
        if not item_type or not item_id:
            abort(404, _("The specified item was not found."))

        try:
            item_cls = BaseItem.cast(item_type)
        except TypeError:
            item = None
        else:
            item = item_cls.get(id=item_id)

        if not item:
            abort(404, _("The specified item was not found."))

        return func(item=item, **kwargs)
    return wrapper


def fetch_charge(func):
    @functools.wraps(func)
    def wrapper(item, **kwargs):
        try:
            charge = Charge.get(item_id=item.id)
        except Charge.DoesNotExist:
            abort(400, _("Cannot determine the requested plan."))
        else:
            if charge.is_executed:
                url = request.app.get_url('broadcast_priority_scheduled',
                                          item_type=item.type,
                                          item_id=item.id)
                redirect(url)
            return func(item=item, charge=charge, **kwargs)
    return wrapper


def cleanup(table, db=None, config=None):
    db = db or request.db.main
    config = config or request.app.config
    days = config['{0}.remove_orphans_after'.format(table)]
    where = "email IS NULL AND created < date('now', '-{0} days')".format(days)
    query = db.Delete(table, where=where)
    db.query(query)


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


def humanize_amount(cent_amount, config=None):
    config = config or request.app.config
    currency = config['charge.currency']
    multiplier = config['charge.basic_monetary_unit_multiplier']
    basic_unit = decimal.Decimal(cent_amount) / multiplier
    return "{} {:,.2f}".format(currency, basic_unit)


def send_payment_confirmation(item, stripe_obj, email, config):
    interval_types = {
        'month': _("monthly"),
        'year': _("annual")
    }
    item_types = {
        'twitter': _("twitter feed"),
        'content': _("content"),
    }
    is_subscription = stripe_obj.object == 'customer'
    if is_subscription:
        card = stripe_obj.sources.data[-1]
        last4digits = card.last4
        subscription = stripe_obj.subscriptions.data[-1]
        interval = interval_types[subscription.plan.interval]
        timestamp = subscription.start
        amount = subscription.plan.amount
    else:
        last4digits = stripe_obj.source.last4
        interval = None
        timestamp = stripe_obj.created
        amount = stripe_obj.amount

    context_data = {'email': email,
                    'item_type': item_types[item.type],
                    'last4digits': last4digits,
                    'timestamp': datetime.datetime.fromtimestamp(timestamp),
                    'total_amount': humanize_amount(amount, config=config),
                    'interval': interval,
                    'is_subscription': is_subscription}
    send_mail(email,
              _("Payment Confirmation"),
              text='email/payment_confirmation',
              data=context_data,
              config=config)


@template_helper
def plan_period(charge):
    periods = {
        'bc_twitter_monthly': _('every month'),
        'bc_twitter_annual': _('every year'),
    }
    return periods[charge.plan]

