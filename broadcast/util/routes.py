import datetime

from streamline import (
    Route,
    RouteBase,
    NonIterableRouteBase,
    TemplateRoute,
    XHRPartialRoute,
    ROCARoute,
    FormRoute,
    TemplateFormRoute,
    XHRPartialFormRoute,
)
from bottle import static_file
from streamline.template import TemplateMixin
from streamline.forms import FormMixin, FormBase
from bottle_utils.i18n import dummy_gettext as _
from bottle_utils.csrf import csrf_protect, csrf_token

from .serializers import jsonify
from .template import render
from ..models import auth


# Monkey-patch the TemplateMixin to use our own rendering function
TemplateMixin.template_func = staticmethod(render)


class StaticRoute(NonIterableRouteBase):
    path = None
    exclude_plugins = ['sessions']
    path_prefix = '/static'

    EXP_TIMESTAMP = '%a, %d %b %Y %H:%M:%S GMT'

    def get_base_dir(self):
        raise NotImplementedError('Subclass must implement this method')

    def get(self, path):
        response = static_file(path, root=self.get_base_dir())
        exp = datetime.datetime.utcnow() + datetime.timedelta(365)
        response.headers['Expires'] = exp.strftime(self.EXP_TIMESTAMP)
        return response

    @classmethod
    def get_path_prefix(cls):
        return cls.path_prefix

    @classmethod
    def get_path(cls):
        return cls.path or '{}/<path:path>'.format(
            cls.get_path_prefix()).replace('//', '/')


class ActionMixin(object):
    """
    This mixin provides the basi building blocks for obtaining the context
    information and template names for rendering action feedback templats.

    The action feedback is part of the GET-POST-REFRESH flow, which is a
    variation on the GET-POST-REDIRECT flow. In the standard GET-POST-REDIRECT
    flow, user obtains the form markup with a GET request, performs a POST, and
    gets REDIRECTed to another route on success. In the GET-POST-REFRESH flow,
    after successful submission, a redirect is not performed directly, but via
    a feedback page armed with ``<meta http-equiv="refresh">`` tag.

    This mixin does not provide means for selecting the template or
    constructing the template context. That is done in the other mixins.
    """

    def __init__(self, *args, **kwargs):
        self.status = None
        super(ActionMixin, self).__init__(*args, **kwargs)

    feedback_template = 'feedback.mako'
    feedback_pratial_template = '_feedback.mako'

    success_title = 'Success'
    success_message = 'Action was successful'
    success_url = '/'
    success_url_label = 'home'

    error_title = 'Error'
    error_message = 'Action failed'
    error_url = None
    error_url_label = 'nowhere'

    def get_success_title(self):
        """
        Return the success title
        """
        return self.success_title

    def get_success_message(self):
        """
        Return the success message
        """
        return self.success_message

    def get_url(self, url):
        """
        Try to parse the ``url`` argument as a two-tuple containing route name
        and route params, and return ``url`` if the value is not a two-tuple.

        If the value is a two-tuple, the application object's ``get_url()``
        method is invoked to construct the URL.

        Second item in the two-tuple is expected to be a dict contianing the
        keyword arguments for the route.
        """
        try:
            route_name, params = url
        except ValueError:
            return url
        else:
            return self.app.get_url(route_name, **params)

    def get_success_url(self):
        """
        Return the redirect URL for the success status
        """
        return self.get_url(self.success_url)

    def get_success_url_label(self):
        """
        Return the label for the success URL
        """
        return self.success_url_label

    def get_error_title(self):
        """
        Return the error title
        """
        return self.error_title

    def get_error_message(self):
        """
        Return the error message
        """
        return self.error_message

    def get_error_url(self):
        """
        Return the redirect URL for the error status
        """
        return self.get_url(self.error_url)

    def get_error_url_label(self):
        """
        Return the label for the error URL
        """
        return self.error_url_label

    def get_context(self):
        """
        Construct and return the template context. The context is contructed
        according to the following rules:

        - If ``status`` property is ``None``, return whatever context the route
          handler would normally return.
        - In all other cases the ``success`` variable is added to the template
          that has the value of the ``status`` property, and the ``title``,
          ``message``, ``url``, and ``url_label`` context variables are added
          according to the values supplied by matching methods from the
          ``ActionMixin`` mixin.

        .. note::
            Response code is set to 400 for ``False`` status.

        """
        ctx = super(ActionMixin, self).get_context()
        if self.status is None:
            return ctx
        ctx['success'] = self.status
        ctx['redirect'] = True
        if not self.status:
            self.response.status = 400
        status = 'success' if self.status else 'error'
        for name in ('title', 'message', 'url', 'url_label'):
            prop = 'get_{status}_{name}'.format(status=status, name=name)
            meth = getattr(self, prop)
            ctx[name] = meth()
        return ctx


class ActionFormMixin(FormMixin):
    """
    Mixin that implments setting of ``status`` property according to form
    validation result. When form validates, ``status`` is set to ``True``. When
    form validation fails, ``status`` is set to ``None``.
    """
    def form_valid(self, *args, **kwargs):
        self.status = True

    def form_invalid(self, *args, **kwargs):
        self.status = None

    def get_context(self):
        ctx = super(ActionFormMixin, self).get_context()
        ctx['form'] = self.form
        return ctx

    def create_response(self):
        self.form = self.get_form()
        super(ActionFormMixin, self).create_response()


