"""
priority.py: Priority content charging utilities

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import datetime
import decimal
import math

import stripe

from bottle import request
from bottle_utils.form import ValidationError
from bottle_utils.i18n import lazy_gettext as _


class ChargeError(ValidationError):
    pass


def calculate_chargable_size(content_size):
    return int(math.ceil(float(content_size) / 1024 / 1024))


def calculate_price(content_size):
    content_size_in_mb = calculate_chargable_size(content_size)
    price_per_mb_cents = request.app.config['content.price_per_mb']
    return content_size_in_mb * price_per_mb_cents


def humanize_amount(cent_amount):
    currency = request.app.config['content.currency']
    multiplier = request.app.config['content.basic_monetary_unit_multiplier']
    basic_unit = decimal.Decimal(cent_amount) / multiplier
    return "{0:,.2f} {1}".format(basic_unit, currency)


def save_charge_info(content_id, charge_id, db=None):
    db = db or request.db.main
    query = db.Update('content',
                      charge_id=':charge_id',
                      charged_at=':charged_at',
                      where='content_id = :content_id')
    db.query(query,
             charge_id=charge_id,
             charged_at=datetime.datetime.utcnow(),
             content_id=content_id)


def charge(content, token):
    stripe.api_key = request.app.config['stripe.secret_key']
    currency = request.app.config['content.currency']
    charged_size = calculate_chargable_size(content.file_size)
    price = calculate_price(content.file_size)
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
        save_charge_info(content.content_id, charge_obj.id)
