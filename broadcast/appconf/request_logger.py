import time
import logging

from streamline import before, after


def before_request(route):
    route.__start_time = time.time()
    logging.info('%s %s (%s)', route.request.method, route.request.fullpath,
                 route.request.remote_addr)


def after_request(route):
    total_time = time.time() - route.__start_time
    logging.debug('END: %s %s (%ss)', route.request.method,
                  route.request.fullpath, total_time)


def pre_init():
    before(before_request)
    after(after_request)
