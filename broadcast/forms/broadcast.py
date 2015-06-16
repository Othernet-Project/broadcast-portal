"""
broadcast.py: Content upload forms

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import os
import zipfile

from bottle import request
from bottle_utils import form
from bottle_utils import html
from bottle_utils.i18n import lazy_gettext as _

from outernet_metadata.values import LICENSE_PAIRS

from ..util.broadcast import sign, get_content_by_url


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
    content_id = form.HiddenField(validators=[form.Required()])
    signature = form.HiddenField(validators=[form.Required()])
    # Translators, used as label for content file upload field
    content_file = form.FileField(_("Content"),
                                  placeholder=_('content'),
                                  validators=[form.Required()])
    # Translators, used as label for content title field
    title = form.StringField(_("Content title"),
                             placeholder=_('content title'),
                             validators=[form.Required()])
    # Translators, used as label for content license field
    license = form.SelectField(_("License"),
                               choices=LICENSE_PAIRS.items(),
                               validators=[form.Required()])
    # Translators, used as label for content link field
    path = form.StringField(_("Choose your content link"),
                            validators=[form.Required()])

    def postprocess_content(self, file_upload):
        # validate extension
        ext = get_extension(file_upload.filename)
        valid = request.app.config['content.allowed_upload_extensions']

        if ext not in valid:
            msg = _("Only {0} files are allowed.").format(",".join(valid))
            raise form.ValidationError(msg, {})

        # validate file size
        allowed_size = request.app.config['content.size_limit']
        if get_file_size(file_upload.file, limit=allowed_size) > allowed_size:
            h_size = html.hsize(allowed_size)
            msg = _("Files larger than {0} are not allowed.").format(h_size)
            raise form.ValidationError(msg, {})

        # validate contents
        is_html_file = lambda filename: any(filename.endswith(ext)
                                            for ext in ('htm', 'html'))
        files = list_zipfile(file_upload.file)
        if not any(is_html_file(filename) for filename in files):
            msg = _("No HTML file found in: {0}").format(file_upload.filename)
            raise form.ValidationError(msg, {})
        # must seek to the beginning of file so it can be saved
        file_upload.file.seek(0)

        return file_upload

    def postprocess_path(self, value):
        template = request.app.config['content.content_path_template']
        content_url = template.format(value)
        if get_content_by_url(content_url):
            message = _("The chosen path is already in use.")
            raise form.ValidationError(message, {})

        return content_url

    def validate(self):
        content_id = self.processed_data['content_id']
        signature = self.processed_data['signature']
        secret_key = request.app.config.get('app.secret_key')
        if signature != sign(content_id, secret_key):
            message = _("Form data missing or has been tampered with.")
            raise form.ValidationError(message, {})
