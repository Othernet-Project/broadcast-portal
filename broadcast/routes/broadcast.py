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

from ..forms.broadcast import (ContentForm,
                               ContentDetailsForm,
                               TVForm,
                               TVDetailsForm,
                               TwitterForm)
from ..util.broadcast import (ContentItem,
                              TVItem,
                              TwitterItem,
                              get_unique_id,
                              sign,
                              fetch_item)
from ..util.template import template, view


@view('broadcast_content')
@csrf_token
def show_broadcast_content_form(item_type):
    id = get_unique_id()
    signature = sign(id, secret_key=request.app.config['app.secret_key'])
    initial_data = {'id': id, 'signature': signature}
    form_cls = {'content': ContentForm, 'tv': TVForm}[item_type]
    size_limit = hsize(request.app.config['{0}.size_limit'.format(item_type)])
    return dict(form=form_cls(initial_data),
                item_type=item_type,
                size_limit=size_limit)


@csrf_protect
@view('broadcast_content')
def broadcast_content(item_type):
    form_data = request.forms.decode()
    form_data.update(request.files)
    form_cls = {'content': ContentForm, 'tv': TVForm}[item_type]
    form = form_cls(form_data)
    if form.is_valid():
        item_cls = {'content': ContentItem, 'tv': TVItem}[item_type]
        item = item_cls(
            created=datetime.datetime.utcnow(),
            title=form.processed_data['title'],
            language=form.processed_data['language'],
            id=form.processed_data['id'],
            content_file=form.processed_data['content_file'],
            file_size=form.processed_data['file_size']
        )
        item.save()
        next_url = request.app.get_url('broadcast_content_details_form',
                                       item_type=item.type,
                                       item_id=item.id)
        redirect(next_url)

    size_limit = hsize(request.app.config['{0}.size_limit'.format(item_type)])
    return dict(form=form, item_type=item_type, size_limit=size_limit)


@view('broadcast_content_details')
@fetch_item
@csrf_token
def show_broadcast_content_details_form(item):
    signature = sign(item.id, secret_key=request.app.config['app.secret_key'])
    initial_data = {'id': item.id,
                    'signature': signature,
                    'license': item.license}
    form_cls = {'content': ContentDetailsForm, 'tv': TVDetailsForm}[item.type]
    return dict(item=item, form=form_cls(initial_data))


@csrf_protect
@fetch_item
def broadcast_content_details(item):
    form_cls = {'content': ContentDetailsForm, 'tv': TVDetailsForm}[item.type]
    form = form_cls(request.forms)
    if form.is_valid():
        item_cls = {'content': ContentItem, 'tv': TVItem}[item.type]
        item.update(status=item_cls.PROCESSING,
                    license=form.processed_data['license'],
                    email=form.processed_data['email'])
        if form.processed_data['mode'] == 'priority':
            next_url = request.app.get_url('broadcast_priority_form',
                                           item_type=item.type,
                                           item_id=item.id)
            redirect(next_url)
        else:
            message = _('Free uplink has been successfully scheduled.')
            return template('feedback',
                            item=item,
                            status='success',
                            page_title=_('Uplink Scheduled'),
                            message=message,
                            redirect_url=request.app.get_url('main'),
                            redirect_target=_('main page'))
    return template('broadcast_content_details', item=item, form=form)


@view('broadcast_twitter')
@csrf_token
def show_broadcast_twitter_form():
    return dict(form=TwitterForm())


@csrf_protect
@view('broadcast_twitter')
def broadcast_twitter():
    form = TwitterForm(request.forms)
    if form.is_valid():
        twitter_item = TwitterItem(status=TwitterItem.PROCESSING,
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
            '/broadcast/<item_type:re:content|tv>/',
            'GET',
            show_broadcast_content_form,
            'broadcast_content_form',
            {}
        ), (
            '/broadcast/<item_type:re:content|tv>/',
            'POST',
            broadcast_content,
            'broadcast_content',
            {}
        ), (
            '/broadcast/<item_type:re:content|tv>/<item_id:re:[0-9a-f]{32}>/details/',
            'GET',
            show_broadcast_content_details_form,
            'broadcast_content_details_form',
            {}
        ), (
            '/broadcast/<item_type:re:content|tv>/<item_id:re:[0-9a-f]{32}>/details/',
            'POST',
            broadcast_content_details,
            'broadcast_content_details',
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
