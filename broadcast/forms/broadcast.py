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
from bottle_utils.i18n import lazy_gettext as _


def get_extension(filepath):
    return os.path.splitext(filepath)[-1].strip(".").lower()


def list_zipfile(zip_filepath):
    with zipfile.ZipFile(zip_filepath, 'r') as zf:
        return zf.namelist()


class ContentForm(form.Form):
    # Translators, used as label for a login field
    content = form.FileField(_("Content"),
                             placeholder=_('content'),
                             validators=[form.Required()])

    def postprocess_content(self, file_upload):
        ext = get_extension(file_upload.filename)
        valid = request.app.config.get('app.allowed_upload_extensions',
                                       'zip').split(',')

        if ext not in valid:
            msg = _("Only {0} files are allowed.").format(",".join(valid))
            raise form.ValidationError(msg, {})

        is_html_file = lambda filename: any(filename.endswith(ext)
                                            for ext in ('htm', 'html'))
        files = list_zipfile(file_upload.file)
        if not any(is_html_file(filename) for filename in files):
            msg = _("No HTML file found in: {0}").format(file_upload.filename)
            raise form.ValidationError(msg, {})
        # must seek to the beginning of file so it can be saved
        file_upload.file.seek(0)

        return file_upload
