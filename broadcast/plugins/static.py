import os
import glob
import logging
import functools

import webassets
from webassets.script import CommandLineEnvironment

from bottle import request

from ..app.exts import container as exts


MODDIR = os.path.dirname(__file__)
PKGDIR = os.path.dirname(MODDIR)


class Assets:
    """
    Wrapper class for webassets.Environment
    """
    def __init__(self, directory='static', url='/static/', debug='merge'):
        self.directory = os.path.abspath(directory)
        self.url = url
        self.debug = debug
        self.env = webassets.Environment(directory=self.directory, url=url,
                                         debug=debug, url_expire=True)
        self.env.versions = 'hash'
        self.env.manifest = 'file'
        if not debug:
            self.env.auto_rebuild = False

    def add_static_source(self, path, url=None):
        """
        Third parties should call this method to register their own static
        folders.
        """
        self.env.append_path(path, url=url)

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

        The ``out`` value is also used to identify bundles, and the identifier
        is prefixed with 'js/'.

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
        bundle = webassets.Bundle(*assets, filters='rjsmin', output=out_path)
        self.env.register('js/' + out, bundle)
        return bundle

    def add_css_bundle(self, out, assets):
        """
        Create and register Compass bundle

        The ``out`` parameter is a path to bundle. It does not include the
        ``css/`` prefix nor ``.css`` extension. These are added automatically.
        For example, if you want to build a bundle in ``static/css/main.css``,
        then you would set the ``out`` argument to ``main``.

        The ``out`` value is also used to identify the bundle, and the
        identifier is prefixed with 'css/'.

        Assets is an iterable containing the bundle's contents. They must be
        specified in correct load order. Similar to output path, the asset
        paths are specified without the ``scss/`` directory and ``.scss``
        extension. These are appended to the paths autmatically.

        This method returns the ``Bundle`` object which can be used to nest
        within other bundles.
        """
        assets = [self._scss_path(a) for a in assets]
        out_path = 'css/' + out + '-%(version)s.css'
        bundle = webassets.Bundle(*assets, filters='cssmin', output=out_path)
        self.env.register('css/' + out, bundle)
        return bundle

    def get(self, name):
        return self.env[name].urls()[0]

    def __getitem__(self, name):
        return self.get(name)

    @staticmethod
    def _js_path(s):
        if type(s) is str:
            return s + '.js'
        return s

    @staticmethod
    def _scss_path(s):
        if type(s) is str:
            return s + '.css'
        return s


def parse_bundle(bundle):
    bundle_name, bundle_content = [b.strip() for b in bundle.split(':')]
    bundle_content = [b.strip() for b in bundle_content.split(',')]
    return bundle_name, bundle_content


def make_assets(config):
    """ Create Assets instance from dict-like config object """
    assets_dir = os.path.join(PKGDIR, config['assets.directory'])
    assets_url = config['assets.url']
    assets_debug = config['assets.debug']

    assets = Assets(assets_dir, assets_url, assets_debug)
    assets.add_static_source(os.path.join(assets_dir, 'css'), url=assets_url)
    assets.add_static_source(os.path.join(assets_dir, 'js'), url=assets_url)

    js_bundles = [parse_bundle(b)
                  for b in config.get('assets.js_bundles', [])]
    for name, contents in js_bundles:
        assets.add_js_bundle(name, contents)

    css_bundles = [parse_bundle(b)
                   for b in config.get('assets.css_bundles', [])]
    for name, contents in css_bundles:
        assets.add_css_bundle(name, contents)
    return assets


def rebuild_assets():
    config = exts.config.copy()
    config['assets.debug'] = True
    assets = make_assets(config)
    assets_dir = assets.env.directory
    # Remove existing assets
    for name, bundle in assets.env._named_bundles.items():
        path = os.path.join(assets_dir, bundle.output) % {'version': '*'}
        for p in glob.iglob(path):
            os.unlink(p)
    cmdenv = CommandLineEnvironment(assets.env, logging.getLogger('assets'))
    cmdenv.invoke('build', {})


def pre_init():
    exts.assets = make_assets(exts.config)


def assets_plugin():
    def plugin(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            request.assets = exts.assets
            return fn(*args, **kwargs)
        return wrapper
    plugin.name = 'assets'
    return plugin
