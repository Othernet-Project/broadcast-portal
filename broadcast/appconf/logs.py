import sys
import logging
from logging.config import dictConfig as log_config

from ..app.exts import container as exts


def pre_init():
    config = exts.config
    log_config({
        'version': 1,
        'root': {
            'handlers': ['file'] if exts.quiet else ['file', 'console'],
            'level': logging.DEBUG if exts.debug else logging.INFO,
        },
        'handlers': {
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': config['logging.output'],
                'maxBytes': config['logging.size'],
                'backupCount': config['logging.backups'],
            },
            'console': {
                'formatter': 'simple',
                'class': 'logging.StreamHandler',
                'stream': sys.stdout
            }
        },
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)-8s %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S (%z)',
            },
            'simple': {
                'format': '[%(levelname)-8s] %(message)s',
            }
        },
    })
