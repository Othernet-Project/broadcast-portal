"""
broadcast.py: Manage content entries

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import datetime
import decimal
import functools
import hmac
import hashlib
import math
import os
import uuid
import urlparse

import stripe

from bottle import request, redirect, abort
from bottle_utils.form import ValidationError
from bottle_utils.i18n import dummy_gettext as _

from .gdrive import DriveClient
from .gsheet import SheetClient
from .sendmail import send_mail


def get_unique_id():
    return uuid.uuid4().hex


def sign(data, secret_key):
    return hmac.new(secret_key, data, hashlib.sha256).hexdigest()


def row_to_dict(row):
    if not row:
        return row

    return dict((key, row[key]) for key in row.keys())


def get_item(table, db=None, raw=False, **kwargs):
    db = db or request.db.main
    query = db.Select(sets=table)
    for name, value in kwargs.items():
        op = 'IS' if value is None else '='
        query.where += '{0} {1} :{0}'.format(name, op)

    db.query(query, **kwargs)
    row = row_to_dict(db.result)

    if not raw and row is not None:
        (wrapper_cls,) = [cls for cls in (ContentItem, TwitterItem)
                          if cls.type == table]
        return wrapper_cls(db=db, **row)

    # no wrapper specified
    return row


def filter_items(table, db=None, raw=False, **kwargs):
    db = db or request.db.main
    query = db.Select(sets=table, order=['date(created)'])
    for name, value in kwargs.items():
        op = 'IS' if value is None else '='
        query.where += '{0} {1} :{0}'.format(name, op)

    db.query(query, **kwargs)
    rows = map(row_to_dict, db.results)

    if not raw and rows:
        (wrapper_cls,) = [cls for cls in (ContentItem, TwitterItem)
                          if cls.type == table]
        return [wrapper_cls(db=db, **row) for row in rows]

    # no wrapper specified
    return rows


def cleanup(table, db=None, config=None):
    db = db or request.db.main
    config = config or request.app.config
    days = config['{0}.remove_orphans_after'.format(table)]
    where = "email IS NULL AND created < date('now', '-{0} days')".format(days)
    query = db.Delete(table, where=where)
    db.query(query)


def humanize_amount(cent_amount, config):
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


def upload_to_drive(item, config):
    dc = DriveClient(config['google.service_credentials_path'])
    upload_root = config['{}.upload_root'.format(item.type)]
    upload_path = os.path.join(upload_root, item.file_path)
    file_data = dc.upload(upload_path,
                          parent_id=config.get('google.parent_folder_id'))
    sc = SheetClient(config['google.service_credentials_path'])
    sc.insert(config['google.spreadsheet_id'],
              config['google.worksheet_index'],
              item.values() + [file_data['alternateLink'], file_data['id']])


class ChargeError(ValidationError):
    pass


class BaseItem(object):
    PROCESSING = 'PROCESSING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'

    def __init__(self, db=None, **kwargs):
        self.db = db or request.db.main
        self._data = kwargs

    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError:
            cls_name = self.__class__.__name__
            msg = "'{0}' object has no attribute '{1}'".format(cls_name, name)
            raise AttributeError(msg)

    def __getitem__(self, name):
        return self._data[name]

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def validate(self, data):
        valid_statuses = (self.PROCESSING, self.ACCEPTED, self.REJECTED)
        if 'status' in data and data['status'] not in valid_statuses:
            msg = ("Value of `status` can only be one of the following: "
                   "{0}".format(valid_statuses))
            raise ValueError(msg)

    def update(self, **kwargs):
        self.validate(kwargs)
        self._data.update(kwargs)
        self.save()

    def save(self):
        query = self.db.Replace(self.type, cols=self._data.keys())
        self.db.execute(query, self._data)

    def save_charge_id(self, obj):
        query = self.db.Update(self.type,
                               charge_id=':charge_id',
                               where='id = :id')
        self.db.query(query, id=self.id, charge_id=obj.id)
        self.update(charge_id=obj.id)

    def save_charge_object(self, charge_obj):
        # create charge object
        query = self.db.Insert('charges', cols=('id', 'charged_at'))
        charge_data = dict(id=charge_obj.id, charged_at=charge_obj.created)
        self.db.execute(query, charge_data)
        # store charge object id on content table
        self.save_charge_id(charge_obj)

    def calculate_price(self):
        raise NotImplementedError()

    @property
    def priority_price(self):
        return humanize_amount(self.calculate_price(),
                               config=request.app.config)

    @property
    def has_free_mode(self):
        return request.app.config['{0}.allow_free'.format(self.type)]

    def _charge(self, token, description):
        stripe.api_key = request.app.config['stripe.secret_key']
        currency = request.app.config['charge.currency']
        price = self.calculate_price()
        try:
            charge_obj = stripe.Charge.create(amount=price,
                                              currency=currency,
                                              source=token,
                                              capture=False,
                                              description=description)
        except stripe.error.CardError as exc:
            raise ChargeError(exc.message, {}, is_form=True)
        except Exception:
            message = _("Payment processing failed.")
            raise ChargeError(message, {}, is_form=True)
        else:
            self.save_charge_object(charge_obj)
            return charge_obj

    def _subscribe(self, token, plan):
        stripe.api_key = request.app.config['stripe.secret_key']
        try:
            subscription_obj = stripe.Customer.create(source=token,
                                                      plan=plan,
                                                      email=self.email)
        except Exception:
            message = _("Subscription to the chosen plan failed.")
            raise ChargeError(message, {}, is_form=True)
        else:
            self.save_charge_id(subscription_obj)
            return subscription_obj


class BaseUploadItem(BaseItem):
    modifieable_fields = ('status',)

    def __init__(self, id, content_file=None, upload_root=None, **kwargs):
        self.content_file = content_file
        if self.content_file:
            conf = request.app.config
            upload_root = upload_root or conf[self.ckey('upload_root')]
            file_path = os.path.join(id, self.content_file.filename)
            self.upload_path = os.path.join(upload_root, file_path)
            super(BaseUploadItem, self).__init__(id=id,
                                                 file_path=file_path,
                                                 **kwargs)
        else:
            super(BaseUploadItem, self).__init__(id=id, **kwargs)

    def ckey(self, name):
        return '{0}.{1}'.format(self.type, name)

    def content(self):
        path, filename = self.file_path.split('/', 1)
        return filename

    @property
    def internal_url(self):
        url_template = request.app.config[self.ckey('url_template')]
        base_url = url_template.format(self._data['name'])
        return urlparse.urljoin(base_url, self._data['url'])

    @property
    def unit_price(self):
        return humanize_amount(request.app.config[self.ckey('review_price')],
                               request.app.config)

    def save(self):
        if self.content_file:
            # make sure folder with id exists
            upload_dir = os.path.dirname(self.upload_path)
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            if os.path.exists(self.upload_path):
                # remove file if already exists
                os.remove(self.upload_path)

            self.content_file.save(self.upload_path)

        super(BaseUploadItem, self).save()

    def calculate_price(self):
        return request.app.config[self.ckey('review_price')]

    def calculate_chargeable_size(self):
        return int(math.ceil(float(self.file_size) / 1024 / 1024))

    def charge(self, token):
        human_size = '{0} MB'.format(self.calculate_chargeable_size())
        description = request.app.config[self.ckey('description_template')]
        description = description.format(human_size)
        return self._charge(token, description)


class ContentItem(BaseUploadItem):
    type = 'content'


class TwitterItem(BaseItem):
    type = 'twitter'
    modifieable_fields = ('status',)

    PLAN_PERIODS = {
        'bc_twitter_monthly': _('every month'),
        'bc_twitter_annual': _('every year'),
    }

    def content(self):
        return self.handle

    def calculate_price(self):
        for plan in request.app.config['twitter.prices']:
            name, amt = plan.split(':')
            if name == self.plan:
                return int(amt)
        raise KeyError('No plan found for {}'.format(self.plan))

    def charge(self, token):
        if self.plan in request.app.config['twitter.subscription_plans']:
            return self._subscribe(token, self.plan)
        else:
            description = request.app.config['twitter.description_template']
            description = description.format(self.plan)
            return self._charge(token, description)

    @property
    def plan_period(self):
        return self.PLAN_PERIODS[self.plan]

    @property
    def plan_price(self):
        return humanize_amount(self.calculate_price(),
                               request.app.config)


def fetch_item(func):
    @functools.wraps(func)
    def wrapper(**kwargs):
        item_type = kwargs.pop('item_type', None)
        item_id = kwargs.pop('item_id', None)
        if not item_type or not item_id:
            abort(404, _("The specified item was not found."))

        item = get_item(item_type, id=item_id)
        if not item:
            abort(404, _("The specified item was not found."))

        return func(item=item, **kwargs)
    return wrapper


def guard_already_charged(func):
    @functools.wraps(func)
    def wrapper(item, **kwargs):
        if item.charge_id:
            scheduled_url = request.app.get_url('broadcast_priority_scheduled',
                                                item_type=item.type,
                                                item_id=item.id)
            redirect(scheduled_url)

        return func(item=item, **kwargs)
    return wrapper
