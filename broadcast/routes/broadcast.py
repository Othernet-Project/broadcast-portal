"""
broadcast.py: Content upload

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import os

from bottle import request
from bottle_utils.csrf import csrf_protect, csrf_token

from ..forms.broadcast import ContentForm
from ..util.auth import login_required
from ..util.template import view


@login_required()
@view('broadcast')
@csrf_token
def show_broadcast_form():
    return dict(form=ContentForm())


@csrf_protect
@login_required()
@view('broadcast')
def broadcast():
    form_data = request.forms.decode()
    form_data.update(request.files)
    form = ContentForm(form_data)
    if form.is_valid():
        uploaded_file = form.processed_data['content']
        upload_root = request.app.config['app.upload_root']
        upload_path = os.path.join(upload_root, uploaded_file.filename)
        uploaded_file.save(upload_path)

    return dict(form=form)


def route(conf):
    return (
        ('/broadcast/', 'GET', show_broadcast_form, 'broadcast_form', {}),
        ('/broadcast/', 'POST', broadcast, 'broadcast', {}),
    )
