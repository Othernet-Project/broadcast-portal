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

from ..forms.broadcast import ContentForm, TwitterForm
from ..util.auth import login_required
from ..util.broadcast import ContentItem, TwitterItem, get_unique_id, sign
from ..util.template import view


@login_required()
@view('broadcast_content')
@csrf_token
def show_broadcast_content_form():
    url_template = request.app.config['content.url_template']
    url_prefix = url_template.format(request.user.username)
    id = get_unique_id()
    signature = sign(id, secret_key=request.app.config['app.secret_key'])
    initial_data = {'id': id, 'signature': signature}
    return dict(form=ContentForm(initial_data), url_prefix=url_prefix)


@csrf_protect
@login_required()
@view('broadcast_content')
def broadcast_content():
    url_template = request.app.config['content.url_template']
    url_prefix = url_template.format(request.user.username)
    form_data = request.forms.decode()
    form_data.update(request.files)
    form = ContentForm(form_data)
    if form.is_valid():
        content_item = ContentItem(
            email=request.user.email,
            name=request.user.username,
            created=datetime.datetime.utcnow(),
            title=form.processed_data['title'],
            license=form.processed_data['license'],
            url=form.processed_data['url'],
            id=form.processed_data['id'],
            content_file=form.processed_data['content_file'],
            file_size=form.processed_data['file_size']
        )
        content_item.save()
        next_url = request.app.get_url('broadcast_free_form',
                                       item_type=content_item.type,
                                       item_id=content_item.id)
        redirect(next_url)

    return dict(form=form, url_prefix=url_prefix)


@login_required()
@view('broadcast_twitter')
@csrf_token
def show_broadcast_twitter_form():
    return dict(form=TwitterForm())


@csrf_protect
@login_required()
@view('broadcast_twitter')
def broadcast_twitter():
    form = TwitterForm(request.forms)
    if form.is_valid():
        twitter_item = TwitterItem(email=request.user.email,
                                   name=request.user.username,
                                   created=datetime.datetime.utcnow(),
                                   handle=form.processed_data['handle'],
                                   plan=form.processed_data['plan'],
                                   id=get_unique_id())
        twitter_item.save()
        next_url = request.app.get_url('broadcast_priority_form',
                                       item_type=twitter_item.type,
                                       item_id=twitter_item.id)
        redirect(next_url)

    return dict(form=form)


def route(conf):
    return (
        (
            '/broadcast/content/',
            'GET',
            show_broadcast_content_form,
            'broadcast_content_form',
            {}
        ), (
            '/broadcast/content/',
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