class ActionTemplateRoute(ActionMixin, TemplateRoute):
    """
    ``TemplateRoute`` subclass that implements the GET-POST-REFRESH flow. If
    any of the handler methods (``get()``, ``post()``, etc) set the ``status``
    property to a boolean value (``True`` or ``False``) then a feedback
    template is rendered according to the ``ActionTemplateMixin``
    implementation.

    In the usual GET-POST-REFRESH flow, the ``get()`` method leaves the value
    of the ``status`` property at its default value (``None``), and the
    ``post()`` method sets the value. However, a short-circuit GET-REFRESH flow
    can be implemneted by letting the ``get()`` method set the value. The
    latter approach is useful for things like email confirmation links.
    """
    def get_feedback_template_name(self):
        """
        Return the template name for the feedback
        """
        return self.feedback_template

    get_success_template_name = get_feedback_template_name
    get_error_template_name = get_feedback_template_name

    def get_template_name(self, template_name=None):
        """
        Select the template for the response. The template is selected
        according to the following rules:

        - if ``status`` property is ``None``, has the same behavior as a normal
          ``TemplateRoute``
        - if ``status`` is ``True`` return the result of the
          ``get_success_template_name()`` method call
        - if ``status`` is ``False`` return the result of the
          ``get_error_template_name()`` method call.
        """
        if self.status is None:
            return super(ActionTemplateRoute, self).get_template_name(
                template_name)
        if self.status:
            return self.get_success_template_name()
        return self.get_error_template_name()


class ActionXHRPartialRoute(ActionMixin, XHRPartialRoute):
    """
    ``XHRPartialRoute`` mixin that implements the GET-POST-REFRESH flow. The
    non-GET methods are expected to set the ``status`` property to one of the
    ``None``, ``True``, or ``False`` value.
    """
    def get_feedback_template_name(self):
        """
        Return the template name for the feedback. For XHR request, a partial
        template is selected.
        """
        if self.is_xhr:
            return self.feedback_partial_template
        else:
            return self.feedback_template

    get_success_template_name = get_feedback_template_name
    get_error_template_name = get_feedback_template_name

    def get_template_name(self):
        if self.status is None:
            return super(ActionXHRPartialRoute, self).get_template_name()
        if self.status:
            return self.get_success_template_name()
        return self.get_error_template_name()


class ActionTemplateFormRoute(ActionFormMixin, FormBase, ActionTemplateRoute):
    """
    ``TemplateFormRoute`` subclass that implements the GET-POST-REFRESH flow.
    """
    pass


class ActionXHRPartialFormRoute(ActionFormMixin, FormBase,
                                ActionXHRPartialRoute):
    """
    ``XHRPartialFormRoute`` subclass that implments the GET-POST-REFRESH flow.
    """
    pass


class UploadFormMixin(object):
    """
    A mixin used for forms that handle file uploads. This mixin slightly
    modifies the behavior of the ``get_bound_form()`` to handle multi-part
    forms. It updates the form data passed to the form factory function with
    the actual file objects extracted by Bottle, such that the key matching the
    form field containing the file will point to the file object instaed of the
    file name.
    """
    def get_bound_form(self):
        data = self.request.forms.decode()
        data.update(self.request.files)
        form_factory = self.get_form_factory()
        return form_factory(data)


class RoleMixin(object):
    """
    Route mixin that checks for user role specified by the ``role`` property,
    and aborts with 403 status code when the user role does not match.

    The ``role_denied_message`` is a string that is used as a message when role
    is denied access.

    The ``role_method_whitelist`` is a list of methods that should not be
    checked for role. It is an empty list by default, and all methods are
    checked. The values should be upper-case method names (e.g., 'GET', 'POST',
    etc).
    """
    role = None
    role_denided_message = _('You cannot access this page with current '
                             'privileges')
    role_needs_login_message = _('Please log in in order to gain access to '
                                 'this page')
    role_method_whitelist = []

    # FIXME: Temporary assignment
    SUPERUSER = auth.GUEST
    MODERATOR = auth.GUEST
    USER = auth.GUEST
    GUEST = auth.GUEST

    def get_role(self):
        return self.role

    def get_role_denied_message(self):
        return self.role_denied_message

    def get_role_method_whitelist(self):
        return self.role_method_whitelist

    def check_role(self):
        if self.request.method in self.get_role_method_whitelist():
            return

        user = self.request.user
        role = self.get_role()

        if user.should_login_for_role(role):
            self.abort(401, self.get_role_needs_login_message())

        if not user.has_role(role):
            self.abort(403, self.get_role_denied_message())

    def create_response(self):
        self.check_role()
        super(RoleMixin, self).create_response()


class CSRFMixin(object):
    """
    This mixin adds CSRF tokens and guards to appropriate methods in the route
    handler class. The ``get()`` method will be wrapped in the
    ``@bottle_utils.csrf.csrf_token`` decorator, while all other methods are
    wrapped in the ``@bottle_utils.csrf.csrf_protect`` decorator. Only the
    methods that are actually implmented by the class are wrppped.
    """
    def __new__(cls, *args, **kwargs):
        if hasattr(cls, 'get'):
            cls.get = csrf_token(cls.get)
        for meth in ['post', 'put', 'patch', 'delete']:
            if not hasattr(cls, meth):
                continue
            orig_meth = getattr(cls, meth)
            setattr(cls, meth, csrf_protect(orig_meth))
        return super(CSRFMixin, cls).__new__(cls, *args, **kwargs)


class XHRJsonRoute(NonIterableRouteBase):
    """
    Route class that rejects non-XHR requests with 400 status, and responds
    with JSON data to XHR requests.
    """
    def create_response(self):
        if not self.request.is_xhr:
            self.abort(400)
        super(XHRJsonRoute, self).create_response()
        self.body = jsonify(self.body)
        self.response.set_header('Content-Type', 'application/json')
