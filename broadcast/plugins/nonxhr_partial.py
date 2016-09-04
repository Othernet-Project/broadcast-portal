import functools

from bottle import request


def nonxhr_partial_plugin():
    """
    Makes non-XHR requests behave as if they are XHR if they contain
    partial=yes parameter in the request data.
    """
    def plugin(callback):
        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            if request.params.get('partial') == 'yes':
                request.environ['HTTP_X_REQUESTED_WITH'] = 'xmlhttprequest'
            return callback(*args, **kwargs)
        return wrapper
    plugin.name = 'noxhr_partial'
    return plugin
