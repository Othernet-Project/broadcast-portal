from os.path import join, normpath, isdir

from ..app.exts import container as exts


def skin_dir():
    skindir = exts.config['assets.skin_dir']
    extras = exts.config['assets.extra_skins']
    skin = exts.config['assets.skin']
    if extras:
        skinpath = join(normpath(extras), skin)
    if isdir(skinpath):
        return skinpath
    return join(exts.root, normpath(skindir), skin)


def skin_view_dir():
    return join(skin_dir(), 'views')


def skin_assets_dir():
    return join(skin_dir(), 'assets')


def skin_src_dir():
    return join(skin_dir(), 'src')


def skin_bundles():
    return join(skin_assets_dir(), 'bundles.conf')
