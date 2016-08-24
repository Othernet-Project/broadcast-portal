import logging

from bottle_utils import form
from bottle_utils.i18n import dummy_gettext as _

from ..app.exts import container as exts
from ..models.auth import InvitationToken
from ..util.validators import EmailValidator


BETA_SIGNUP_EXPIRY = 20


class BetaSignupForm(form.Form):
    email = form.StringField(
        # Translators, used as label in create user form
        _("Email"),
        validators=[form.Required(), EmailValidator()],
        placeholder=_('Email'))

    def validate(self):
        email = self.processed_data['email']
        if email in exts.beta_whitelist:
            token = InvitationToken.new(email, BETA_SIGNUP_EXPIRY)
            token.send()
            self.processed_data['token_sent'] = True
        else:
            logging.debug('BETA: %s', email)
            self.processed_data['token_sent'] = False
