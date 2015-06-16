"""
priority.py: Handle priority broadcasts

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from functools import wraps

from bottle import request, redirect, abort
from bottle_utils.csrf import csrf_protect, csrf_token
from bottle_utils.i18n import lazy_gettext as _

from ..forms.priority import PaymentForm
from ..util.auth import login_required
from ..util.broadcast import get_content_by
from ..util.priority import (ChargeError,
                             calculate_price,
                             charge,
                             humanize_amount)
from ..util.template import view


def content_owner_or_404(func):
    @wraps(func)
    def wrapper(**kwargs):
        content_id = kwargs.pop('content_id', None)
        if not content_id:
            abort(404, _("The specified content was not found."))

        content = get_content_by(content_id=content_id)
        if not content:
            abort(404, _("The specified content was not found."))

        if content.email != request.user.email:
            abort(404, _("The specified content was not found."))

        return func(content=content, **kwargs)
    return wrapper


@login_required()
@view('free')
@content_owner_or_404
def show_broadcast_free_form(content):
    priority_price = humanize_amount(calculate_price(content.file_size))
    return dict(mode='free', priority_price=priority_price, content=content)


@login_required()
@view('priority')
@csrf_token
@content_owner_or_404
def show_broadcast_priority_form(content):
    priority_price = humanize_amount(calculate_price(content.file_size))
    stripe_public_key = request.app.config['stripe.public_key']
    form = PaymentForm({'stripe_public_key': stripe_public_key})
    return dict(mode='priority',
                priority_price=priority_price,
                content=content,
                form=form)


@login_required()
@view('priority')
@csrf_protect
@content_owner_or_404
def broadcast_priority(content):
    priority_price = humanize_amount(calculate_price(content.file_size))
    form = PaymentForm(request.forms)

    if form.is_valid():
        token = form.processed_data['stripe_token']
        try:
            charge(content, token)
        except ChargeError as exc:
            form.error = exc
        else:
            success_url = request.app.get_url('broadcast_accepted',
                                              content_id=content.content_id)
            redirect(success_url)

    return dict(mode='priority',
                priority_price=priority_price,
                content=content,
                form=form)


def route(conf):
    return (
        (
            '/broadcast/<content_id:re:[0-9a-f]{32}>/free/',
            'GET',
            show_broadcast_free_form,
            'broadcast_free_form',
            {}
        ), (
            '/broadcast/<content_id:re:[0-9a-f]{32}>/priority/',
            'GET',
            show_broadcast_priority_form,
            'broadcast_priority_form',
            {}
        ), (
            '/broadcast/<content_id:re:[0-9a-f]{32}>/priority/',
            'POST',
            broadcast_priority,
            'broadcast_priority',
            {}
        ),
    )
