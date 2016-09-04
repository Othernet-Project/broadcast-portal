import os
import logging
from os.path import normpath, abspath, join, exists

try:
    from urllib.request import pathname2url
except ImportError:
    from urllib import pathname2url

import webassets.script

from ..app.exts import container as exts
from ..util.skinning import skin_assets_dir, skin_bundles


class Assets:
    """
    Wrapper class for webassets.Environment
    """
    out_pattern = '{filetype}/{filename}-%(version)s.{filetype}'

    def __init__(self, directory='static', url='/static/', debug='merge'):
        self.directory = abspath(directory)
        self.url = url
        self.debug = debug
        self.env = self._env_factory(directory, url, debug)

    @staticmethod
    def _env_factory(directory, url, debug):
        """
        Create a ``webassets.Environment`` instance which will manage the
        assets for this object.
        """
        env = webassets.Environment(directory=directory, url=url, debug=debug,
                                    url_expire=True)
        env.append_path(directory, url=url)
        env.versions = 'hash'
        env.manifest = 'file'
        env.auto_build = True
        return env

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
        assets = [self._js_path(a) for a in self._unique(assets)]
        out_path = self.out_pattern.format(filetype='js', filename=out)
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
        paths are specified without the ``css/`` directory and ``.css``
        extension. These are appended to the paths autmatically.

        This method returns the ``Bundle`` object which can be used to nest
        within other bundles.
        """
        assets = [self._css_path(a) for a in self._unique(assets)]
        out_path = self.out_pattern.format(filetype='css', filename=out)
        bundle = webassets.Bundle(*assets, filters='cssmin', output=out_path)
        self.env.register('css/' + out, bundle)
        return bundle

    def get(self, name):
        return self.env[name].urls()[0]

    def __getitem__(self, name):
        return self.get(name)

    @staticmethod
    def _unique(seq):
        """
        Generator that yields elements of a sequence in order they appear
        without repeating already yielded elements.
        """
        seen = set()
        for i in seq:
            if i in seen:
                continue
            seen.add(i)
            yield i

    @staticmethod
    def _js_path(s):
        """
        Return a string with '.js' extension if input is a string, otherwise
        return input value verbatim.
        """
        if type(s) is str:
            return normpath(s + '.js')
        return s

    @staticmethod
    def _css_path(s):
        """
        Return a string with '.css' extension if input is a string, otherwise
        return input value verbatim.
        """
        if type(s) is str:
            return normpath(s + '.css')
        return s

    @classmethod
    def configure(cls, basedir, url, srcdir, bundles, debug=False):
        """
        Create Assets instance using specified configuration.
        """
        assets = cls(basedir, url, debug)
        assets.add_static_source(join(srcdir, 'js'))
        assets.add_static_source(join(srcdir, 'css'))
        for name, contents in bundles['js'].items():
            assets.add_js_bundle(name, contents)
            logging.debug('Added JS bundle: %s.js', name)
        for name, contents in bundles['css'].items():
            assets.add_css_bundle(name, contents)
            logging.debug('Added CSS bundle: %s.css', name)
        return assets


class BundleParser:
    """
    Parse the bundle configuration file

    The bundle defintion file looks like this::

        foo.js:
          foo
          bar
          baz

        foo.css:
          foo
          bar/baz

    Each bundle starts with ``<bundlename>.<ext>:`` line, followed by any
    number of bundle members that are listed without the extension (extension
    is assumed to match the extension of the bundle). Lines containing member
    files do not need to be indented. Bundles must be separated by a blank
    line.

    Function returns JavaScript and CSS bundles as a two-tuple of dicts mapping
    bundle names to their members. Returns two empty dicts if bundle file does
    not exist, or is not readable.
    """

    def __init__(self, confpath):
        self.confpath = confpath
        self.next = self.find_header
        self.current = None
        self.type = None
        self.members = []
        self.collected = {'js': {}, 'css': {}}

    def finalize_bundle(self):
        if not self.current:
            return
        if self.members:
            self.collected[self.type][self.current] = self.members
        self.type = None
        self.currrent = None
        self.members = []

    def find_header(self, line):
        if not line.endswith(':'):
            return
        name, ext = line[:-1].rsplit('.', 1)
        self.current = name
        self.type = ext
        self.next = self.collect_member

    def collect_member(self, line):
        if not line:
            self.finalize_bundle()
            self.next = self.find_header
            return
        self.members.append(line)

    def parse(self):
        try:
            fd = open(self.confpath, 'r')
        except (OSError, IOError):
            return self.collected
        for line in fd:
            self.next(line.strip())
        self.finalize_bundle()
        fd.close()
        return self.collected


def pre_init():
    logging.info('Configuring static assets')
    conf = exts.config
    output_dir = normpath(conf['assets.output_dir'])
    if not exists(output_dir):
        os.makedirs(output_dir)
    srcdir = skin_assets_dir()
    bundlefile = skin_bundles()
    bundles = BundleParser(bundlefile).parse()
    url = conf['assets.url']
    debug = conf.get('assets.debug', exts.debug) and 'merge'
    assets = Assets.configure(output_dir, url, srcdir, bundles, debug)
    exts.template_defaults['assets'] = assets
    exts.assets = assets
