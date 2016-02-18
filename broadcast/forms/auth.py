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
            auth.User.login(username, password)
        except auth.User.InvalidCredentials:
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
        placeholder=_('Username'),
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
        placeholder=_('Password'),
        messages={
            'password_length': _('Must be longer than {length} characters.'),
        })
    password2 = form.PasswordField(
        # Translators, used as label in create user form
        _("Confirm Password"),
        validators=[form.Required()],
        placeholder=_('Retype the password'))
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

        try:
            user = auth.User.get(value)
        except auth.User.DoesNotExist:
            pass  # good, email is free
        else:
            if not user.is_anonymous:
                raise form.ValidationError('email_taken', {})

        return value

    def postprocess_username(self, value):
        try:
            auth.User.get(value)
        except auth.User.DoesNotExist:
            return value  # good, username is free
        else:
            raise form.ValidationError('username_taken', {})

    def validate(self):
        password1 = self.processed_data['password1']
        password2 = self.processed_data['password2']
        if password1 != password2:
            raise form.ValidationError('pwmatch', {})


class ConfirmationForm(form.Form):
    # Translators, used as label in create user form
    email = form.StringField(
        _("Email"),
        validators=[form.Required()],
        placeholder=_('Email'),
        messages={
            # Translators, used as error messages for invalid email addresses
            # in send email confirmation form
            'invalid_email': _("Invalid e-mail address entered."),
            'not_registered': _("E-mail address not registered.")
        }
    )

    def postprocess_email(self, value):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', value):
            raise form.ValidationError('invalid_email', {})

        try:
            auth.User.get(value)
        except auth.User.DoesNotExist:
            raise form.ValidationError('not_registered', {})
        else:
            return value


class PasswordResetRequestForm(form.Form):
    messages = {
        'invalid_email': _("Invalid e-mail address entered."),
    }
    # Translators, used as label in create user form
    email = form.StringField(
        _("Email"),
        validators=[form.Required()],
        placeholder=_('Email'),
        messages={
            # Translators, used as error messages for invalid email addresses
            # in password reset form
            'invalid_email': _("Invalid e-mail address entered."),
        }
    )

    def postprocess_email(self, value):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', value):
            raise form.ValidationError('invalid_email', {})

        return value


class PasswordResetForm(form.Form):
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
        _("Confirm bew password"),
        validators=[form.Required()],
        placeholder=_('Password'),
        messages={
            'password_length': _('Must be longer than {length} characters.'),
        }
    )

    def validate(self):
        key = self.processed_data['key']
        try:
            auth.verify_temporary_key(key)
        except auth.KeyExpired:
            raise form.ValidationError('key_expired', {})
        except auth.KeyNotFound:
            raise form.ValidationError('key_invalid', {})

        new_password1 = self.processed_data['new_password1']
        new_password2 = self.processed_data['new_password2']
        if new_password1 != new_password2:
            raise form.ValidationError('pwmatch', {})
