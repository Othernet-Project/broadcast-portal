"""
broadcast.py: Content upload

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from ..util.auth import login_required
from ..util.template import view


@login_required()
@view('broadcast')
def show_broadcast_form():
    return {}


def route(conf):
    return (
        ('/broadcast/', 'GET', show_broadcast_form, 'broadcast_form', {}),
    )
