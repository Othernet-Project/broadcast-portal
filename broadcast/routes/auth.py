"""
auth.py: Authentication routes

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import logging

from bottle_utils.i18n import dummy_gettext as _

from ..models.auth import User, EmailVerificationToken
from ..forms.auth import (
    LoginForm,
    RegisterForm,
    EmailVerificationForm,
    PasswordResetRequestForm,
    ResetPasswordForm,
)
from ..util.routes import (
    ActionXHRPartialFormRoute,
    ActionTemplateRoute,
    CSRFMixin,
    XHRJsonRoute,
)


class NextPathMixin(object):
    """
    This mixin select the appropriate URL and label depending on whether the
    redirect path is present in the request parameters.
    """
    success_url = ('main:home', {})
    success_url_label = _('main page')
    error_url = success_url
    error_url_label = _('main page')

    def get_success_url(self):
        return self.request.params.get(
            'next', super(NextPathMixin, self).get_success_url())

    def get_error_url(self):
        return self.request.params.get(
            'next', super(NextPathMixin, self).get_error_url())

    def get_success_url_label(self):
        if self.params.get('next'):
            return _('your previous location')
        return super(NextPathMixin, self).get_success_url_label()

    def get_error_url_label(self):
        if self.params.get('next'):
            return _('your previous location')
        return super(NextPathMixin, self).get_error_url_label()


class LoginOnSuccessMixin(object):
    """
    Used in conjunction with Action* routes where user is to be redirected to
    the log-in page on successful action.
    """
    success_url = ('auth:login', {})
    success_url_label = _('log-in page')


class NoLoginNeededMixin(object):
    """
    Used with routes requiring login for anonymous users, causing non-anonymous
    users to go straigth to success URL.
    """
    def get(self):
        if not self.request.user.is_guest:
            # Don't bother authenticated users
            self.redirect(self.get_success_url())
        return super(NoLoginNeededMixin, self).get()


class Register(NoLoginNeededMixin, CSRFMixin, ActionXHRPartialFormRoute):
    path = '/accounts/'
    template_name = 'auth/register.mako'
    partial_template_name = 'auth/_register.mako'
    form_factory = RegisterForm
    success_message = _('Check your inbox for an email confirmation link')
    success_url = ('main:home', {})


class Login(NoLoginNeededMixin, CSRFMixin, NextPathMixin,
            ActionXHRPartialFormRoute):
    path = '/accounts/login'
    template_name = 'auth/login.mako'
    partial_template_name = 'auth/_login.mako'
    form_factory = LoginForm
    success_message = _('You have been logged in')


class ResendConfirmation(CSRFMixin, ActionXHRPartialFormRoute):
    path = '/accounts/resend-confirmation'
    template_name = 'auth/confirmation.mako'
    partial_template_name = 'auth/_confirmation.mako'
    form_factory = EmailVerificationForm
    success_message = _('Check your inbox for an email confirmation link')

    def get_success_url(self):
        return self.app.get_url('main:home')


class ConfirmEmail(LoginOnSuccessMixin, NextPathMixin, ActionTemplateRoute):
    path = '/accounts/verify/<key:re:[0-9a-f]{32}'
    success_message = _('Your email address has been confirmed')
    error_message = _('The confirmation link has expired or has already been '
                      'used.')
    error_message = _('main page')

    def get_error_url(self):
        return self.app.get_url('main:home')

    def get(self, key):
        EmailVerificationToken.clear_expired()
        try:
            token = EmailVerificationToken.get(key)
        except EmailVerificationToken.NotFound:
            self.status = False
            return
        else:
            token.accept()
            self.status = True


class PasswordResetRequest(CSRFMixin, LoginOnSuccessMixin,
                           ActionXHRPartialFormRoute):
    path = '/accounts/password-reset'
    template_name = 'auth/password_reset_request.mako'
    partial_template_name = 'auth/_password_reset_request.mako'
    form_factory = PasswordResetRequestForm
    success_message = _('Check your inbox for a password reset link')


class ResetPassword(CSRFMixin, LoginOnSuccessMixin,
                    ActionXHRPartialFormRoute):
    path = '/accounts/reset-password/<key:re:[0-9a-f]{32}'
    template_name = 'auth/reset_password.mako'
    partial_template_name = 'auth/_reset_password.mako'
    form_factory = ResetPasswordForm
    success_message = _('Your password has been updated')


class NameCheck(XHRJsonRoute):
    path = '/accounts/check-name'

    @staticmethod
    def has_username(username):
        try:
            User.get(username=username)
        except User.NotFound:
            return False
        else:
            return True

    def get(self):
        username = self.request.params.get('username', None)
        return {'result': self.has_username(username)}


class LogOut(ActionTemplateRoute):
    path = '/accounts/bye'
    success_message = _('You have been logged out')
    success_url = ('main:home', {})
    success_url_label = _('main page')
    error_message = _('The system could not log you out due to an error')
    error_url = ('main:home', {})
    error_url_label = _('main page')

    def get(self):
        try:
            self.request.user.logout()
        except Exception as e:
            logging.exception('Error while logging out user: %s (%s)',
                              e, self.request.user.username)
            self.status = False
        else:
            self.status = True


def route():
    return (
        Register,
        Login,
        ResendConfirmation,
        ConfirmEmail,
        PasswordResetRequest,
        ResetPassword,
        NameCheck,
    )
