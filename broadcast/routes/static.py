import datetime

from bottle import static_file

from ..util.routes import StaticRoute
from ..app.exts import container as exts


class Static(StaticRoute):
    def get_base_dir(self):
        return exts.assets.directory

    @classmethod
    def get_path_prefix(cls):
        return exts.config['assets.url']


class Favicon(Static):
    path = '/favicon.ico'

    def get(self):
        return super(Favicon, self).get('favicon.ico')


def route():
    return (Static, Favicon)
