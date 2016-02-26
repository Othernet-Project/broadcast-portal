from bottle import request
from bottle_utils.i18n import dummy_gettext as _

from ...util.sendmail import send_mail
from .tokens import EmailVerification


def send_confirmation_email(email, next_path, config=None, db=None):
    config = config or request.app.config
    expiration = config['authentication.confirmation_expires']
    verification = EmailVerification.create(email, expiration, db=db)
    task_runner = config['task.runner']
    task_runner.schedule(send_mail,
                         email,
                         _("Confirm registration"),
                         text='email/confirm',
                         data={'confirmation_key': verification.key,
                               'next_path': next_path},
                         config=config)

