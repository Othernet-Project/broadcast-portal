from ..util.template import view


@view('main')
def show_main():
    return {}


def route(conf):
    return (
        ('/', 'GET', show_main, 'main', {}),
    )
