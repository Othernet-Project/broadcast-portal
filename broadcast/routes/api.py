"""
api.py: API routes reserved for superusers only

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from bottle import request, HTTPError

from ..util.broadcast import get_item, filter_items


HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_405_METHOD_NOT_ALLOWED = 405


class BaseAPI(object):

    @classmethod
    def create(cls):
        return cls()

    def to_json(self, item):
        # using getattr so that values generated in a property will be included
        return dict((key, getattr(item, key)) for key in item.keys())

    def __call__(self, *args, **kwargs):
        instance = self.create()
        try:
            handler = getattr(instance, request.method.lower())
        except AttributeError:
            raise HTTPError(HTTP_405_METHOD_NOT_ALLOWED, "Method not allowed")
        else:
            return handler(*args, **kwargs)


class BaseListAPI(BaseAPI):

    def get(self):
        results = filter_items(self.table, raw=True, **request.query)
        return {'results': results, 'count': len(results)}


class BaseDetailAPI(BaseAPI):

    def get(self, id):
        item = get_item(self.table, id=id)
        return self.to_json(item)

    def patch(self, id):
        item = get_item(self.table, id=id)
        # None is a possible incoming value, so we cannot rely on using
        # `request.json.get`
        patch_data = dict()
        for key in self.modifieable_fields:
            try:
                patch_data[key] = request.json[key]
            except KeyError:
                pass

        item.update(**patch_data)
        return self.to_json(item)


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
    return generated_routes
