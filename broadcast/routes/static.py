from ..util.routes import StaticRoute
from ..util.skinning import skin_assets_dir
from ..app.exts import container as exts


class Static(StaticRoute):

    def get_base_dirs(self):
        return [exts.assets.directory, skin_assets_dir()]

    @classmethod
    def get_path_prefix(cls):
        return exts.config['assets.url']


class Favicon(Static):
    path = '/favicon.ico'

    def get(self):
        return super(Favicon, self).get('favicon.ico')


def route():
    return (Static, Favicon)
