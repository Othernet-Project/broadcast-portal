import logging

from bottle_utils.i18n import dummy_gettext as _

from ..util.routes import (
    TemplateRoute,
    ActionXHRPartialFormRoute,
    CSRFMixin,
)
from ..forms.main import BetaSignupForm
from ..app.exts import container as exts


class Home(TemplateRoute):
    path = '/'
    template_name = 'main/home.mako'

    def get(self):
        return {}


class BetaSignup(CSRFMixin, ActionXHRPartialFormRoute):
    path = '/beta-signup'
    template_name = 'main/beta_signup.mako'
    partial_template_name = 'main/_beta_signup.mako'
    form_factory = BetaSignupForm
    success_message = _('You have been added to the closed beta list')
    success_url = ('main:home', {})


class Terms(TemplateRoute):
    path = '/terms'
    template_name = 'main/terms.mako'

    def get(self):
        return {}


def load_beta_whitelist():
    whitelist_path = exts.config['beta.whitelist']
    try:
        with open(whitelist_path, 'r') as f:
            blist = [l.strip().lower() for l in f]
    except (OSError, IOError):
        logging.error('Could not load the beta whitelist')
        blist = []
    return blist


def route():
    exts.beta_whitelist = load_beta_whitelist()
    return (Home, BetaSignup, Terms)
