import os
import functools

import webassets

from bottle import request, static_file

MODDIR = os.path.dirname(__file__)
PKGDIR = os.path.dirname(MODDIR)


class Assets:
    """
    Wrapper class for webassets.Environment
    """
    def __init__(self, directory='static', url='/static/', debug='merge'):
        self.directory = directory
        self.url = url
        self.debug = debug
        self.env = webassets.Environment(directory=directory, url=url,
                                         debug=debug, url_expire=True)

        # Configure pyScss
        self.env.config['pyscss_static_root'] = directory
        self.env.config['pyscss_static_url'] = url
        self.env.config['pyscss_assets_root'] = os.path.join(directory, 'img')
        self.env.config['pyscss_assets_url'] = url + 'img/'
        self.env.config['pyscss_style'] = (
            'compressed' if debug is False else 'normal')

    def add_js_bundle(self, out, assets):
        """
        Create and register a JavaScript bundle

        The ``out`` parameter is a path to the bundle. It does not include the
        ``js/`` path prefix nor the ``.js`` extension. These are added
        automatically by this method. For example, if you want to build a
        bundle in ``static/js/common/foo.js``, then you would set the ``out``
        argument to ``common/foo``. The ``%(version)s`` paceholder is
        automatically inserted into the resulting filename, so the complete
        path will be ``js/common/foo-%(version)s.js``.

        The ``out`` value is also used to identify bundles.

        Assets is an iterable containing the bundle's contents. They must be
        specified in correct load order. Similar to output path, the asset
        paths are specified without the ``js/`` directory and ``.js``
        extension. These are appended to the paths autmatically.

        JavaScript assets use ``uglifyjs`` as filter.

        This method returns the ``Bundle`` object. Bundle object can be used
        for nesting within other bundles.
        """
        assets = [self._js_path(a) for a in assets]
        out_path = 'js/' + out + '-%(version)s.js'
        bundle = webassets.Bundle(*assets, filters='uglifyjs', output=out_path)
        self.env.register(out, bundle)
        return bundle

    def register_scss_bundle(self, out, assets):
        """
        Create and register Compass bundle

        The ``out`` parameter is a path to bundle. It does not include the
        ``css/`` prefix nor ``.css`` extension. These are added automatically.
        For example, if you want to build a bundle in ``static/css/main.css``,
        then you would set the ``out`` argument to ``main``. The ``out`` value
        is also used to identify the bundle.

        Assets is an iterable containing the bundle's contents. They must be
        specified in correct load order. Similar to output path, the asset
        paths are specified without the ``scss/`` directory and ``.scss``
        extension. These are appended to the paths autmatically.

        This method returns the ``Bundle`` object which can be used to nest
        within other bundles.
        """
        assets = [self._scss_path(a) for a in assets]
        out_path = 'css/' + out + '-%(version)s.css'
        bundle = webassets.Bundle(*assets, filter='pyscss', output=out_path)
        self.env.register(out, bundle)
        return bundle

    @staticmethod
    def _js_path(s):
        if type(s) is str:
            return 'js/' + s + '.js'
        return s

    @staticmethod
    def _scss_path(s):
        if type(s) is str:
            return 'scss/' + s + '.scss'
        return s


def assets_plugin(conf):
    assets_dir = os.path.join(PKGDIR, conf['assets.directory'])
    assets_url = conf['assets.url']
    assets_debug = conf['assets.debug']

    assets = Assets(assets_dir, assets_url, assets_debug)

    def plugin(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            request.assets = assets
            return fn(*args, **kwargs)
        return wrapper
    plugin.name = 'assets'
    return plugin


def static_handler(static_dir='static'):
    """ Return static asset request handler """
    def handle_asset(path):
        return static_file(path, root=static_dir)
    return handle_asset
