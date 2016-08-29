"""
auth.py: User authentication and authorization

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import uuid
import datetime

import pbkdf2
from bottle import request
from bottle_utils.i18n import dummy_gettext as _

from . import Model
from ..util.helpers import utcnow
from ..util.sendmail import send_mail


SUPERUSER = 'superuser'
MODERATOR = 'moderator'
USER = 'user'
GUEST = 'guest'
GROUPS = {
    SUPERUSER,
    MODERATOR,
    USER,
    GUEST,
}
LOGIN_GROUPS = {
    SUPERUSER,
    MODERATOR,
    USER,
}
ROLE_LEVELS = {
    SUPERUSER: 1000,
    MODERATOR: 100,
    USER: 10,
    GUEST: 1
}


class UserBase(object):
    SUPERUSER = SUPERUSER
    MODERATOR = MODERATOR
    USER = USER
    GUEST = GUEST
    GROUPS = GROUPS
    LOGIN_GROUPS = LOGIN_GROUPS

    @property
    def is_authenticated(self):
        return self.email is not None

    @property
    def is_guest(self):
        return self.group == GUEST

    @property
    def is_superuser(self):
        return self.group == SUPERUSER

    @property
    def is_confirmed(self):
        return self.confirmed is not None

    @property
    def role_level(self):
        return ROLE_LEVELS[self.group]

    def has_role(self, group, strict=False):
        if strict:
            return self.group == group or self.group == SUPERUSER
        group_level = ROLE_LEVELS[group]
        return self.role_level >= group_level

    def should_login_for_role(self, group):
        """
        This method returns True if the account reuquires a log-in to consume
        resources at given group's role level. If user is already
        authenticated, this method always returns ``False``. This check is
        distinct from role-level check.
        """
        if self.is_authenticated:
            return False
        return group != GUEST


class AnonymousUser(UserBase):
    def __init__(self, *args, **kwargs):
        self.email = None
        self.username = 'anonymous'
        self.password = None
        self.created = None
        self.confirmed = False
        self.data = None
        self.group = GUEST


class User(UserBase, Model):
    class AlreadyExists(Model.Error):
        pass

    class InvalidCredentials(Model.Error):
        pass

    dbname = 'sessions'
    table = 'users'
    columns = (
        'id',
        'email',
        'username',
        'password',
        'created',
        'confirmed',
        'data',
        'groupname',
    )
    pk = 'id'

    def logout(self):
        if self.is_authenticated:
            request.session.delete().reset()
            request.user = AnonymousUser()

    def make_logged_in(self):
        request.user = self
        request.session.rotate()
        return self

    def set_password(self, new_password):
        self.password = self.encrypt_password(new_password)
        return self

    def confirm(self, cursor=None):
        self.confirmed = utcnow()
        return self

    @property
    def group(self):
        return self.groupname

    @classmethod
    def new(cls, username, email, password, group=USER, confirmed=False,
            overwrite=False):
        user = User({
            'username': username,
            'email': email,
            'groupname': group,
            'created': utcnow(),
        })
        user.set_password(password)
        if confirmed:
            user.confirm()
        user.save(force_replace=overwrite)
        return User.get(username=username, email=email)

    @classmethod
    def login(cls, username_or_email, password=None, verify=True, db=None):
        """Makes the user of the passed in username or email logged in, with
        optional security verification."""
        try:
            user = cls.get(email=username_or_email, db=db)
        except cls.DoesNotExist:
            # if it's not found by username either, raise freely
            user = cls.get(username=username_or_email, db=db)

        if verify and not cls.is_valid_password(password, user.password):
            raise cls.InvalidCredentials()

        return user.make_logged_in()

    @staticmethod
    def encrypt_password(password):
        return pbkdf2.crypt(password)

    @staticmethod
    def is_valid_password(password, encrypted_password):
        return encrypted_password == pbkdf2.crypt(password, encrypted_password)


class BaseToken(Model):
    dbname = 'sessions'
    table = 'tokens'
    columns = (
        'key',
        'email',
        'expires',
    )
    pk = 'key'

    class KeyExpired(Model.Error):
        pass

    def __init__(self, *args, **kwargs):
        super(BaseToken, self).__init__(*args, **kwargs)
        if self.has_expired:
            self.delete()
            raise self.KeyExpired()

    @property
    def has_expired(self):
        return self.expires < utcnow()

    def accept(self):
        self.delete()

    @staticmethod
    def generate_key():
        return uuid.uuid4().hex

    @classmethod
    def clear_expired(cls, cursor=None):
        cursor = cursor or cls.db.cursor()
        q = cls.db.Delete(cls.table, where='expires <= :now')
        cursor.query(q, now=utcnow())

    @classmethod
    def new(cls, email, expiration, cursor=None):
        expires = utcnow() + datetime.timedelta(days=expiration)
        token = cls({
            'email': email,
            'expires': expires,
        })
        token.save(pk=cls.generate_key(), cursor=cursor)
        return token

    def send(self, next_path=None):
        email_ctx = {
            'key': self.key,
            'next_path': next_path,
        }
        send_mail(to=self.email,
                  subject=self.email_subject,
                  template=self.email_template,
                  data=email_ctx)


class EmailVerificationToken(BaseToken):
    email_subject = _("Confirm your email")
    email_template = 'email/confirm.mako'

    def accept(self):
        user = User.get(email=self.email)
        user.confirm().make_logged_in()
        super(EmailVerificationToken, self).accept()
        return user


class PasswordResetToken(BaseToken):
    email_subject = _("Password reset request")
    email_template = 'email/confirm.mako'

    def accept(self, new_password):
        user = User.get(email=self.email)
        user.set_password(new_password)
        super(PasswordResetToken, self).accept()
        return user


class InvitationToken(BaseToken):
    email_subject = _('You are invited to join the Outernet Filecast Center')
    email_template = 'email/invite.mako'
