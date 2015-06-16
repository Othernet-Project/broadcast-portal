"""
broadcast.py: Content upload

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

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
    path_template = request.app.config['content.content_path_template']
    path_prefix = path_template.format(request.user.username)
    content_id = get_content_id()
    signature = sign(content_id,
                     secret_key=request.app.config['app.secret_key'])
    initial_data = {'content_id': content_id, 'signature': signature}
    return dict(form=ContentForm(initial_data), path_prefix=path_prefix)


@csrf_protect
@login_required()
@view('broadcast')
def broadcast():
    path_template = request.app.config['content.content_path_template']
    path_prefix = path_template.format(request.user.username)
    form_data = request.forms.decode()
    form_data.update(request.files)
    form = ContentForm(form_data)
    if form.is_valid():
        content_id = form.processed_data['content_id']
        uploaded_file = form.processed_data['content_file']
        # store uploaded file on disk
        file_path = save_upload(content_id, uploaded_file)
        save_content(content_id=content_id,
                     email=request.user.email,
                     name=request.user.username,
                     file_path=file_path,
                     title=form.processed_data['title'],
                     license=form.processed_data['license'],
                     url=form.processed_data['path'])
        redirect('broadcast_free_form')

    return dict(form=form, path_prefix=path_prefix)


def route(conf):
    return (
        ('/broadcast/', 'GET', show_broadcast_form, 'broadcast_form', {}),
        ('/broadcast/', 'POST', broadcast, 'broadcast', {}),
    )
