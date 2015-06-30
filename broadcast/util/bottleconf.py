import os

import bottle

import bottle_utils.csrf
import bottle_utils.html


def pre_init(config):
    app = config['bottle']
    bottle.debug(config['server.debug'])
    bottle.TEMPLATE_PATH.insert(0, os.path.join(
        config['root'], config['app.view_path']))
    bottle.BaseTemplate.defaults.update({
        'request': bottle.request,
        'h': bottle_utils.html,
        'url': app.get_url,
        'csrf_tag': bottle_utils.csrf.csrf_tag,
        '_': lambda x: x,
        'REDIRECT_DELAY': config['app.redirect_delay'],
    })
