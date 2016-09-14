"""
auth.py: Authentication form

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import time
import random

from bottle import request

from bottle_utils import form
from bottle_utils.i18n import lazy_gettext as _

from ..models.auth import (
    User,
    PasswordResetToken,
    InvitationToken,
)
from ..app.exts import container as exts
from ..util.validators import EmailValidator


class UniqueUsernameValidator(form.Validator):
    messages = {
        'user_taken': _('This username is already in use')
    }

    def validate(self, value):
        try:
            User.get(username=value)
        except User.NotFound:
            return value
        else:
            raise form.ValidationError('user_taken', {})


class UniqueEmailValidator(form.Validator):
    messages = {
        'user_taken': _('This email is already in use')
    }

    def validate(self, value):
        try:
            User.get(email=value)
        except User.NotFound:
            return value
        else:
            raise form.ValidationError('user_taken', {})


class EmailTokenMixin(object):
    TokenClass = None
    token_data = None

    def get_token_data(self):
        return self.token_data

    def send_token(self):
        next_path = request.params.get('next_path', '/')
        email = self.processed_data['email']
        try:
            User.get(email=email)
        except User.NotFound:
            # There is no such account, so we're faking it
            time.sleep(random.randint(2, 5))
        else:
            token = self.TokenClass.new(email, data=self.get_token_data())
            token.send(next_path)


class LoginForm(form.Form):
    messages = {
        # Translators, error shown when log in attempt fails
        'invalid': _("Please enter the correct username and password."),
    }

    # Translators, used as label for a login field
    username = form.StringField(_("Username or email"),
                                placeholder=_('Username or email'),
                                validators=[form.Required()])
    # Translators, used as label for a password field
    password = form.PasswordField(_("Password"),
                                  placeholder=_('Password'),
                                  validators=[form.Required()])

    def validate(self):
        username = self.processed_data['username']
        password = self.processed_data['password']
        try:
            User.login(username, password)
        except (User.NotFound, User.InvalidCredentials):
            raise form.ValidationError('invalid', {})


class TruthValidator(form.Validator):
    messages = {
        'truth': _('This field is required'),
    }

    def validate(self, value):
        if not value:
            raise form.ValidationError('truth', {})


class RegisterForm(EmailTokenMixin, form.Form):
    TokenClass = PasswordResetToken
    token_data = 'registration'

    min_password_length = 4
    messages = {
        'pwmatch': _("The entered passwords do not match."),
        'userexists': _("User with specified username or email already "
                        "exits."),
    }

    username = form.StringField(
        # Translators, used as label in create user form
        _("Username"),
        validators=[form.Required(), UniqueUsernameValidator()],
        placeholder=_('Username'),
        messages={
            'username_taken': _("Username already taken."),
        })
    email = form.StringField(
        # Translators, used as label in create user form
        _("Email"),
        validators=[form.Required(), EmailValidator(), UniqueEmailValidator()],
        placeholder=_('Email'))

    def validate(self):
        email = self.processed_data['email']
        if email in exts.beta_whitelist:
            group = User.MODERATOR
        else:
            group = User.USER
        try:
            User.new(username=self.processed_data['username'],
                     email=email,
                     group=group)
        except User.IntegrityError:
            raise form.ValidationError('userexists')
        self.send_token()


class EmailVerificationForm(EmailTokenMixin, form.Form):
    TokenClass = PasswordResetToken
    token_data = 'registration'

    email = form.StringField(
        # Translators, used as label in create user form
        _("Email"),
        validators=[form.Required(), EmailValidator()],
        placeholder=_('Email'))

    def validate(self):
        self.send_token()


class PasswordResetRequestForm(EmailTokenMixin, form.Form):
    TokenClass = PasswordResetToken

    # Translators, used as label in create user form
    email = form.StringField(
        # Translators, used as label in create user form
        _("Email"),
        validators=[form.Required(), EmailValidator()],
        placeholder=_('Email'))

    def validate(self):
        self.send_token()


class ResetPasswordForm(form.Form):
    min_password_length = 4
    messages = {
        # Translators, error shown when password reset fails
        'pwmatch': _("The entered passwords do not match."),
        'key_expired': _("The password reset key has already expired."),
        'key_invalid': _("The password reset key is not valid.")
    }
    key = form.HiddenField()
    new_password1 = form.PasswordField(
        # Translators, used as label in password reset form
        _("New password"),
        validators=[form.Required()],
        placeholder=_('Password'),
        messages={
            'password_length': _('Must be longer than {length} characters.'),
        }
    )
    new_password2 = form.PasswordField(
        # Translators, used as label in password reset form
        _("Confirm new password"),
        validators=[form.Required()],
        placeholder=_('Password'),
        messages={
            'password_length': _('Must be longer than {length} characters.'),
        }
    )

    def validate(self):
        key = self.processed_data['key']
        try:
            token = PasswordResetToken.get(key=key)
        except PasswordResetToken.NotFound:
            raise form.ValidationError('key_invalid', {})
        new_password1 = self.processed_data['new_password1']
        new_password2 = self.processed_data['new_password2']
        if new_password1 != new_password2:
            raise form.ValidationError('pwmatch', {})
        is_reg = token.data == 'registration'
        self.processed_data['is_reg'] = is_reg
        user = token.accept(new_password1)
        self.processed_data['is_moderator'] = user.group == user.MODERATOR


class AcceptInvitationForm(form.Form):
    min_password_length = 4
    messages = {
        'pwmatch': _("The entered passwords do not match."),
        'userexists': _("User with specified username or email already "
                        "exits."),
        'claimed': _("Email matching this invitation has already been "
                     "claimed"),
        'key_expired': _("The password reset key has already expired."),
        'key_invalid': _("The password reset key is not valid.")
    }
    email = form.HiddenField()
    key = form.HiddenField()
    username = form.StringField(
        # Translators, used as label in create user form
        _("Username"),
        validators=[form.Required(), UniqueUsernameValidator()],
        placeholder=_('Username'),
        messages={
            'username_taken': _("Username already taken."),
        })
    password1 = form.PasswordField(
        # Translators, used as label in create user form
        _("Password"),
        validators=[form.Required()],
        placeholder=_('Password'),
        messages={
            'password_length': _('Must be longer than {length} characters.'),
        })
    password2 = form.PasswordField(
        # Translators, used as label in create user form
        _("Confirm Password"),
        validators=[form.Required()],
        placeholder=_('Retype the password'))

    def preprocess_password(self, value):
        if len(value) < self.min_password_length:
            raise form.ValidationError('password_length',
                                       {'length': self.min_password_length})

    def validate(self):
        key = self.processed_data['key']
        try:
            token = InvitationToken.get(key=key)
        except InvitationToken.NotFound:
            raise form.ValidationError('key_invalid', {})
        password1 = self.processed_data['password1']
        password2 = self.processed_data['password2']
        if password1 != password2:
            raise form.ValidationError('pwmatch', {})
        try:
            User.new(username=self.processed_data['username'],
                     email=self.processed_data['email'],
                     password=password1,
                     group=User.MODERATOR,
                     confirmed=True)
        except User.IntegrityError:
            raise form.ValidationError('userexists')
        token.accept()
