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

from .options import Options


class UserAlreadyExists(Exception):
    pass


class InvalidUserCredentials(Exception):
    pass


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

    def __init__(self, username=None, email=None, is_superuser=None,
                 confirmed=None, created=None, options=None):
        self.username = username
        self.email = email
        self.is_superuser = is_superuser
        self.confirmed = confirmed
        self.created = created
        self.options = Options(options, onchange=self.save_options)

    @property
    def is_authenticated(self):
        return self.username is not None

    def save_options(self):
        if self.is_authenticated:
            db = request.db.sessions
            options = self.options.to_json()
            query = db.Update('users',
                              options=':options',
                              where='username = :username')
            db.query(query, username=self.username, options=options)

    def logout(self):
        if self.is_authenticated:
            request.session.delete().reset()
            request.user = User()

    def to_json(self):
        data = dict(username=self.username,
                    email=self.email,
                    is_superuser=self.is_superuser,
                    confirmed=self.confirmed,
                    created=self.created,
                    options=self.options.to_native())
        return json.dumps(data, cls=DateTimeEncoder)

    @classmethod
    def from_json(cls, data):
        return cls(**json.loads(data, cls=DateTimeDecoder))


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


def encrypt_password(password):
    return pbkdf2.crypt(password)


def is_valid_password(password, encrypted_password):
    return encrypted_password == pbkdf2.crypt(password, encrypted_password)


def create_user(username, password, email, is_superuser=False,
                confirmed=None, db=None, overwrite=False):
    if not username or not email or not password:
        raise InvalidUserCredentials()

    encrypted = encrypt_password(password)

    user_data = {'username': username,
                 'password': encrypted,
                 'email': email,
                 'created': datetime.datetime.utcnow(),
                 'is_superuser': is_superuser,
                 'confirmed': confirmed}

    db = db or request.db.sessions
    sql_cmd = db.Replace if overwrite else db.Insert
    query = sql_cmd('users', cols=('username',
                                   'password',
                                   'email',
                                   'created',
                                   'is_superuser',
                                   'confirmed'))
    try:
        db.execute(query, user_data)
    except sqlite3.IntegrityError:
        raise UserAlreadyExists()


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

    query = db.Update('users',
                      confirmed=':confirmed',
                      where='email = :email')
    db.query(query, confirmed=now, email=confirmation.email)
    delete_temporary_key(key, db=db)
    return confirmation.email


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
    encrypted_password = encrypt_password(new_password)
    db.query(query, password=encrypted_password, email=email)


def get_user(username_or_email):
    db = request.db.sessions
    query = db.Select(sets='users',
                      where='username = :username OR email = :email')
    db.query(query, username=username_or_email, email=username_or_email)
    return db.result


def login_user_no_auth(username_or_email):
    """Makes the user of the passed in username or email logged in, with no
    security verification whatsoever."""
    user = get_user(username_or_email)
    if user:
        request.user = User(username=user.username,
                            email=user.email,
                            is_superuser=user.is_superuser,
                            confirmed=user.confirmed,
                            created=user.created,
                            options=user.options)
        request.session.rotate()


def login_user(username_or_email, password):
    user = get_user(username_or_email)
    if user and is_valid_password(password, user.password):
        request.user = User(username=user.username,
                            email=user.email,
                            is_superuser=user.is_superuser,
                            confirmed=user.confirmed,
                            created=user.created,
                            options=user.options)
        request.session.rotate()
        return True

    return False


def user_plugin(conf):
    no_auth = conf['session.no_auth']
    bottle = conf['bottle']
    # Set up a hook, so handlers that raise cannot escape session-saving

    @bottle.hook('after_request')
    def process_options():
        if hasattr(request, 'session') and hasattr(request, 'user'):
            request.user.options.apply()
            request.session['user'] = request.user.to_json()

    def plugin(callback):
        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            request.no_auth = no_auth
            user_data = request.session.get('user', '{}')
            request.user = User.from_json(user_data)
            return callback(*args, **kwargs)

        return wrapper
    plugin.name = 'user'
    return plugin
