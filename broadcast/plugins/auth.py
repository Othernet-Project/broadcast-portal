import functools

from bottle import request

from ..app.exts import container as exts
from ..models.auth import User, AnonymousUser


def user_plugin():
    conf = exts.config
    no_auth = conf['session.no_auth']

    # Set up a hook, so handlers that raise cannot escape session-saving
    @exts.app.hook('after_request')
    def process_options():
        if not hasattr(request, 'session'):
            return
        if hasattr(request, 'user') and not request.user.is_guest:
            request.session['user'] = request.user.to_json()

    def plugin(callback):
        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            if hasattr(request, 'session'):
                request.no_auth = no_auth
                user_data = request.session.get('user')
                if user_data:
                    request.user = User.from_json(user_data)
                else:
                    request.user = AnonymousUser()
            return callback(*args, **kwargs)

        return wrapper
    plugin.name = 'user'
    return plugin
