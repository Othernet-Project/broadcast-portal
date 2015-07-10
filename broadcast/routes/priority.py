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
from bottle_utils.i18n import dummy_gettext as _

from ..forms.priority import PaymentForm
from ..util.auth import login_required
from ..util.broadcast import get_item, send_payment_confirmation, ChargeError
from ..util.template import view


def item_owner_or_404(func):
    @wraps(func)
    def wrapper(**kwargs):
        item_type = kwargs.pop('item_type', None)
        item_id = kwargs.pop('item_id', None)
        if not item_type or not item_id:
            abort(404, _("The specified item was not found."))

        item = get_item(item_type, id=item_id)
        if not item:
            abort(404, _("The specified item was not found."))

        if not item.email:
            # if it has no owner so far, the first access to the object will
            # associate the current user as the object's owner
            item.update(email=request.user.email, name=request.user.username)

        if item.email != request.user.email:
            abort(404, _("The specified item was not found."))

        return func(item=item, **kwargs)
    return wrapper


def guard_free_mode(func):
    @wraps(func)
    def wrapper(item, **kwargs):
        if not item.has_free_mode:
            priority_url = request.app.get_url('broadcast_priority_form',
                                               item_type=item.type,
                                               item_id=item.id)
            redirect(priority_url)

        return func(item=item, **kwargs)
    return wrapper


def guard_already_charged(func):
    @wraps(func)
    def wrapper(item, **kwargs):
        if item.charge_id:
            scheduled_url = request.app.get_url('broadcast_priority_scheduled',
                                                item_type=item.type,
                                                item_id=item.id)
            redirect(scheduled_url)

        return func(item=item, **kwargs)
    return wrapper


@login_required()
@view('free')
@item_owner_or_404
@guard_already_charged
@guard_free_mode
def show_broadcast_free_form(item):
    return dict(mode='free', item=item)


@login_required()
@view('priority')
@csrf_token
@item_owner_or_404
@guard_already_charged
def show_broadcast_priority_form(item):
    stripe_public_key = request.app.config['stripe.public_key']
    form = PaymentForm({'stripe_public_key': stripe_public_key})
    return dict(mode='priority', item=item, form=form)


@login_required()
@view('priority')
@csrf_protect
@item_owner_or_404
@guard_already_charged
def broadcast_priority(item):
    form = PaymentForm(request.forms)
    error = None
    if form.is_valid():
        token = form.processed_data['stripe_token']
        try:
            stripe_obj = item.charge(token)
        except ChargeError as exc:
            error = exc
        else:
            task_runner = request.app.config['task.runner']
            task_runner.schedule(send_payment_confirmation,
                                 item,
                                 stripe_obj,
                                 request.user.username,
                                 request.user.email,
                                 request.app.config)
            scheduled_url = request.app.get_url('broadcast_priority_scheduled',
                                                item_type=item.type,
                                                item_id=item.id)
            redirect(scheduled_url)

    return dict(mode='priority', item=item, form=form, charge_error=error)


@login_required()
@view('feedback')
@item_owner_or_404
def show_broadcast_priority_scheduled(item):
    if item.charge_id is None:
        # attempted access to success-page, while not charged
        priority_url = request.app.get_url('broadcast_priority_form',
                                           item_type=item.type,
                                           item_id=item.id)
        redirect(priority_url)

    messages = {
        'content': _('Priority broadcast has been successfully scheduled.'),
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
            '{0}/free/'.format(pre),
            'GET',
            show_broadcast_free_form,
            'broadcast_free_form',
            {}
        ), (
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
