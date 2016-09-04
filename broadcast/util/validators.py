import re

from bottle_utils import form
from bottle_utils.i18n import dummy_gettext as _


class EmailValidator(form.Validator):
    EMAIL_RE = re.compile(r'[^@]+@[^@]+\.[^@]+')

    messages = {
        'invalid_email': _('Please enter a valid email')
    }

    def validate(self, value):
        if self.EMAIL_RE.match(value):
            return value
        raise form.ValidationError('invalid_email', {})
