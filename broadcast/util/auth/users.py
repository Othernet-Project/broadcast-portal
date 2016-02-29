"""
auth.py: User authentication and authorization

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import datetime
import sqlite3

import pbkdf2
from bottle import request

from .base import DBDataWrapper
from .groups import Group
from .permissions import BasePermission
from .utils import is_string, from_csv, to_list


class User(DBDataWrapper):

    class Error(Exception):
        pass

    class DoesNotExist(Error):
        pass

    class AlreadyExists(Error):
        pass

    class InvalidCredentials(Error):
        pass

    _table = 'users'
    _columns = (
        'email',
        'username',
        'password',
        'created',
        'confirmed',
        'data',
        'groups',
    )

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._groups = [Group.from_name(name, db=self._db)
                        for name in from_csv(self.groups)]

    def get_permission_kwargs(self):
        """Returns the keyword arguments for instantiating the permission."""
        return dict()

    def has_permission(self, permission_class, *args, **kwargs):
        if is_string(permission_class):
            permission_class = BasePermission.cast(permission_class)

        for group in self._groups:
            if group.has_superpowers:
                return True

            if group.contains_permission(permission_class):
                permission = permission_class(**self.get_permission_kwargs())
                return permission.is_granted(*args, **kwargs)

        return False

    @to_list
    def is_in_group(self, groups):
        member_of = [group.name for group in self._groups]
        return all([name in member_of for name in groups])

    @property
    def is_authenticated(self):
        return self.email is not None

    @property
    def is_superuser(self):
        return any([group.has_superpowers for group in self._groups])

    @property
    def is_anonymous(self):
        return self.email and self.username is None

    @property
    def is_confirmed(self):
        return self.confirmed is not None

    def logout(self):
        if self.is_authenticated:
            request.session.delete().reset()
            request.user = User()

    def make_logged_in(self):
        request.user = self
        request.session.rotate()
        return self

    def update(self, **kwargs):
        if any([key not in self._columns for key in kwargs]):
            raise ValueError("Unknown columns detected.")

        placeholders = dict((name, ':{}'.format(name))
                            for name in kwargs.keys())
        query = self._db.Update(self._table,
                                where='email = :email',
                                **placeholders)
        self._db.query(query, email=self.email, **kwargs)
        self._data.update(kwargs)
        return self

    def set_password(self, new_password):
        self.update(password=self.encrypt_password(new_password))
        return self

    def confirm(self):
        self.update(confirmed=datetime.datetime.now())
        return self

    @classmethod
    def get(cls, username_or_email, db=None):
        db = db or request.db.sessions
        query = db.Select(sets=cls._table,
                          where='username = :username OR email = :email')
        db.query(query,
                 username=username_or_email,
                 email=username_or_email)
        raw_data = db.result
        if not raw_data:
            raise cls.DoesNotExist()

        return cls(raw_data, db=db)

    @classmethod
    def create(cls, email, username=None, password=None, is_superuser=False,
               confirmed=None, overwrite=False, db=None):
        db = db or request.db.sessions
        password = cls.encrypt_password(password) if password else None
        data = {'username': username,
                'password': password,
                'email': email,
                'created': datetime.datetime.utcnow(),
                'groups': 'superuser' if is_superuser else '',
                'confirmed': confirmed}
        statement_cls = db.Replace if overwrite else db.Insert
        query = statement_cls(cls._table, cols=('username',
                                                'password',
                                                'email',
                                                'created',
                                                'groups',
                                                'confirmed'))
        try:
            db.execute(query, data)
        except sqlite3.IntegrityError:
            raise cls.AlreadyExists()
        else:
            return cls(data, db=db)

    @classmethod
    def login(cls, username_or_email, password=None, verify=True, db=None):
        """Makes the user of the passed in username or email logged in, with
        optional security verification."""
        user = cls.get(username_or_email, db=db)
        if verify and not cls.is_valid_password(password, user.password):
            raise cls.InvalidCredentials()

        return user.make_logged_in()

    @staticmethod
    def encrypt_password(password):
        return pbkdf2.crypt(password)

    @staticmethod
    def is_valid_password(password, encrypted_password):
        return encrypted_password == pbkdf2.crypt(password, encrypted_password)

