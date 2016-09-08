import logging

from ..util.routes import TemplateRoute
from ..app.exts import container as exts


class Home(TemplateRoute):
    path = '/'
    template_name = 'main/home.mako'

    def get(self):
        return {}


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
    return (Home, Terms)
