"""
null_i18n.py: Noop i18n plugin

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import functools
import gettext

from bottle import request


def null_i18n_plugin(config):
    def plugin(callback):
        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            request.gettext = gettext.NullTranslations()
            return callback(*args, **kwargs)
        return wrapper
    plugin.name = 'null_i18n'
    return plugin
