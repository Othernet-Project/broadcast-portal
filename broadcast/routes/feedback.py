"""
feedback.py: Feedback submission

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from bottle_utils.i18n import dummy_gettext as _

from ..forms.feedback import FeedbackForm
from ..util.routes import (
    ActionXHRPartialFormRoute,
    CSRFMixin,
)


class Feedback(CSRFMixin, ActionXHRPartialFormRoute):
    name = 'feedback:submit'
    path = '/feedback/'
    template_name = 'feedback/feedback.mako'
    partial_template_name = 'feedback/_feedback.mako'
    form_factory = FeedbackForm
    success_message = _('Thank you for your feedback.')
    success_url = ('main:home', {})
    success_url_label = _('home page')


def route():
    return (Feedback,)
