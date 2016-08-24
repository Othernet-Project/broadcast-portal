import sys
import logging
from logging.config import dictConfig as log_config

from ..app.exts import container as exts


def pre_init():
    config = exts.config
    log_config({
        'version': 1,
        'root': {
            'handlers': ['file', 'console'],
            'level': logging.DEBUG,
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
                'class': 'logging.StreamHandler',
                'stream': sys.stdout
            }
        },
        'formatters': {
            'default': {
                'format': config['logging.format'],
                'datefmt': config['logging.date_format'],
            },
        },
    })
