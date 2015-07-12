from ..util.template import view


@view('main')
def show_main():
    return dict()


def route(conf):
    return (
        ('/', 'GET', show_main, 'main', {}),
    )
