import json

import bottle

from ..app.exts import container as exts
from ..util.serializers import DateTimeEncoder


def json_dumps(s):
    return json.dumps(s, cls=DateTimeEncoder)


def pre_init():
    app = exts.app
    app.install(bottle.JSONPlugin(json_dumps=json_dumps))
    bottle.debug(exts.debug)
