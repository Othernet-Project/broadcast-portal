import os

import bottle

import bottle_utils.common
import bottle_utils.csrf
import bottle_utils.html
from bottle_utils.i18n import (
    dummy_gettext as gettext,
    dummy_ngettext as ngettext
)

from mako.lookup import TemplateLookup

from ..util.template_helper import template_helper
from ..app.exts import container as exts


def pre_init():
    app = exts.app
    config = exts.config

    template_dir = os.path.join(exts.root, config['app.view_path'])
    template_debug = config.get('app.view_debug', exts.debug)
    cache_dir = os.path.join(exts.root, config['app.view_cache_dir'])

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    exts.templates = {}
    exts.templates['lookup'] = TemplateLookup(
        directories=[template_dir],
        filesystem_checks=template_debug,
        default_filters=['unicode', 'h'],
        module_directory=cache_dir)
    exts.templates['defaults'] = {
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
        'REDIRECT_DELAY': config['app.redirect_delay'],
    }
