import functools

from bottle import request

from .users import User


def user_plugin(conf):
    no_auth = conf['session.no_auth']
    bottle = conf['bottle']
    # Set up a hook, so handlers that raise cannot escape session-saving

    @bottle.hook('after_request')
    def process_options():
        if hasattr(request, 'session') and hasattr(request, 'user'):
            request.session['user'] = request.user.to_json()

    def plugin(callback):
        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            request.no_auth = no_auth
            user_data = request.session.get('user', '{}')
            request.user = User.from_json(user_data, db=request.db.sessions)
            return callback(*args, **kwargs)

        return wrapper
    plugin.name = 'user'
    return plugin

