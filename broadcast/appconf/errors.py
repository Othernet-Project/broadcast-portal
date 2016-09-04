import logging

from streamline import XHRPartialRoute
from bottle_utils.i18n import dummy_gettext as _

from ..app.exts import container as exts


#: Maps icon name and error message to status codes
ERROR_MESSAGES = {
    404: ('question', _('No such page')),
    500: ('stop', _('Application error')),
    401: ('key', _('Log-in required')),
    403: ('key', _('Access denied')),
}

DEFAULT_ICON = 'stop'
DEFAULT_MESSAGE = _("Something's wrong")


class ErrorHandler(XHRPartialRoute):
    template_name = 'errors/error.mako'
    partial_template_name = 'errors/_error.mako'

    def get_method(self):
        return 'any'

    def any(self, resp):
        try:
            print(self.request.session)
        except AttributeError:
            print('no session')
        if resp.traceback:
            logging.error("Unhandled error '%s' at %s %s:\n\n%s",
                          resp.exception,
                          self.request.method.upper(),
                          self.request.path,
                          resp.traceback)
        icon, message = ERROR_MESSAGES.get(resp.status_code,
                                           (DEFAULT_ICON, DEFAULT_MESSAGE))
        return dict(err=resp, icon=icon, message=message)


def pre_init():
    app = exts.app
    app.default_error_handler = ErrorHandler
