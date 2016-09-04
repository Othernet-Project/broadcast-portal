from bottle import request
from bottle_utils.i18n import dummy_gettext as _

from ...util.sendmail import send_mail
from ...app.exts import container as exts
from .tokens import EmailVerification


def send_confirmation_email(email, next_path):
    config = exts.config
    expiration = config['authentication.confirmation_expires']
    verification = EmailVerification.new(email, expiration)
    send_mail(email,
              _("Confirm registration"),
              text='email/confirm',
              data={'confirmation_key': verification.key,
                    'next_path': next_path},
              is_async=True,
              config=config)
