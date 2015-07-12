from bottle import request, redirect


def show_main():
    broadcast_url = request.app.get_url('broadcast_content_form',
                                        item_type='content')
    redirect(broadcast_url)


def route(conf):
    return (
        ('/', 'GET', show_main, 'main', {}),
    )
