"""
auth.py: Authentication routes

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from bottle import request, redirect
from bottle_utils.csrf import csrf_protect, csrf_token
from bottle_utils.i18n import dummy_gettext as _

from ..forms.auth import (LoginForm,
                          RegistrationForm,
                          ConfirmationForm,
                          PasswordResetRequestForm,
                          PasswordResetForm)
from ..util.auth import (create_user,
                         get_user,
                         create_temporary_key,
                         confirm_user,
                         reset_password,
                         login_user_no_auth,
                         KeyExpired,
                         KeyNotFound)
from ..util.email import send_mail
from ..util.http import http_redirect
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
        return http_redirect(next_path)

    return dict(next_path=next_path,
                login_form=login_form,
                registration_form=RegistrationForm())


@view('confirmation')
@csrf_token
def send_confirmation_form():
    return dict(form=ConfirmationForm())


@csrf_protect
def send_confirmation(email=None):
    if email is None:
        form = ConfirmationForm(request.params)
        if not form.is_valid():
            return template('confirmation', form=form)

        email = form.processed_data['email']

    expiration = request.app.config['authentication.confirmation_expires']
    confirmation_key = create_temporary_key(email, expiration)
    request.app.config['app.url'] = request.url
    task_runner = request.app.config['task.runner']
    task_runner.schedule(send_mail,
                         email,
                         _("Confirm registration"),
                         text='email/confirm',
                         data={'confirmation_key': confirmation_key},
                         config=request.app.config)
    return template('feedback',
                    page_title=_('Account registration complete'),
                    status='email',
                    redirect_url=request.app.get_url('login'),
                    message=_('Confirmation email has been sent to '
                              '{address}. Check your inbox.').format(
                                  address=email),
                    redirect_target=_('log-in'))


@view('feedback')
def confirm(key):
    try:
        email = confirm_user(key)
    except KeyExpired:
        return {'message': _("The confirmation key has already expired."),
                'page_title': _("Confirmation"),
                'status': 'error',
                'redirect_url': request.app.get_url('login'),
                'redirect_target': _('log-in')}
    except KeyNotFound:
        return {'message': _("The confirmation key is not valid."),
                'page_title': _("Confirmation"),
                'status': 'error',
                'redirect_url': request.app.get_url('login'),
                'redirect_target': _('log-in')}
    else:
        login_user_no_auth(email)
        return {'message': _("E-mail address successfully confirmed. You have "
                             "been automatically logged in."),
                'page_title': _("Confirmation"),
                'status': 'success',
                'redirect_url': request.app.get_url('main'),
                'redirect_target': _('the main page')}


@view('password_reset_request')
@csrf_token
def password_reset_request_form():
    return dict(form=PasswordResetRequestForm())


@csrf_protect
def password_reset_request():
    form = PasswordResetRequestForm(request.params)
    if not form.is_valid():
        return template('password_reset_request', form=form)

    email = form.processed_data['email']
    if get_user(email):
        expires = request.app.config['authentication.password_reset_expires']
        reset_key = create_temporary_key(email, expires)
        task_runner = request.app.config['task.runner']
        task_runner.schedule(send_mail,
                             email,
                             _("Reset Password"),
                             text='email/password_reset',
                             data={'reset_key': reset_key},
                             config=request.app.config)
    return template('feedback',
                    page_title=_('Password reset email sent'),
                    status='email',
                    redirect_url=request.app.get_url('login'),
                    message=_('An email with a password reset link has been '
                              'sent to {address}. Check your inbox.').format(
                                  address=email),
                    redirect_target=_('log-in'))


@view('password_reset')
@csrf_token
def password_reset_form(key):
    return dict(form=PasswordResetForm({'key': key}))


@csrf_protect
def password_reset(key):
    form = PasswordResetForm(request.forms)
    if not form.is_valid():
        return template('password_reset', form=form)

    key = form.processed_data['key']
    new_password = form.processed_data['new_password1']
    reset_password(key, new_password)
    return template('feedback',
                    page_title=_('Password reset successful'),
                    status='success',
                    redirect_url=request.app.get_url('login'),
                    message=_('You have successfully reset your password.'),
                    redirect_target=_('log-in'))


@view('register')
@csrf_token
def show_register_form():
    return dict(registration_form=RegistrationForm())


@csrf_protect
def register():
    referer = request.headers.get('Referer', 'register')
    template_name = 'login' if 'login' in referer else 'register'
    next_path = request.params.get('next', '/')
    registration_form = RegistrationForm(request.params)

    if registration_form.is_valid():
        username = registration_form.processed_data['username']
        email = registration_form.processed_data['email']
        password = registration_form.processed_data['password1']
        create_user(username=username,
                    password=password,
                    email=email,
                    db=request.db.sessions)
        return send_confirmation(email)

    return template(template_name,
                    next_path=next_path,
                    login_form=LoginForm(),
                    registration_form=registration_form)


def check_available():
    username_or_email = request.params.get('account', '').strip()
    if not username_or_email:
        return {'result': False}
    return {'result': get_user(username_or_email) is not None}


def logout():
    next_path = request.params.get('next', '/')
    request.user.logout()
    redirect(next_path)


def route(conf):
    return (
        ('/login/', 'GET', show_login_form, 'login_form', {}),
        ('/login/', 'POST', login, 'login', {}),
        ('/register/', 'GET', show_register_form, 'register_form', {}),
        ('/register/', 'POST', register, 'register', {}),
        ('/check/', 'GET', check_available, 'check_available', {}),
        ('/confirm/', 'GET', send_confirmation_form, 'send_confirmation_form', {}),
        ('/confirm/', 'POST', send_confirmation, 'send_confirmation', {}),
        ('/confirm/<key:re:[0-9a-f]{32}>', 'GET', confirm, 'confirm', {}),
        ('/password-reset/', 'GET', password_reset_request_form, 'password_reset_request_form', {}),
        ('/password-reset/', 'POST', password_reset_request, 'password_reset_request', {}),
        ('/password-reset/<key:re:[0-9a-f]{32}>', 'GET', password_reset_form, 'password_reset_form', {}),
        ('/password-reset/<key:re:[0-9a-f]{32}>', 'POST', password_reset, 'password_reset', {}),
        ('/logout/', 'GET', logout, 'logout', {}),
    )
