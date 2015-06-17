"""
broadcast.py: Manage content entries

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import datetime
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


def humanize_amount(cent_amount):
    currency = request.app.config['content.currency']
    multiplier = request.app.config['content.basic_monetary_unit_multiplier']
    basic_unit = decimal.Decimal(cent_amount) / multiplier
    return "{0:,.2f} {1}".format(basic_unit, currency)


def get_item(table, **kwargs):
    db = request.db.main
    query = db.Select(sets=table)
    for name in kwargs:
        query.where += '{0} = :{0}'.format(name)

    db.query(query, **kwargs)
    row = db.result

    if row is not None:
        for wrapper_cls in DBResultWrapper.__subclasses__():
            if wrapper_cls.type == table:
                return wrapper_cls(**dict((key, row[key])
                                   for key in row.keys()))

    # no wrapper specified
    return row


class ChargeError(ValidationError):
    pass


class DBResultWrapper(object):

    def __init__(self, db=None, **kwargs):
        self.db = db or request.db.main
        self.data = kwargs

    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError:
            return super(DBResultWrapper, self).__getattr__(name)

    def save(self):
        query = self.db.Insert(self.type, cols=self.data.keys())
        self.db.execute(query, self.data)

    def save_charge_info(self, charge_obj):
        query = self.db.Update(self.type,
                               charge_id=':charge_id',
                               charged_at=':charged_at',
                               where='id = :id')
        self.db.query(query,
                      id=self.id,
                      charge_id=charge_obj.id,
                      charged_at=datetime.datetime.utcnow())


class ContentItem(DBResultWrapper):
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

    @staticmethod
    def calculate_chargable_size(content_size):
        return int(math.ceil(float(content_size) / 1024 / 1024))

    @classmethod
    def calculate_price(cls, content_size):
        content_size_in_mb = cls.calculate_chargable_size(content_size)
        price_per_mb_cents = request.app.config['content.price_per_mb']
        return content_size_in_mb * price_per_mb_cents

    @property
    def priority_price(self):
        return humanize_amount(self.calculate_price(self.data['file_size']))

    def charge(self, token):
        stripe.api_key = request.app.config['stripe.secret_key']
        currency = request.app.config['content.currency']
        charged_size = self.calculate_chargable_size(self.data['file_size'])
        price = self.calculate_price(self.data['file_size'])
        description = request.app.config['content.description_template']
        human_size = '{0} MB'.format(charged_size)
        description = description.format(human_size)
        try:
            charge_obj = stripe.Charge.create(amount=price,
                                              currency=currency,
                                              source=token,
                                              capture=False,
                                              description=description)
        except stripe.error.CardError as exc:
            raise ChargeError(exc.message, {}, is_form=True)
        except Exception as exc:
            print(exc)
            message = _("Payment processing failed.")
            raise ChargeError(message, {}, is_form=True)
        else:
            self.save_charge_info(charge_obj)


class TwitterItem(DBResultWrapper):
    type = 'twitter'

    @property
    def priority_price(self):
        raise NotImplementedError()

    def charge(self, token):
        raise NotImplementedError()
