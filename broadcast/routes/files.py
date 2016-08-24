"""
broadcast.py: Content upload

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from bottle_utils.csrf import csrf_protect, csrf_token

from ..util.auth.decorators import role
from ..forms.files import ContentForm
from ..util.routes import ActionXHRPartialFormRoute, UploadFormMixin


class Upload(ActionXHRPartialFormRoute, UploadFormMixin):
    path = '/upload/'
    template_name = 'files/upload'
    partial_template_name = 'files/_upload'
    form_factory = ContentForm

    @csrf_token
    @role(role.MODERATOR)
    def get(self, *args, **kwargs):
        return super(Upload, self).get(*args, **kwargs)

    @csrf_protect
    @role(role.MODERATOR)
    def post(self, *args, **kwargs):
        return super(Upload, self).post(*args, **kwargs)

    def get_context(self):
        ctx = super(Upload, self).get_context()
        ctx['size_limit'] = self.app.config['content.size_limit']
        return ctx


def route():
    return (Upload,)
