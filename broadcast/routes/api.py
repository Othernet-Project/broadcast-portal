"""
api.py: API routes reserved for superusers only

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import functools
import os

from bottle import (request,
                    response,
                    auth_basic,
                    static_file,
                    HTTPError,
                    HTTP_CODES)

from ..util.auth import User
from ..util.broadcast import get_item, filter_items


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

    def to_json(self, obj):
        # using getattr so that values generated in a property will be included
        return dict((key, getattr(obj, key)) for key in obj.keys())

    @auth_basic(check_auth)
    def __call__(self, *args, **kwargs):
        instance = self.create()
        try:
            handler = getattr(instance, request.method.lower())
        except AttributeError:
            self.error(HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return handler(*args, **kwargs)


class BaseListAPI(BaseAPI):

    def get(self):
        results = filter_items(self.table, raw=True, **request.query)
        return {'results': results, 'count': len(results)}


class BaseDetailAPI(BaseAPI):

    def get_object(self, id):
        obj = get_item(self.table, id=id)
        if obj is None:
            self.error(HTTP_404_NOT_FOUND)
        return obj

    def get(self, id):
        obj = self.get_object(id)
        return self.to_json(obj)

    @json_required
    def patch(self, id):
        obj = get_item(self.table, id=id)
        # None is a possible incoming value, so we cannot rely on using
        # `request.json.get`
        patch_data = dict()
        for key in obj.modifieable_fields:
            try:
                patch_data[key] = request.json[key]
            except KeyError:
                pass

        try:
            obj.update(**patch_data)
        except ValueError as exc:
            response.status = HTTP_400_BAD_REQUEST
            return {'error': str(exc)}
        else:
            return self.to_json(obj)


@auth_basic(check_auth)
def download_content_file(id):
    obj = get_item('content', id=id)
    if obj is None:
        raise HTTPError(HTTP_404_NOT_FOUND, HTTP_CODES[HTTP_404_NOT_FOUND])

    return static_file(obj.file_path,
                       root=request.app.config['content.upload_root'],
                       download=os.path.basename(obj.file_path))


def route(conf):
    generated_routes = []
    for item_type in conf['app.broadcast_types']:
        # generate list api endpoint
        list_api_cls_name = '{0}ListAPI'.format(item_type.capitalize())
        list_api_cls = type(list_api_cls_name,
                            (BaseListAPI,),
                            {'__name__': list_api_cls_name,
                             'table': item_type})
        # generate detail api endpoint
        detail_api_cls_name = '{0}DetailAPI'.format(item_type.capitalize())
        detail_api_cls = type(detail_api_cls_name,
                              (BaseDetailAPI,),
                              {'__name__': list_api_cls_name,
                               'table': item_type})
        # add routes to api endpoints
        generated_routes.extend([(
            '/api/{0}/'.format(item_type),
            ['GET', 'POST'],
            list_api_cls(),
            '{0}_list'.format(item_type),
            {}
        ), (
            '/api/{0}/<id>'.format(item_type),
            ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
            detail_api_cls(),
            '{0}_detail'.format(item_type),
            {}
        )])

    generated_routes.append((
        '/api/content/<id>/file/',
        ['GET'],
        download_content_file,
        'download_content_file',
        {}
    ))
    return generated_routes
