"""
admin.py: Routes reserved for superusers only

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from bottle import redirect, request, static_file

from ..util.auth import login_required
from ..util.broadcast import get_item, filter_items
from ..util.template import view


def scheduled_redirect():
    return redirect(request.app.get_url('scheduled_list'))


@login_required(superuser_only=True)
@view('scheduled_list')
def scheduled_list():
    items = []
    for item_type in request.app.config['app.broadcast_types']:
        items.extend(filter_items(item_type))

    return dict(items=sorted(items, key=lambda x: x.created, reverse=True))


@login_required(superuser_only=True)
@view('scheduled_list')
def scheduled_type_list(item_type):
    items = filter_items(item_type)
    return dict(items=sorted(items, key=lambda x: x.created, reverse=True))


@login_required(superuser_only=True)
@view('scheduled_detail')
def scheduled_detail(item_type, item_id):
    item = get_item(item_type, id=item_id)
    return dict(item=item)


@login_required(superuser_only=True)
def expose_content(item_type, item_id, name):
    if item_type != "twitter":
        return scheduled_file(item_id, name)
    url = "https://twitter.com/{}".format(name)
    redirect(url)


@login_required(superuser_only=True)
def scheduled_file(item_id, filename):
    upload_root = request.app.config['content.upload_root']
    root = upload_root + '/' + item_id
    return static_file(filename, root=root)


def route(conf):
    types = '|'.join(conf['app.broadcast_types'])
    return (
        (
            '/admin/',
            'GET',
            scheduled_redirect,
            'scheduled_redirect',
            {}
        ), (
            '/admin/scheduled/',
            'GET',
            scheduled_list,
            'scheduled_list',
            {}
        ), (
            '/admin/scheduled/<item_type:re:%s>/' % types,
            'GET',
            scheduled_type_list,
            'scheduled_type_list',
            {}
        ), (
            '/admin/scheduled/<item_type:re:%s>/<item_id:re:[0-9a-f]{32}>' % types,
            'GET',
            scheduled_detail,
            'scheduled_detail',
            {}
        ), (
            '/admin/<item_type:re:%s>/<item_id:re:[0-9a-f]{32}>/<name>' % types,
            'GET',
            expose_content,
            'expose_content',
            {}
        ),
    )
