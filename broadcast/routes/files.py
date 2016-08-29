"""
broadcast.py: Content upload

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from ..forms.files import ContentForm
from ..util.routes import (
    ActionXHRPartialFormRoute,
    UploadFormMixin,
    RoleMixin,
    CSRFMixin,
)


class Upload(RoleMixin, CSRFMixin, UploadFormMixin, ActionXHRPartialFormRoute):
    role = RoleMixin.USER
    path = '/upload/'
    template_name = 'files/upload.mako'
    partial_template_name = 'files/_upload.mako'
    form_factory = ContentForm

    def get_context(self):
        ctx = super(Upload, self).get_context()
        ctx['size_limit'] = self.app.config['content.size_limit']
        return ctx


def route():
    return (Upload,)
