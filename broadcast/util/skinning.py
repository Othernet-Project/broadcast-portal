from os.path import join, normpath

from ..app.exts import container as exts


def skin_dir():
    return join(exts.root, normpath(exts.config['assets.skin_dir']),
                exts.config['assets.skin'])


def skin_view_dir():
    return join(skin_dir(), 'views')


def skin_assets_dir():
    return join(skin_dir(), 'assets')


def skin_src_dir():
    return join(skin_dir(), 'src')
