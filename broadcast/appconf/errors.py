import logging

from bottle import request
from bottle_utils.ajax import roca_view

from ..util.template import template
from ..app.exts import container as exts


@roca_view('errors/error.mako', 'errors/_error.mako', template_func=template)
def error_handler(resp):
    if resp.traceback:
        logging.error("Unhandled error '%s' at %s %s:\n\n%s",
                      resp.exception,
                      request.method.upper(),
                      request.path,
                      resp.traceback)
    return dict(err=resp)


def pre_init():
    app = exts.app
    app.default_error_handler = error_handler
