"""
broadcast.py: Content upload

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import os

from bottle import request, redirect
from bottle_utils.csrf import csrf_protect, csrf_token

from ..forms.broadcast import ContentForm
from ..util.auth import login_required
from ..util.broadcast import get_content_id, sign, save_upload, save_content
from ..util.template import view


@login_required()
@view('broadcast')
@csrf_token
def show_broadcast_form():
    url_template = request.app.config['content.url_template']
    url_prefix = url_template.format(request.user.username)
    content_id = get_content_id()
    signature = sign(content_id,
                     secret_key=request.app.config['app.secret_key'])
    initial_data = {'content_id': content_id, 'signature': signature}
    return dict(form=ContentForm(initial_data), url_prefix=url_prefix)


@csrf_protect
@login_required()
@view('broadcast')
def broadcast():
    url_template = request.app.config['content.url_template']
    url_prefix = url_template.format(request.user.username)
    form_data = request.forms.decode()
    form_data.update(request.files)
    form = ContentForm(form_data)
    if form.is_valid():
        content_id = form.processed_data['content_id']
        uploaded_file = form.processed_data['content_file']
        # store uploaded file on disk
        file_path = save_upload(content_id, uploaded_file)
        abs_file_path = os.path.join(request.app.config['content.upload_root'],
                                     file_path)
        file_size = os.path.getsize(abs_file_path)
        save_content(content_id=content_id,
                     email=request.user.email,
                     name=request.user.username,
                     file_path=file_path,
                     file_size=file_size,
                     title=form.processed_data['title'],
                     license=form.processed_data['license'],
                     url=form.processed_data['url'])
        next_url = request.app.get_url('broadcast_free_form',
                                       content_id=content_id)
        redirect(next_url)

    return dict(form=form, url_prefix=url_prefix)


def route(conf):
    return (
        ('/broadcast/', 'GET', show_broadcast_form, 'broadcast_form', {}),
        ('/broadcast/', 'POST', broadcast, 'broadcast', {}),
    )
