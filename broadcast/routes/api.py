"""
api.py: API routes reserved for superusers only

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from bottle import request, HTTPError

from ..util.broadcast import get_item, filter_items


class BaseAPI(object):

    @classmethod
    def create(cls):
        return cls()

    def __call__(self, *args, **kwargs):
        instance = self.create()
        try:
            handler = getattr(instance, request.method.lower())
        except AttributeError:
            raise HTTPError(405, "Method not allowed")
        else:
            return handler(*args, **kwargs)


class BaseListAPI(BaseAPI):

    def get(self):
        results = filter_items(self.table, raw=True, **request.query)
        return {'results': results, 'count': len(results)}


class BaseDetailAPI(BaseAPI):

    def get(self, id):
        return get_item(self.table, raw=True, id=id)


def route(conf):
    generated_routes = []
    for item_type in conf['app.broadcast_types']:
        # generate list api endpoint
        list_api_cls_name = '{0}ListAPI'.format(item_type.capitalize())
        list_api_cls = type(list_api_cls_name,
                            (BaseListAPI,),
                            {'__name__': list_api_cls_name,
                             'table': item_type, })
        # generate detail api endpoint
        detail_api_cls_name = '{0}DetailAPI'.format(item_type.capitalize())
        detail_api_cls = type(detail_api_cls_name,
                              (BaseDetailAPI,),
                              {'__name__': list_api_cls_name,
                               'table': item_type, })
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
    return generated_routes
