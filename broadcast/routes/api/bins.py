from .base import BaseAPI
from ...util.bins import Bin


class BinListAPI(BaseAPI):
    __name__ = 'BinListAPI'

    def get(self):
        results = [b.to_json() for b in Bin.list()]
        return {'results': results, 'count': len(results)}


def route(conf):
    return [
        ('/api/bin/', ['GET'], BinListAPI(), 'bin_list', {}),
    ]

