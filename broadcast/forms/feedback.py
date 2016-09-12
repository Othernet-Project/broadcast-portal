"""
feedback.py: Feedback submission forms

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from bottle import request
from bottle_utils import form
from bottle_utils.i18n import lazy_gettext as _

from ..app.exts import container as exts
from ..util.sendmail import send_mail


class FeedbackForm(form.Form):
    # Translators, used as label for email field
    email = form.StringField(_("Email"), placeholder=_('Email'))
    # Translators, used as label for message field
    message = form.TextAreaField(_("Message"),
                                 placeholder=_('Message'),
                                 validators=[form.Required()])

    def validate(self):
        ctx = dict(self.processed_data)
        if request.user.is_authenticated:
            ctx.update(email=request.user.email)
        # email sending must happen within valid request context
        send_mail(to=exts.config['feedback.email'],
                  subject='feedback',
                  template='email/feedback.mako',
                  data=ctx)
