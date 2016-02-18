"""
auth.py: User authentication and authorization

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import datetime
import functools
import json
import sqlite3
import urllib
import urlparse
import uuid

import pbkdf2
from bottle import request, abort, redirect
from bottle_utils.i18n import dummy_gettext as _

from ..util.sendmail import send_mail


class KeyNotFound(Exception):
    pass


class KeyExpired(Exception):
    pass


class DateTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        return super(DateTimeEncoder, self).default(obj)


class DateTimeDecoder(json.JSONDecoder):

    def __init__(self, *args, **kargs):
        super(DateTimeDecoder, self).__init__(object_hook=self.object_hook,
                                              *args,
                                              **kargs)

    def object_hook(self, obj):
        if '__type__' not in obj:
            return obj

        obj_type = obj.pop('__type__')
        try:
            return datetime(**obj)
        except Exception:
            obj['__type__'] = obj_type
            return obj


class User(object):

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
        'is_superuser',
        'created',
        'confirmed',
        'options',
    )

    def __init__(self, data=None, db=None):
        self._db = db or request.db.sessions
        # if user logs out, an empty user object is needed
        if not data:
            data = dict((k, None) for k in self._columns)
        # data must be json-serializable, make sure it is
        if not isinstance(data, dict):
            data = dict((k, data[k]) for k in data.keys())

        self._data = data

    def __getattr__(self, name):
        if name in self._columns:
            return self._data.get(name, None)
        raise AttributeError(name)

    @property
    def is_authenticated(self):
        return self.email is not None

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

    def to_json(self):
        return json.dumps(self._data, cls=DateTimeEncoder)

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

    @classmethod
    def from_json(cls, data, db=None):
        return cls(json.loads(data, cls=DateTimeDecoder), db=db)

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
                'is_superuser': is_superuser,
                'confirmed': confirmed}
        statement_cls = db.Replace if overwrite else db.Insert
        query = statement_cls(cls._table, cols=('username',
                                                'password',
                                                'email',
                                                'created',
                                                'is_superuser',
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


def get_redirect_path(base_path, next_path, next_param_name='next'):
    QUERY_PARAM_IDX = 4

    next_encoded = urllib.urlencode({next_param_name: next_path})

    parsed = urlparse.urlparse(base_path)
    new_path = list(parsed)

    if parsed.query:
        new_path[QUERY_PARAM_IDX] = '&'.join([new_path[QUERY_PARAM_IDX],
                                              next_encoded])
    else:
        new_path[QUERY_PARAM_IDX] = next_encoded

    return urlparse.urlunparse(new_path)


def login_required(redirect_to='/login/', superuser_only=False, next_to=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if request.no_auth:
                return func(*args, **kwargs)

            if next_to is None:
                next_path = request.fullpath
                if request.query_string:
                    next_path = '?'.join([request.fullpath,
                                          request.query_string])
            else:
                next_path = next_to

            if request.user.is_authenticated:
                is_superuser = request.user.is_superuser
                if not superuser_only or (superuser_only and is_superuser):
                    return func(*args, **kwargs)
                return abort(403)

            redirect_path = get_redirect_path(redirect_to, next_path)
            return redirect(redirect_path)
        return wrapper
    return decorator


def create_temporary_key(email, expiration, db=None):
    key = uuid.uuid4().hex
    expires = datetime.datetime.utcnow() + datetime.timedelta(days=expiration)
    data = {'key': key,
            'email': email,
            'expires': expires}
    db = db or request.db.sessions
    query = db.Insert('confirmations', cols=('key', 'email', 'expires'))
    db.execute(query, data)
    return key


def delete_temporary_key(key, db=None):
    db = db or request.db.sessions
    db.query(db.Delete('confirmations', where='key = :key'), key=key)


def send_confirmation_email(email, next_path, config=None, db=None):
    config = config or request.app.config
    expiration = config['authentication.confirmation_expires']
    confirmation_key = create_temporary_key(email, expiration, db=db)
    task_runner = config['task.runner']
    task_runner.schedule(send_mail,
                         email,
                         _("Confirm registration"),
                         text='email/confirm',
                         data={'confirmation_key': confirmation_key,
                               'next_path': next_path},
                         config=config)


def confirm_user(key, db=None):
    db = db or request.db.sessions
    query = db.Select(sets='confirmations', where='key = :key')
    db.execute(query, dict(key=key))
    confirmation = db.result
    if not confirmation:
        raise KeyNotFound()

    now = datetime.datetime.utcnow()
    if confirmation.expires < now:
        delete_temporary_key(key, db=db)
        raise KeyExpired()

    user = User.get(confirmation.email)
    user.update(confirmed=now)
    user.make_logged_in()
    delete_temporary_key(key, db=db)
    return user


def verify_temporary_key(key, db=None):
    db = db or request.db.sessions
    query = db.Select(sets='confirmations', where='key = :key')
    db.execute(query, dict(key=key))
    temp_key = db.result
    if not temp_key:
        raise KeyNotFound()

    now = datetime.datetime.utcnow()
    if temp_key.expires < now:
        delete_temporary_key(key, db=db)
        raise KeyExpired()


def reset_password(key, new_password, db=None):
    db = db or request.db.sessions
    query = db.Select(sets='confirmations', where='key = :key')
    db.execute(query, dict(key=key))
    temp_key = db.result
    change_password(temp_key.email, new_password, db=db)
    delete_temporary_key(key, db=db)


def change_password(email, new_password, db=None):
    db = db or request.db.sessions
    query = db.Update('users',
                      password=':password',
                      where='email = :email')
    encrypted_password = User.encrypt_password(new_password)
    db.query(query, password=encrypted_password, email=email)


def user_plugin(conf):
    no_auth = conf['session.no_auth']
    bottle = conf['bottle']
    # Set up a hook, so handlers that raise cannot escape session-saving

    @bottle.hook('after_request')
    def process_options():
        if hasattr(request, 'session') and hasattr(request, 'user'):
            request.session['user'] = request.user.to_json()

    def plugin(callback):
        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            request.no_auth = no_auth
            user_data = request.session.get('user', '{}')
            request.user = User.from_json(user_data, db=request.db.sessions)
            return callback(*args, **kwargs)

        return wrapper
    plugin.name = 'user'
    return plugin
