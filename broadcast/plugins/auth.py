import functools

from bottle import request
from streamline import after

from ..app.exts import container as exts
from ..models.auth import User, AnonymousUser


def user_plugin():
    conf = exts.config
    no_auth = conf['session.no_auth']

    @after
    def store_user(*args):
        if hasattr(request, 'user') and not request.user.is_guest:
            request.session['user'] = request.user.to_json()

    def plugin(callback):
        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            if not hasattr(request, 'session'):
                return callback(*args, **kwargs)

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
