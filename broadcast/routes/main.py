from bottle import request

from ..util.template import view


@view('main')
def show_main():
    return dict(item_type=request.query.get('item_type', None))


def route(conf):
    return (
        ('/', 'GET', show_main, 'main', {}),
    )
