from bottle import request

from ..models.bins import Bin
from ..util.template import view


@view('main')
def show_main():
    current_bin = Bin.current()
    return dict(bin=current_bin,
                item_type=request.query.get('item_type', None))


@view('rocket_service')
def show_rocket_service():
    return dict()


def route(conf):
    return (
        ('/', 'GET', show_main, 'main', {}),
        ('/rocket/', 'GET', show_rocket_service, 'rocket_service', {}),
    )
