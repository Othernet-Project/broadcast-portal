import os

import bottle

import bottle_utils.html


def pre_init(config):
    bottle.debug(config['server.debug'])
    bottle.TEMPLATE_PATH.insert(0, os.path.join(
        config['root'], config['app.view_path']))
    bottle.BaseTemplate.defaults.update({
        'request': bottle.request,
        'h': bottle_utils.html,
    })
