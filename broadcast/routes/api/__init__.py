from .bins import route as bin_routes
from .items import route as item_routes


def route(conf):
    return item_routes(conf) + bin_routes(conf)

