"""
broadcast.py: Content upload forms

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import os
import re
import logging
import zipfile

from bottle import request
from bottle_utils import form
from bottle_utils import html
from bottle_utils.i18n import lazy_gettext as _

from ..models.items import ContentItem


def get_extension(filepath):
    return os.path.splitext(filepath)[-1].strip(".").lower()


def get_file_size(file_obj, limit=None, chunk_size=1024):
    pos = file_obj.tell()
    file_obj.seek(0)
    file_size = 0
    while True:
        chunk = file_obj.read(chunk_size)
        if not chunk:
            break

        file_size += len(chunk)
        if limit is not None and file_size > limit:
            # guard against reading huge files into memory
            break
    file_obj.seek(pos)
    return file_size


def list_zipfile(zip_filepath):
    with zipfile.ZipFile(zip_filepath, 'r') as zf:
        return zf.namelist()


class ContentForm(form.Form):
    payment_plan = 'review'
    type = ContentItem.table
    messages = {
        # Translators, error shown when file could not be saved
        'nocreate': _('The uploaded file could not be saved, please try again '
                      'a bit later or contact us for help.')
    }

    content_file = form.FileField(
        # Translators, used as label for content file upload field
        _("Upload"),
        placeholder=_('content'),
        validators=[form.Required()],
        messages={
            # Translators, upload form error, do not translate '{formats}'
            'file_format': _('Only {formats} files are allowed.'),
            # Translators, upload form error, do not translate '{size}'
            'file_size': _('File is too large.'),
            # Translators, upload form error, do not translate '{filename}'
            'index': _('No HTML file found in {filename}'),
        }
    )
    is_authorized = form.BooleanField(
        # Translators, used as label for is_authorized field
        _("I am authorized"),
        value="authorized",
        validators=[form.Required()],
        help_text=_("Are you authorized to distribute this file?")
    )

    def postprocess_email(self, value):
        if value and not re.match(r'[^@]+@[^@]+\.[^@]+', value):
            raise form.ValidationError('email_invalid', {})

        return value

    def postprocess_content_file(self, file_upload):
        # validate file size
        allowed_size = request.app.config['{0}.size_limit'.format(self.type)]
        file_size = get_file_size(file_upload.file, limit=allowed_size)
        if file_size > allowed_size:
            h_size = html.hsize(allowed_size)
            raise form.ValidationError('file_size', {'size': h_size})
        # must seek to the beginning of file so it can be saved
        file_upload.file.seek(0)
        return file_upload

    def validate(self):
        try:
            ContentItem.new(
                email=request.user.email,
                username=request.user.username,
                ipaddr=request.user.remote_addr,
                file_object=self.processed_data['content_file'],
            )
        except Exception:
            logging.exception('Content item creation failed')
            raise form.ValidationError('nocreate', {})
