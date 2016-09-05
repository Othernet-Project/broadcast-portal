import logging

from bottle import request
from streamline import after, before


def pre_init():
    @before
    def init_user(route):
        from ..models.auth import User, AnonymousUser
        if 'auth' in (route.exclude_plugins or []):
            logging.debug('Auth disabled')
            return
        if not hasattr(request, 'session'):
            return
        user_data = request.session.get('user')
        if user_data:
            request.user = User.from_json(user_data)
        else:
            request.user = AnonymousUser()

    @after
    def store_user(route):
        if hasattr(request, 'user') and not request.user.is_guest:
            request.session['user'] = request.user.to_json()
