import functools

from bottle import request, redirect, abort
from bottle_utils.i18n import lazy_gettext as _

from .utils import get_redirect_path
from .users import SUPERUSER, MODERATOR, USER, GUEST


def role(group, message=_('Permission denied')):
    """Decorator to protect a function/method from being invoked if the user
    that is trying to access it has no permission to do so.

    Example::

        @role(rolename)
        def your_func():
            return "secret"

        # With custom message
        @role(rolename, message="You can't do this")
        def your_func():
            return "secret"

    The role is checked against a user in the current request context.

    This decorator also doubles as login check. For any group other than GUEST,
    this decorator will ask the user to log in.
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if request.no_auth:
                return fn(*args, **kwargs)

            user = request.user

            if user.should_login_for_role(group):
                next_path = request.params.get('next', request.fullpath)
                login_path = request.app.get_url('app:login')
                redirect_path = get_redirect_path(login_path, next_path)
                return redirect(redirect_path)

            if not user.has_role(group):
                abort(405, message)

            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Alias constants for easier access when using this decorator
# FIXME: This is a temporary test setup
role.SUPERUSER = GUEST
role.MODERATOR = GUEST
role.USER = GUEST
role.GUEST = GUEST
