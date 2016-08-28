import os
from os.path import join, normpath, exists

import bottle

import bottle_utils.common
import bottle_utils.csrf
import bottle_utils.html
from bottle_utils.i18n import (
    dummy_gettext as gettext,
    dummy_ngettext as ngettext
)

from mako.lookup import TemplateLookup

from ..app.exts import container as exts
from ..util.skinning import skin_view_dir
from ..util.template_helper import template_helper


def pre_init():
    app = exts.app
    config = exts.config

    template_dirs = [skin_view_dir(), join(exts.root, 'views')]
    template_debug = config.get('app.view_debug', exts.debug)
    cache_dir = join(exts.root, normpath(config['app.view_cache_dir']))

    if not exists(cache_dir):
        os.makedirs(cache_dir)

    exts.template_lookup = TemplateLookup(
        directories=template_dirs,
        filesystem_checks=template_debug,
        default_filters=['unicode', 'h'],
        module_directory=cache_dir
    )
    exts.template_defaults.update({
        'DEBUG': exts.debug,
        'request': bottle.request,
        'h': bottle_utils.html,
        'th': template_helper,
        'esc': bottle_utils.common.html_escape,
        'aesc': bottle_utils.common.attr_escape,
        'u': bottle_utils.common.to_unicode,
        'url': app.get_url,
        'csrf_tag': bottle_utils.csrf.csrf_tag,
        '_': gettext,
        'ngettext': ngettext,
    })
