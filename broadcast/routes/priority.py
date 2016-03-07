"""
priority.py: Handle priority broadcasts

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from bottle import request, redirect
from bottle_utils.csrf import csrf_protect, csrf_token
from bottle_utils.i18n import dummy_gettext as _

from ..forms.priority import PaymentForm
from ..helpers import fetch_item, fetch_charge, upload_to_drive
from ..models.charges import Charge
from ..util.sendmail import send_mail
from ..util.template import view


@view('priority')
@csrf_token
@fetch_item
@fetch_charge()
def show_broadcast_priority_form(item, charge):
    stripe_public_key = request.app.config['stripe.public_key']
    form = PaymentForm({'stripe_public_key': stripe_public_key,
                        'email': item.email})
    return dict(mode='priority', item=item, charge=charge, form=form)


@view('priority')
@csrf_protect
@fetch_item
@fetch_charge()
def broadcast_priority(item, charge):
    form = PaymentForm(request.forms)
    error = None
    if form.is_valid():
        token = form.processed_data['stripe_token']
        if not item.email:
            item.update(email=form.processed_data['email'])
        try:
            stripe_object = charge.execute(token, item=item)
        except Charge.Error as exc:
            error = exc
        else:
            if item.type == 'content':
                tasks = request.app.config['tasks']
                tasks.schedule(upload_to_drive,
                               args=(item, request.app.config))
            send_mail(item.email,
                      _("Payment Confirmation"),
                      text='email/payment_confirmation',
                      data=dict(item=item, stripe_object=stripe_object),
                      is_async=True,
                      config=request.app.config)
            scheduled_url = request.app.get_url('broadcast_priority_scheduled',
                                                item_type=item.type,
                                                item_id=item.id)
            redirect(scheduled_url)

    return dict(mode='priority',
                item=item,
                charge=charge,
                charge_error=error,
                form=form)


@view('feedback')
@fetch_item
@fetch_charge(guard_already_charged=False)
def show_broadcast_priority_scheduled(item, charge):
    if charge.is_executed:
        # attempted access to success-page, while not charged
        priority_url = request.app.get_url('broadcast_priority_form',
                                           item_type=item.type,
                                           item_id=item.id)
        redirect(priority_url)

    return dict(item=item,
                status='success',
                page_title=_('Thank You'),
                message=_('Your payment has been completed. You will receive'
                          ' an email with your receipt shortly.'))


def route(conf):
    types = '|'.join(conf['app.broadcast_types'])
    pre = '/broadcast/<item_type:re:%s>/<item_id:re:[0-9a-f]{32}>' % types
    return (
        (
            '{0}/priority/'.format(pre),
            'GET',
            show_broadcast_priority_form,
            'broadcast_priority_form',
            {}
        ), (
            '{0}/priority/'.format(pre),
            'POST',
            broadcast_priority,
            'broadcast_priority',
            {}
        ), (
            '{0}/scheduled/'.format(pre),
            'GET',
            show_broadcast_priority_scheduled,
            'broadcast_priority_scheduled',
            {}
        ),
    )

