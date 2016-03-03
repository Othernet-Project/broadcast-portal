from .base import BaseAPI
from ...util.bins import Bin
from ...util.broadcast import filter_items, ContentItem


class BinListAPI(BaseAPI):
    __name__ = 'BinListAPI'

    def get(self):
        results = [b.to_native() for b in Bin.list()]
        return {'results': results, 'count': len(results)}


class BinItemsListAPI(BaseAPI):
    __name__ = 'BinItemsListAPI'

    def get(self, id):
        results = filter_items(ContentItem.type, bin=id, raw=True)
        return {'results': results, 'count': len(results)}


def route(conf):
    return [
        ('/api/bin/', ['GET'], BinListAPI(), 'bin_list', {}),
        ('/api/bin/<id>/items/', ['GET'], BinItemsListAPI(), 'bin_items_list', {}),
    ]

