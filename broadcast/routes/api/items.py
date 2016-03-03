import os

from bottle import request, response, static_file, HTTPError, HTTP_CODES

from .base import (BaseAPI,
                   json_required,
                   auth_basic,
                   check_auth,
                   HTTP_400_BAD_REQUEST,
                   HTTP_404_NOT_FOUND)
from ...util.broadcast import get_item, filter_items


class ItemListAPI(BaseAPI):

    def get(self):
        results = filter_items(self.table, raw=True, **request.query)
        return {'results': results, 'count': len(results)}


class ItemDetailAPI(BaseAPI):

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
                            (ItemListAPI,),
                            {'__name__': list_api_cls_name,
                             'table': item_type})
        # generate detail api endpoint
        detail_api_cls_name = '{0}DetailAPI'.format(item_type.capitalize())
        detail_api_cls = type(detail_api_cls_name,
                              (ItemDetailAPI,),
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
