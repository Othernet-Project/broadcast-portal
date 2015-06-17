"""
broadcast.py: Manage content entries

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import decimal
import hmac
import hashlib
import math
import os
import uuid

import stripe

from bottle import request
from bottle_utils.form import ValidationError
from bottle_utils.i18n import lazy_gettext as _


def get_unique_id():
    return uuid.uuid4().hex


def sign(data, secret_key):
    return hmac.new(secret_key, data, hashlib.sha256).hexdigest()


def get_item(table, **kwargs):
    db = request.db.main
    query = db.Select(sets=table)
    for name in kwargs:
        query.where += '{0} = :{0}'.format(name)

    db.query(query, **kwargs)
    row = db.result

    if row is not None:
        for wrapper_cls in BaseItem.__subclasses__():
            if wrapper_cls.type == table:
                return wrapper_cls(**dict((key, row[key])
                                   for key in row.keys()))

    # no wrapper specified
    return row


class ChargeError(ValidationError):
    pass


class BaseItem(object):

    def __init__(self, db=None, **kwargs):
        self.db = db or request.db.main
        self.data = kwargs

    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError:
            cls_name = self.__class__.__name__
            msg = "'{0}' object has no attribute '{1}'".format(cls_name, name)
            raise AttributeError(msg)

    def save(self):
        query = self.db.Insert(self.type, cols=self.data.keys())
        self.db.execute(query, self.data)

    def save_charge_id(self, obj):
        query = self.db.Update(self.type,
                               charge_id=':charge_id',
                               where='id = :id')
        self.db.query(query, id=self.id, charge_id=obj.id)

    def save_charge_object(self, charge_obj):
        # create charge object
        query = self.db.Insert('charges', cols=('id', 'charged_at'))
        charge_data = dict(id=charge_obj.id, charged_at=charge_obj.created)
        self.db.execute(query, charge_data)
        # store charge object id on content table
        self.save_charge_id(charge_obj)

    def humanize_amount(self, cent_amount):
        conf = request.app.config
        currency = conf['charge.currency']
        multiplier = conf['charge.basic_monetary_unit_multiplier']
        basic_unit = decimal.Decimal(cent_amount) / multiplier
        return "{0:,.2f} {1}".format(basic_unit, currency)

    def calculate_price(self):
        raise NotImplementedError()

    @property
    def priority_price(self):
        return self.humanize_amount(self.calculate_price())

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

    def _subscribe(self, token, plan):
        stripe.api_key = request.app.config['stripe.secret_key']
        try:
            subscription_obj = stripe.Customer.create(source=token,
                                                      plan=plan,
                                                      email=self.email)
        except Exception:
            message = _("Subscription to the chosen failed.")
            raise ChargeError(message, {}, is_form=True)
        else:
            self.save_charge_id(subscription_obj)


class ContentItem(BaseItem):
    type = 'content'

    def __init__(self, id, content_file=None, upload_root=None, **kwargs):
        self.content_file = content_file
        if self.content_file:
            conf = request.app.config
            upload_root = upload_root or conf['content.upload_root']
            file_path = os.path.join(id, self.content_file.filename)
            self.upload_path = os.path.join(upload_root, file_path)
            super(ContentItem, self).__init__(id=id,
                                              file_path=file_path,
                                              **kwargs)
        else:
            super(ContentItem, self).__init__(id=id, **kwargs)

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

        super(ContentItem, self).save()

    def calculate_chargeable_size(self):
        return int(math.ceil(float(self.file_size) / 1024 / 1024))

    def calculate_price(self):
        chargeable_size = self.calculate_chargeable_size()
        price_per_mb_cents = request.app.config['content.price_per_mb']
        return chargeable_size * price_per_mb_cents

    def charge(self, token):
        human_size = '{0} MB'.format(self.calculate_chargeable_size())
        description = request.app.config['content.description_template']
        description = description.format(human_size)
        self._charge(token, description)


class TwitterItem(BaseItem):
    type = 'twitter'

    def calculate_price(self):
        return request.app.config['twitter.price_{0}'.format(self.plan)]

    def charge(self, token):
        if self.plan in request.app.config['twitter.subscription_plans']:
            self._subscribe(token, self.plan)
        else:
            description = request.app.config['twitter.description_template']
            description = description.format(self.plan)
            self._charge(token, description)
