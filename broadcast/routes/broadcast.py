"""
broadcast.py: Content upload

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import datetime

from bottle import request, redirect
from bottle_utils.csrf import csrf_protect, csrf_token
from bottle_utils.html import hsize
from bottle_utils.i18n import dummy_gettext as _

from ..forms.broadcast import ContentForm, TwitterForm
from ..helpers import upload_to_drive
from ..models.charges import Charge
from ..models.items import ContentItem, TwitterItem
from ..util.auth.users import User
from ..util.auth.helpers import send_confirmation_email
from ..util.security import sign
from ..util.template import template, view


@view('broadcast_content')
@csrf_token
def show_broadcast_content_form(item_type):
    id = ContentItem.generate_unique_id()
    signature = sign(id, secret_key=request.app.config['app.secret_key'])
    initial_data = {'id': id, 'signature': signature}
    form = ContentForm(initial_data)
    size_limit = hsize(request.app.config['{0}.size_limit'.format(item_type)])
    return dict(form=form,
                item_type=item_type,
                size_limit=size_limit.replace('.00', ''))


@csrf_protect
def broadcast_content(item_type):
    form_data = request.forms.decode()
    form_data.update(request.files)
    form = ContentForm(form_data)
    if form.is_valid():
        email = form.processed_data['email']
        if request.user.is_authenticated:
            email = request.user.email
        else:
            try:
                user = User.create(email=email, db=request.db.sessions)
            except User.AlreadyExists:
                pass  # ignore, just resend confirmation mail
            else:
                user.make_logged_in()

            send_confirmation_email(email,
                                    next_path='/',
                                    config=request.app.config,
                                    db=request.db.sessions)

        item = ContentItem.create(created=datetime.datetime.utcnow(),
                                  title=form.processed_data['title'],
                                  language=form.processed_data['language'],
                                  id=form.processed_data['id'],
                                  size=form.processed_data['file_size'],
                                  status=ContentItem.PROCESSING,
                                  license=form.processed_data['license'],
                                  email=email,
                                  url=form.processed_data['url'])
        upload_root = request.app.config['content.upload_root']
        path = item.save_file(form.processed_data['content_file'],
                              upload_root=upload_root)
        item.update(path=path)
        Charge.create(item_id=item.id,
                      item_type=item.type,
                      plan=form.payment_plan)
        if form.processed_data['mode'] == 'priority':
            next_url = request.app.get_url('broadcast_priority_form',
                                           item_type=item.type,
                                           item_id=item.id)
            redirect(next_url)
        else:
            task_runner = request.app.config['task.runner']
            task_runner.schedule(upload_to_drive, item, request.app.config)
            message = _('Free uplink has been successfully scheduled.')
            return template('feedback',
                            item=item,
                            status='success',
                            page_title=_('Uplink Scheduled'),
                            message=message,
                            redirect_url=request.app.get_url('main'),
                            redirect_target=_('main page'))

    size_limit = hsize(request.app.config['{0}.size_limit'.format(item_type)])
    return template('broadcast_content',
                    form=form,
                    item_type=item_type,
                    size_limit=size_limit.replace('.00', ''))


@view('broadcast_twitter')
@csrf_token
def show_broadcast_twitter_form():
    return dict(form=TwitterForm())


@csrf_protect
@view('broadcast_twitter')
def broadcast_twitter():
    form = TwitterForm(request.forms)
    if form.is_valid():
        item = TwitterItem.create(status=TwitterItem.PROCESSING,
                                  created=datetime.datetime.utcnow(),
                                  handle=form.processed_data['handle'],
                                  id=TwitterItem.generate_unique_id())
        Charge.create(item_id=item.id,
                      item_type=item.type,
                      plan=form.processed_data['plan'])
        next_url = request.app.get_url('broadcast_priority_form',
                                       item_type=item.type,
                                       item_id=item.id)
        redirect(next_url)

    return dict(form=form)


def route(conf):
    return (
        (
            '/broadcast/<item_type:re:content>/',
            'GET',
            show_broadcast_content_form,
            'broadcast_content_form',
            {}
        ), (
            '/broadcast/<item_type:re:content>/',
            'POST',
            broadcast_content,
            'broadcast_content',
            {}
        ), (
            '/broadcast/twitter/',
            'GET',
            show_broadcast_twitter_form,
            'broadcast_twitter_form',
            {}
        ), (
            '/broadcast/twitter/',
            'POST',
            broadcast_twitter,
            'broadcast_twitter',
            {}
        ),
    )
