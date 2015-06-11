"""
auth.py: Authentication routes

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from bottle import request, redirect
from bottle_utils.csrf import csrf_protect, csrf_token

from ..forms.auth import LoginForm
from ..util.template import view


@view('login')
@csrf_token
def show_login_form():
    return dict(form=LoginForm(), next_path=request.params.get('next', '/'))


@view('login')
@csrf_protect
def login():
    next_path = request.params.get('next', '/')

    form = LoginForm(request.params)
    if form.is_valid():
        return redirect(next_path)

    return dict(next_path=next_path, form=form)


def logout():
    next_path = request.params.get('next', '/')
    request.user.logout()
    redirect(next_path)


def route(conf):
    return (
        ('/login/', 'GET', show_login_form, 'login_form', {}),
        ('/login/', 'POST', login, 'login', {}),
        ('/logout/', 'GET', logout, 'logout', {}),
    )
