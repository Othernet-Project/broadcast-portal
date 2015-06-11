"""
auth.py: Authentication routes

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from bottle import request, redirect
from bottle_utils.csrf import csrf_protect, csrf_token

from ..forms.auth import LoginForm, RegistrationForm
from ..util.template import view, template


@view('login')
@csrf_token
def show_login_form():
    return dict(login_form=LoginForm(),
                registration_form=RegistrationForm(),
                next_path=request.params.get('next', '/'))


@view('login')
@csrf_protect
def login():
    next_path = request.params.get('next', '/')
    login_form = LoginForm(request.params)
    if login_form.is_valid():
        return redirect(next_path)

    return dict(next_path=next_path,
                login_form=login_form,
                registration_form=RegistrationForm())


@csrf_protect
def register():
    next_path = request.params.get('next', '/')
    registration_form = RegistrationForm(request.params)
    if registration_form.is_valid():
        email = registration_form.processed_data['email']
        return template('confirm', email=email)

    return template('login',
                    next_path=next_path,
                    login_form=LoginForm(),
                    registration_form=registration_form)


def logout():
    next_path = request.params.get('next', '/')
    request.user.logout()
    redirect(next_path)


def route(conf):
    return (
        ('/login/', 'GET', show_login_form, 'login_form', {}),
        ('/login/', 'POST', login, 'login', {}),
        ('/register/', 'POST', register, 'register', {}),
        ('/logout/', 'GET', logout, 'logout', {}),
    )
