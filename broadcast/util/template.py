"""
template.py: Mako template rendering functions

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import functools

from ..app.exts import container as exts


def render(template, ctx={}):
    """
    Render a Mako template given context
    """
    final_ctx = exts.template_defaults.copy()
    final_ctx.update(ctx)
    template = exts.template_lookup.get_template(template)
    return template.render(**final_ctx)


def view(template):
    """
    Bottle route decorator that renders the handler output with Mako template
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            ctx = fn(*args, **kwargs)
            return render(template, ctx)
        return wrapper
    return decorator
