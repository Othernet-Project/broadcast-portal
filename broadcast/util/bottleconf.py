import datetime
import json
import os

import bottle

import bottle_utils.common
import bottle_utils.csrf
import bottle_utils.html

SMINUTE = 60
SHOUR = 60 * SMINUTE


class DateTimeCapableEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        return super(DateTimeCapableEncoder, self).default(obj)


def time_ago(dt, fmt):
    delta = datetime.datetime.utcnow() - dt
    if delta.days > 7:
        return dt.strftime(fmt)
    if delta.days > 1:
        return '{} days ago'.format(delta.days)
    if delta.days == 1:
        return 'yesterday'
    if delta.seconds / SHOUR > 6:
        return 'today'
    if delta.seconds / SHOUR > 1:
        return '{} hours ago'.format(delta.seconds / SHOUR)
    if delta.seconds / SHOUR == 1:
        return '1 hour ago'
    if delta.seconds / SMINUTE > 5:
        return '{} minutes ago'.format(delta.seconds / SMINUTE)
    return 'just now'


def json_dumps(s):
    return json.dumps(s, cls=DateTimeCapableEncoder)


def pre_init(config):
    app = config['bottle']
    app.install(bottle.JSONPlugin(json_dumps=json_dumps))
    bottle.debug(config['server.debug'])
    bottle.TEMPLATE_PATH.insert(0, os.path.join(
        config['root'], config['app.view_path']))
    bottle.BaseTemplate.defaults.update({
        'DEBUG': bottle.DEBUG,
        'request': bottle.request,
        'h': bottle_utils.html,
        'esc': bottle_utils.common.html_escape,
        'aesc': bottle_utils.common.attr_escape,
        'u': bottle_utils.common.to_unicode,
        'url': app.get_url,
        'csrf_tag': bottle_utils.csrf.csrf_tag,
        '_': lambda x: x,
        'time_ago': time_ago,
        'REDIRECT_DELAY': config['app.redirect_delay'],
    })
