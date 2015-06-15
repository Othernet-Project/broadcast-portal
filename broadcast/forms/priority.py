"""
priority.py: Payment forms

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""


from bottle_utils import form
from bottle_utils.i18n import lazy_gettext as _


class PaymentForm(form.Form):
    stripe_public_key = form.HiddenField()
    stripe_token = form.HiddenField()
    # Translators, used as label for credit card number field
    card_number = form.StringField(_("Card Number"),
                                   **{'data-stripe': 'number', 'size': 20})
    # Translators, used as label for credit card CVC field
    cvc = form.IntegerField(_("CVC"),
                            **{'data-stripe': 'cvc', 'size': 4})
    # Translators, used as label for credit card expiration month field
    exp_month = form.IntegerField(_("Expiration (MM/YYYY)"),
                                  **{'data-stripe': 'exp-month', 'size': 2})
    # Translators, used as label for credit card expiration year field
    exp_year = form.IntegerField(_("Expiration (MM/YYYY)"),
                                 **{'data-stripe': 'exp-year', 'size': 4})

    def validate(self):
        if not self.processed_data['stripe_token']:
            message = _("Payment submission was not successful.")
            raise form.ValidationError(message, {})
