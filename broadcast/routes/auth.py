"""
auth.py: Authentication routes

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import logging

from bottle_utils.i18n import dummy_gettext as _

from ..models.auth import (
    User,
    EmailVerificationToken,
    PasswordResetToken,
    InvitationToken,
)
from ..forms.auth import (
    LoginForm,
    RegisterForm,
    EmailVerificationForm,
    PasswordResetRequestForm,
    ResetPasswordForm,
    AcceptInvitationForm,
)
from ..util.routes import (
    ActionXHRPartialFormRoute,
    ActionTemplateRoute,
    CSRFMixin,
    XHRJsonRoute,
    RoleMixin,
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
        if self.request.params.get('next'):
            return _('your previous location')
        return super(NextPathMixin, self).get_success_url_label()

    def get_error_url_label(self):
        if self.request.params.get('next'):
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


class ConfirmationMixin(object):
    """
    This mixin is used with token confirmation code. The token will be fetched
    from the database based on the key, and assigned to ``token`` property on
    the handler object. If there is no matching token, ``None`` is assigned
    instead. The token's key and email are added to the template context for
    GET requests, but not post.
    """
    token_class = None

    def create_response(self):
        key = self.kwargs['key']
        if not self.token_class:
            raise NotImplementedError('Subclass must define the token_class '
                                      'property.')
        self.token_class.clear_expired()
        try:
            self.token = self.token_class.get(key=key)
        except self.token_class.NotFound:
            self.token = None
        super(ConfirmationMixin, self).create_response()

    def get_context(self):
        ctx = super(ConfirmationMixin, self).get_context()
        ctx['key'] = self.token.key if self.token else None
        ctx['email'] = self.token.email if self.token else None
        return ctx


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


class PasswordResetRequest(CSRFMixin, LoginOnSuccessMixin,
                           ActionXHRPartialFormRoute):
    path = '/accounts/password-reset'
    template_name = 'auth/password_reset_request.mako'
    partial_template_name = 'auth/_password_reset_request.mako'
    form_factory = PasswordResetRequestForm
    success_message = _('Check your inbox for a password reset link')


class ConfirmEmail(ConfirmationMixin, LoginOnSuccessMixin, NextPathMixin,
                   ActionTemplateRoute):
    token_class = EmailVerificationToken
    path = '/accounts/verify/<key:re:[0-9a-f]{32}>'
    success_message = _('Your email address has been confirmed')
    error_message = _('The confirmation link has expired or has already been '
                      'used.')
    error_url = ('main:home', {})
    error_url_label = _('main page')

    def get(self, key):
        if self.token:
            self.token.accept()
            self.status = True
        else:
            self.status = False


class AcceptInvitation(ConfirmationMixin, CSRFMixin, RoleMixin,
                       LoginOnSuccessMixin, ActionXHRPartialFormRoute):
    role = RoleMixin.GUEST
    strict_check = True
    role_denied_message = _('You should lot out if you wish to create another '
                            'account')
    path = '/accounts/accept-invite/<key:re:[0-9a-f]{32}>'
    template_name = 'auth/accept_invitation.mako'
    partial_template_name = 'auth/_accept_invitation.mako'
    form_factory = AcceptInvitationForm
    token_class = InvitationToken
    success_message = _('Registration is complete')

    def get(self, key):
        if not self.token:
            self.abort(404)
        return super(AcceptInvitation, self).get(key)


class ResetPassword(ConfirmationMixin, CSRFMixin, LoginOnSuccessMixin,
                    ActionXHRPartialFormRoute):
    path = '/accounts/reset-password/<key:re:[0-9a-f]{32}>'
    template_name = 'auth/reset_password.mako'
    partial_template_name = 'auth/_reset_password.mako'
    form_factory = ResetPasswordForm
    token_class = PasswordResetToken
    success_message = _('Your password has been updated')

    def get(self, key):
        if not self.token:
            self.abort(404)
        return super(ResetPassword, self).get(key)


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
        AcceptInvitation,
        PasswordResetRequest,
        ResetPassword,
        NameCheck,
    )
