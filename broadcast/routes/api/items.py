import os

from bottle import request, response, static_file, HTTPError, HTTP_CODES

from .base import (BaseAPI,
                   json_required,
                   auth_basic,
                   check_auth,
                   HTTP_400_BAD_REQUEST,
                   HTTP_404_NOT_FOUND)
from ...models.items import BaseItem


class ItemListAPI(BaseAPI):

    def get(self):
        item_cls = BaseItem.cast(self.table)
        results = [item.to_native()
                   for item in item_cls.filter(**request.query)]
        return {'results': results, 'count': len(results)}


class ItemDetailAPI(BaseAPI):

    def get_object(self, id):
        item_cls = BaseItem.cast(self.table)
        try:
            return item_cls.get(id=id)
        except item_cls.DoesNotExist:
            self.error(HTTP_404_NOT_FOUND)

    def get(self, id):
        obj = self.get_object(id)
        return obj.to_native()

    @json_required
    def patch(self, id):
        obj = self.get_object(id)
        # None is a possible incoming value, so we cannot rely on using
        # `request.json.get`
        patch_data = dict()
        for key in self.modifieable_fields:
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
    ContentItem = BaseItem.cast('content')
    try:
        obj = ContentItem.get(id=id)
    except ContentItem.DoesNotExist:
        raise HTTPError(HTTP_404_NOT_FOUND, HTTP_CODES[HTTP_404_NOT_FOUND])
    else:
        return static_file(obj.path,
                           root=request.app.config['content.upload_root'],
                           download=os.path.basename(obj.path))


def route(conf):
    generated_routes = []
    modifiable_fields = ['status']
    for item_type in conf['app.broadcast_types']:
        # generate list api endpoint
        list_api_cls_name = '{0}ListAPI'.format(item_type.capitalize())
        list_api_cls = type(list_api_cls_name,
                            (ItemListAPI,),
                            {'__name__': list_api_cls_name,
                             'table': item_type,
                             'modifiable_fields': modifiable_fields})
        # generate detail api endpoint
        detail_api_cls_name = '{0}DetailAPI'.format(item_type.capitalize())
        detail_api_cls = type(detail_api_cls_name,
                              (ItemDetailAPI,),
                              {'__name__': list_api_cls_name,
                               'table': item_type,
                               'modifiable_fields': modifiable_fields})
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
