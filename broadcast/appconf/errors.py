import logging

from bottle import request

from ..util.template import view
from ..app.exts import container as exts


@view('errors/error.mako')
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
