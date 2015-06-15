"""
priority.py: Handle priority broadcasts

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from bottle import request, redirect
from bottle_utils.csrf import csrf_protect, csrf_token

from ..forms.priority import PaymentForm
from ..util.template import view


@view('free')
def show_broadcast_free_form():
    priority_price = ''
    return dict(mode='free', priority_price=priority_price)


@view('priority')
@csrf_token
def show_broadcast_priority_form():
    priority_price = ''
    stripe_public_key = request.app.config['stripe.public_key']
    form = PaymentForm({'stripe_public_key': stripe_public_key})
    return dict(mode='priority',
                priority_price=priority_price,
                form=form)


@view('priority')
@csrf_protect
def broadcast_priority():
    priority_price = ''
    form = PaymentForm(request.forms)

    if form.is_valid():
        # charge here
        pass

    return dict(mode='priority',
                priority_price=priority_price,
                form=form)


def route(conf):
    return (
        (
            '/broadcast/free/',
            'GET',
            show_broadcast_free_form,
            'broadcast_free_form',
            {}
        ), (
            '/broadcast/priority/',
            'GET',
            show_broadcast_priority_form,
            'broadcast_priority_form',
            {}
        ), (
            '/broadcast/priority/',
            'POST',
            broadcast_priority,
            'broadcast_priority',
            {}
        ),
    )
