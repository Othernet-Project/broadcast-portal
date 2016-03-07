from .base import BaseAPI
from ...models.bins import Bin
from ...models.items import ContentItem


class BinListAPI(BaseAPI):
    __name__ = 'BinListAPI'

    def get(self):
        results = [b.to_native() for b in Bin.filter()]
        return {'results': results, 'count': len(results)}


class BinItemsListAPI(BaseAPI):
    __name__ = 'BinItemsListAPI'

    def get(self, id):
        results = [item.to_native() for item in ContentItem.filter(bin=id)]
        return {'results': results, 'count': len(results)}


def route(conf):
    return [
        ('/api/bins/', ['GET'], BinListAPI(), 'bin_list', {}),
        ('/api/bins/<id>/items/', ['GET'], BinItemsListAPI(), 'bin_items_list', {}),
    ]

