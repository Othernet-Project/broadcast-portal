import os
import logging

from ..app.exts import container as exts


def ensure_dir(path):
    if os.path.exists(path):
        return
    os.makedirs(path)


def pre_init():
    conf = exts.config
    logging.info('Preparing application directories')
    paths = (
        conf['database.path'],
        conf['content.upload_root'],
        conf['mako.module_directory'],
    )
    for p in paths:
        ensure_dir(p)
