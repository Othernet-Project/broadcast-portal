from bottle import redirect, request


def show_main():
    redirect(request.app.get_url('broadcast_content_form', item_type='content'))


def route(conf):
    return (
        ('/', 'GET', show_main, 'main', {}),
    )
