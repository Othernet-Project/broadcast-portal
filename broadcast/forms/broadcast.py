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

from outernet_metadata.values import LICENSES, LICENSE_NAMES

from ..util.broadcast import sign, get_item, ContentItem, TwitterItem

LICENSE_CHOICES = ((None, _('Select the conent license')),)
LICENSE_CHOICES += tuple(zip(LICENSES, LICENSE_NAMES))

# These are locales used for language filtering and similar cases. We want them
# to be as generic as possible, so we only use the main locale without
# territory part. We assume that a consumer of territorry-specific locale is
# able to (at least to an extent) understand generic locale (e.g., pt_BR is
# similar enough to pt).
LOCALES = {
    'gv': u'Gaelg',
    'gu': u'\u0a97\u0ac1\u0a9c\u0ab0\u0abe\u0aa4\u0ac0',
    'gd': u'G\xe0idhlig',
    'ga': u'Gaeilge',
    'gl': u'galego',
    'lg': u'Luganda',
    'ln': u'ling\xe1la',
    'lo': u'\u0ea5\u0eb2\u0ea7',
    'tr': u'T\xfcrk\xe7e',
    'ts': u'Xitsonga',
    'tn': u'Setswana',
    'to': u'lea fakatonga',
    'lt': u'lietuvi\u0173',
    'lu': u'Tshiluba',
    'th': u'\u0e44\u0e17\u0e22',
    'ti': u'\u1275\u130d\u122d\u129b',
    'tg': u'\u0422\u043e\u04b7\u0438\u043a\u04e3',
    'te': u'\u0c24\u0c46\u0c32\u0c41\u0c17\u0c41',
    'ta': u'\u0ba4\u0bae\u0bbf\u0bb4\u0bcd',
    'yo': u'\xc8d\xe8 Yor\xf9b\xe1',
    'de': u'Deutsch',
    'ko': u'\ud55c\uad6d\uc5b4',
    'da': u'dansk',
    'dz': u'\u0f62\u0fab\u0f7c\u0f44\u0f0b\u0f41',
    'kn': u'\u0c95\u0ca8\u0ccd\u0ca8\u0ca1',
    'el': u'\u0395\u03bb\u03bb\u03b7\u03bd\u03b9\u03ba\u03ac',
    'eo': u'esperanto',
    'en': u'English',
    'zh': u'\u4e2d\u6587',
    'ee': u'e\u028begbe',
    'eu': u'euskara',
    'zu': u'isiZulu',
    'es': u'espa\xf1ol',
    'ru': u'\u0440\u0443\u0441\u0441\u043a\u0438\u0439',
    'rw': u'Kinyarwanda',
    'kl': u'kalaallisut',
    'rm': u'rumantsch',
    'rn': u'Ikirundi',
    'ro': u'rom\xe2n\u0103',
    'be': u'\u0431\u0435\u043b\u0430\u0440\u0443\u0441\u043a\u0430\u044f',
    'bg': u'\u0431\u044a\u043b\u0433\u0430\u0440\u0441\u043a\u0438',
    'uk': u'\u0443\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430',
    'ps': u'\u067e\u069a\u062a\u0648',
    'bm': u'bamanakan',
    'bn': u'\u09ac\u09be\u0982\u09b2\u09be',
    'bo': u'\u0f54\u0f7c\u0f51\u0f0b\u0f66\u0f90\u0f51\u0f0b',
    'br': u'brezhoneg',
    'bs': u'bosanski',
    'ja': u'\u65e5\u672c\u8a9e',
    'om': u'Oromoo',
    'os': u'\u0438\u0440\u043e\u043d',
    'or': u'\u0b13\u0b21\u0b3c\u0b3f\u0b06',
    'xh': u'isiXhosa',
    'ca': u'catal\xe0',
    'cy': u'Cymraeg',
    'cs': u'\u010de\u0161tina',
    'lv': u'latvie\u0161u',
    'pt': u'portugu\xeas',
    'pa': u'\u0a2a\u0a70\u0a1c\u0a3e\u0a2c\u0a40',
    'is': u'\xedslenska',
    'pl': u'polski',
    'hy': u'\u0570\u0561\u0575\u0565\u0580\u0565\u0576',
    'hr': u'hrvatski',
    'hu': u'magyar',
    'hi': u'\u0939\u093f\u0928\u094d\u0926\u0940',
    'ha': u'Hausa',
    'he': u'\u05e2\u05d1\u05e8\u05d9\u05ea',
    'mg': u'Malagasy',
    'uz': u'\u040e\u0437\u0431\u0435\u043a',
    'ml': u'\u0d2e\u0d32\u0d2f\u0d3e\u0d33\u0d02',
    'mn': u'\u043c\u043e\u043d\u0433\u043e\u043b',
    'mk': u'\u043c\u0430\u043a\u0435\u0434\u043e\u043d\u0441\u043a\u0438',
    'ur': u'\u0627\u0631\u062f\u0648',
    'mt': u'Malti',
    'ms': u'Bahasa Melayu',
    'mr': u'\u092e\u0930\u093e\u0920\u0940',
    'my': u'\u1017\u1019\u102c',
    'sq': u'shqip',
    'aa': u'Qafar',
    've': u'Tshiven\u1e13a',
    'af': u'Afrikaans',
    'vi': u'Ti\u1ebfng Vi\u1ec7t',
    'ak': u'Akan',
    'am': u'\u12a0\u121b\u122d\u129b',
    'it': u'italiano',
    'vo': u'Volap\xfck',
    'ii': u'\ua188\ua320\ua259',
    'as': u'\u0985\u09b8\u09ae\u09c0\u09af\u09bc\u09be',
    'ar': u'\u0627\u0644\u0639\u0631\u0628\u064a\u0629',
    'et': u'eesti',
    'ia': u'interlingua',
    'az': u'az\u0259rbaycanca',
    'id': u'Bahasa Indonesia',
    'ig': u'Igbo',
    'ks': u'\u06a9\u0672\u0634\u064f\u0631',
    'nl': u'Nederlands',
    'nn': u'nynorsk',
    'nb': u'norsk bokm\xe5l',
    'nd': u'isiNdebele',
    'ne': u'\u0928\u0947\u092a\u093e\u0932\u0940',
    'kw': u'kernewek',
    'nr': u'isiNdebele',
    'fr': u'fran\xe7ais',
    'fa': u'\u0641\u0627\u0631\u0633\u06cc',
    'kk': u'\u049b\u0430\u0437\u0430\u049b \u0442\u0456\u043b\u0456',
    'ff': u'Pulaar',
    'fi': u'suomi',
    'fo': u'f\xf8royskt',
    'ka': u'\u10e5\u10d0\u10e0\u10d7\u10e3\u10da\u10d8',
    'ss': u'Siswati',
    'sr': u'\u0421\u0440\u043f\u0441\u043a\u0438',
    'ki': u'Gikuyu',
    'sw': u'Kiswahili',
    'sv': u'svenska',
    'km': u'\u1781\u17d2\u1798\u17c2\u179a',
    'st': u'Sesotho',
    'sk': u'sloven\u010dina',
    'si': u'\u0dc3\u0dd2\u0d82\u0dc4\u0dbd',
    'so': u'Soomaali',
    'sn': u'chiShona',
    'sl': u'sloven\u0161\u010dina',
    'ky': u'\u041a\u044b\u0440\u0433\u044b\u0437',
    'sg': u'S\xe4ng\xf6',
    'se': u'davvis\xe1megiella'
}
LOCALE_CHOICES = ((None, _('Select the content language')),) + tuple(
    sorted(LOCALES.items(), key=lambda x: x[0]))


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
    type = ContentItem.type

    id = form.HiddenField(validators=[form.Required()])
    signature = form.HiddenField(validators=[form.Required()])
    # Translators, used as label for content file upload field
    content_file = form.FileField(_("Content file"),
                                  placeholder=_('content'),
                                  validators=[form.Required()])
    # Translators, used as label for content title field
    title = form.StringField(_("Content title"),
                             placeholder=_('content title'),
                             validators=[form.Required()])
    # Translators, used as label for content license field
    license = form.SelectField(_("License"),
                               choices=LICENSE_CHOICES,
                               validators=[form.Required()])
    # Translators, used as label for content language field
    language = form.SelectField(_("Language"),
                                choices=LOCALE_CHOICES,
                                validators=[form.Required()])
    # Translators, used as label for content link field
    url = form.StringField(_("Choose your content link"),
                           validators=[form.Required()])

    def postprocess_content_file(self, file_upload):
        # validate extension
        ext = get_extension(file_upload.filename)
        valid = request.app.config['content.allowed_upload_extensions']

        if ext not in valid:
            msg = _("Only {0} files are allowed.").format(",".join(valid))
            raise form.ValidationError(msg, {})

        # validate file size
        allowed_size = request.app.config['content.size_limit']
        file_size = get_file_size(file_upload.file, limit=allowed_size)
        if file_size > allowed_size:
            h_size = html.hsize(allowed_size)
            msg = _("Files larger than {0} are not allowed.").format(h_size)
            raise form.ValidationError(msg, {})

        self.processed_data['file_size'] = file_size

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

    def postprocess_url(self, value):
        template = request.app.config['content.url_template']
        content_url = template.format(value)
        if get_item('content', url=content_url):
            message = _("The chosen path is already in use.")
            raise form.ValidationError(message, {})

        return content_url

    def validate(self):
        id = self.processed_data['id']
        signature = self.processed_data['signature']
        secret_key = request.app.config.get('app.secret_key')
        if signature != sign(id, secret_key):
            message = _("Form data missing or has been tampered with.")
            raise form.ValidationError(message, {})

        if get_item('content', id=id):
            message = _("Form expired, please retry the submission.")
            raise form.ValidationError(message, {})


class TwitterHandle(form.Validator):

    def validate(self, data):
        if not data.startswith('@'):
            message = _("A twitter handle must begin with the @ character.")
            raise form.ValidationError(message, {})


class TwitterForm(form.Form):
    type = TwitterItem.type

    PAYMENT_PLANS = (
        ('lifetime', _("Lifetime")),
    )
    # Translators, used as label for twitter handle(username)
    handle = form.StringField(_("Twitter handle"),
                              placeholder=_('@handle'),
                              validators=[form.Required(), TwitterHandle()])
    # Translators, used as label for payment plan
    plan = form.SelectField(_("Payment plan"),
                            choices=PAYMENT_PLANS,
                            validators=[form.Required()])
