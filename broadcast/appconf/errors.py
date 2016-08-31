import logging

from bottle import request
from bottle_utils.ajax import roca_view
from bottle_utils.i18n import dummy_gettext as _

from ..util.template import template
from ..app.exts import container as exts


#: Maps icon name and error message to status codes
ERROR_MESSAGES = {
    400: ('question', _('No such page')),
    500: ('stop', _('Application error')),
    401: ('key', _('Log-in required')),
    403: ('key', _('Access denied')),
}

DEFAULT_ICON = 'stop'
DEFAULT_MESSAGE = _("Something's wrong")


@roca_view('errors/error.mako', 'errors/_error.mako', template_func=template)
def error_handler(resp):
    if resp.traceback:
        logging.error("Unhandled error '%s' at %s %s:\n\n%s",
                      resp.exception,
                      request.method.upper(),
                      request.path,
                      resp.traceback)
    icon, message = ERROR_MESSAGES.get(resp.status_code,
                                       (DEFAULT_ICON, DEFAULT_MESSAGE))
    return dict(err=resp, icon=icon, message=message)


def pre_init():
    app = exts.app
    app.default_error_handler = error_handler
