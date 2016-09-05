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
            request.user = AnonymousUser()
            logging.debug('Sessions, using anonymous user')
            return
        user_data = request.session.get('user')
        if user_data:
            request.user = User.from_json(user_data)
            logging.debug('Created user from session data: %s',
                          request.user.username)
        else:
            request.user = AnonymousUser()
            logging.debug('Using anonymous user')

    @after
    def store_user(route):
        if hasattr(request, 'user') and not request.user.is_guest:
            logging.debug('Storing user data in the session')
            request.session['user'] = request.user.to_json()
