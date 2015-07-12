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
from ..util.broadcast import (fetch_item,
                              guard_already_charged,
                              send_payment_confirmation,
                              ChargeError)
from ..util.template import view


@view('priority')
@csrf_token
@fetch_item
@guard_already_charged
def show_broadcast_priority_form(item):
    stripe_public_key = request.app.config['stripe.public_key']
    form = PaymentForm({'stripe_public_key': stripe_public_key,
                        'email': item.email})
    return dict(mode='priority', item=item, form=form)


@view('priority')
@csrf_protect
@fetch_item
@guard_already_charged
def broadcast_priority(item):
    form = PaymentForm(request.forms)
    error = None
    if form.is_valid():
        token = form.processed_data['stripe_token']
        item.update(email=form.processed_data['email'])
        try:
            stripe_obj = item.charge(token)
        except ChargeError as exc:
            error = exc
        else:
            if item.email:
                task_runner = request.app.config['task.runner']
                task_runner.schedule(send_payment_confirmation,
                                     item,
                                     stripe_obj,
                                     item.email,
                                     request.app.config)

            scheduled_url = request.app.get_url('broadcast_priority_scheduled',
                                                item_type=item.type,
                                                item_id=item.id)
            redirect(scheduled_url)

    return dict(mode='priority', item=item, form=form, charge_error=error)


@view('feedback')
@fetch_item
def show_broadcast_priority_scheduled(item):
    if item.charge_id is None:
        # attempted access to success-page, while not charged
        priority_url = request.app.get_url('broadcast_priority_form',
                                           item_type=item.type,
                                           item_id=item.id)
        redirect(priority_url)

    messages = {
        'content': _('Priority broadcast has been successfully scheduled.'),
        'tv': _('Priority broadcast has been successfully scheduled.'),
        'twitter': _('Twitter feed broadcast has been successfully scheduled.')
    }
    return dict(item=item,
                status='success',
                page_title=_('Broadcast Scheduled'),
                message=messages[item.type],
                redirect_url=request.app.get_url('main'),
                redirect_target=_('main page'))


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
