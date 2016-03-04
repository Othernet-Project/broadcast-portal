"""
api.py: API routes reserved for superusers only

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import functools

from bottle import (request,
                    response,
                    auth_basic,
                    HTTPError,
                    HTTP_CODES)

from ...util.auth.users import User


HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405


def check_auth(username, password):
    try:
        user = User.login(username, password)
    except (User.DoesNotExist, User.InvalidCredentials):
        return False
    else:
        return user.is_superuser


def json_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if request.json is None:
            response.status = HTTP_400_BAD_REQUEST
            return {'error': 'No JSON data found.'}
        return func(*args, **kwargs)
    return wrapper


class BaseAPI(object):

    @classmethod
    def create(cls):
        return cls()

    def error(self, status_code):
        raise HTTPError(status_code, HTTP_CODES[status_code])

    @auth_basic(check_auth)
    def __call__(self, *args, **kwargs):
        instance = self.create()
        try:
            handler = getattr(instance, request.method.lower())
        except AttributeError:
            self.error(HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return handler(*args, **kwargs)

