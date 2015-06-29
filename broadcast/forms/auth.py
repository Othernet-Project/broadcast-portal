"""
auth.py: Authentication form

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import re

from bottle_utils import form
from bottle_utils.i18n import lazy_gettext as _

from ..util import auth


class LoginForm(form.Form):
    messages = {
        # Translators, error shown when log in attempt fails
        'invalid': _("Please enter the correct username and password."),
    }

    # Translators, used as label for a login field
    username = form.StringField(_("Username or E-mail"),
                                placeholder=_('username or e-mail'),
                                validators=[form.Required()])
    # Translators, used as label for a password field
    password = form.PasswordField(_("Password"),
                                  placeholder=_('password'),
                                  validators=[form.Required()])

    def validate(self):
        username = self.processed_data['username']
        password = self.processed_data['password']

        if not auth.login_user(username, password):
            raise form.ValidationError('invalid', {})


class TruthValidator(form.Validator):
    messages = {
        'truth': _('This field is required'),
    }

    def validate(self, value):
        if not value:
            raise form.ValidationError('truth', {})


class RegistrationForm(form.Form):
    min_password_length = 4
    messages = {
        'pwmatch': _("The entered passwords do not match."),
    }

    username = form.StringField(
        # Translators, used as label in create user form
        _("Username"),
        validators=[form.Required()],
        placeholder=_('username'),
        messages={
            'username_taken': _("Username already taken."),
        })
    email = form.StringField(
        # Translators, used as label in create user form
        _("Email"),
        validators=[form.Required()],
        placeholder=_('Email'),
        messages={
            'email_invalid': _("Invalid e-mail address entered."),
            'email_taken': _("E-mail address already registered."),
        })
    password1 = form.PasswordField(
        # Translators, used as label in create user form
        _("Password"),
        validators=[form.Required()],
        placeholder=_('password'),
        messages={
            'password_length': _('Must be longer than {length} characters.'),
        })
    password2 = form.PasswordField(
        # Translators, used as label in create user form
        _("Confirm Password"),
        validators=[form.Required()],
        placeholder=_('confirm password'))
    tos_agree = form.BooleanField(
        # Translators, used as label for terms of service agreement checkbox
        _('I agree to the <a href="%(url)s">Terms of Service</a>'),
        validators=[TruthValidator()],
        value='agree_tos',
        messages={
            'truth': _('You must agree to the terms')
        })
    priv_read = form.BooleanField(
        # Translators, used as label for privacy policy read checkbox
        _('I have read the <a href="%(url)s">Privacy Policy</a>'),
        validators=[TruthValidator()],
        value='read_tos',
        messages={
            'truth': _('You must confirm that you have read the policy')
        })

    def preprocess_password(self, value):
        if len(value) < self.min_password_length:
            raise form.ValidationError('password_length',
                                       {'length': self.min_password_length})

    def postprocess_email(self, value):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', value):
            raise form.ValidationError('email_invalid', {})

        if auth.get_user(value):
            raise form.ValidationError('email_taken', {})

        return value

    def postprocess_username(self, value):
        if auth.get_user(value):
            raise form.ValidationError('username_taken', {})

        return value

    def validate(self):
        password1 = self.processed_data['password1']
        password2 = self.processed_data['password2']
        if password1 != password2:
            raise form.ValidationError('pwmatch', {})


class ConfirmationForm(form.Form):
    # Translators, used as label in create user form
    email = form.StringField(_("E-mail"),
                             validators=[form.Required()],
                             placeholder=_('e-mail'))

    def postprocess_email(self, value):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', value):
            message = _("Invalid e-mail address entered.")
            raise form.ValidationError(message, {})

        if not auth.get_user(value):
            message = _("E-mail address not registered.")
            raise form.ValidationError(message, {})

        return value
