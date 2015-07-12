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
from bottle_utils.html import set_qparam
from bottle_utils.i18n import dummy_gettext as _

from ..forms.broadcast import ContentForm, ContentDetailsForm, TwitterForm
from ..util.broadcast import (ContentItem,
                              TwitterItem,
                              get_unique_id,
                              sign,
                              fetch_item)
from ..util.template import template, view


@view('broadcast_content')
@csrf_token
def show_broadcast_content_form():
    url_template = request.app.config['content.url_template']
    url_prefix = url_template.format(_("your-username"))
    id = get_unique_id()
    signature = sign(id, secret_key=request.app.config['app.secret_key'])
    initial_data = {'id': id, 'signature': signature}
    return dict(form=ContentForm(initial_data), url_prefix=url_prefix)


@csrf_protect
@view('broadcast_content')
def broadcast_content():
    url_template = request.app.config['content.url_template']
    form_data = request.forms.decode()
    form_data.update(request.files)
    form = ContentForm(form_data)
    if form.is_valid():
        content_item = ContentItem(
            created=datetime.datetime.utcnow(),
            title=form.processed_data['title'],
            url=form.processed_data['url'],
            id=form.processed_data['id'],
            content_file=form.processed_data['content_file'],
            file_size=form.processed_data['file_size']
        )
        content_item.save()
        next_url = request.app.get_url('broadcast_content_details_form',
                                       item_type=content_item.type,
                                       item_id=content_item.id)
        redirect(next_url + set_qparam(mode='free').to_qs())

    return dict(form=form, url_prefix=url_template)


@view('broadcast_content_details')
@fetch_item
@csrf_token
def show_broadcast_content_details_form(item):
    mode = request.params.get('mode', 'free')
    signature = sign(item.id, secret_key=request.app.config['app.secret_key'])
    initial_data = {'mode': mode,
                    'id': item.id,
                    'signature': signature,
                    'language': item.language,
                    'license': item.license}
    return dict(item=item, mode=mode, form=ContentDetailsForm(initial_data))


@csrf_protect
@fetch_item
def broadcast_content_details(item):
    form = ContentDetailsForm(request.forms)
    if form.is_valid():
        item.update(status=ContentItem.PROCESSING,
                    language=form.processed_data['language'],
                    license=form.processed_data['license'])
        if form.processed_data['mode'] == 'priority':
            next_url = request.app.get_url('broadcast_priority_form',
                                           item_type=item.type,
                                           item_id=item.id)
            redirect(next_url)
        else:
            message = _('Free broadcast has been successfully scheduled.')
            return template('feedback',
                            item=item,
                            status='success',
                            page_title=_('Broadcast Scheduled'),
                            message=message,
                            redirect_url=request.app.get_url('main'),
                            redirect_target=_('main page'))
    return template('broadcast_content_details',
                    item=item,
                    form=form,
                    mode=form.processed_data['mode'])


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
            '/broadcast/<item_type:re:content>/<item_id:re:[0-9a-f]{32}>/details/',
            'GET',
            show_broadcast_content_details_form,
            'broadcast_content_details_form',
            {}
        ), (
            '/broadcast/<item_type:re:content>/<item_id:re:[0-9a-f]{32}>/details/',
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
