import datetime
import json
import os

import bottle

import bottle_utils.csrf
import bottle_utils.html


class DateTimeCapableEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        return super(DateTimeCapableEncoder, self).default(obj)


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
        'url': app.get_url,
        'csrf_tag': bottle_utils.csrf.csrf_tag,
        '_': lambda x: x,
        'REDIRECT_DELAY': config['app.redirect_delay'],
    })
