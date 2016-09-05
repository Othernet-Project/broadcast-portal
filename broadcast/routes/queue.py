from __future__ import division

import logging
import datetime

from bottle_utils.i18n import dummy_gettext as _

from ..models.items import ContentItem
from ..util.helpers import to_timestamp, utcnow, tomorrow
from ..app.exts import container as exts
from ..util.routes import (
    ActionTemplateRoute,
    XHRPartialRoute,
    StaticRoute,
    XHRJsonRoute,
    RoleMixin,
)


class ModeratorOnlyMixin(RoleMixin):
    role = RoleMixin.MODERATOR
    role_denied_message = _('This feature is only accessible to moderators')


class ItemListMixin(ModeratorOnlyMixin):
    def get_items(self):
        # TODO: implement paging
        return ContentItem.binless_items(kind=self.item_type,
                                         username=self.request.user.username)

    def get(self):
        return {'items': self.get_items()}


class Status(ModeratorOnlyMixin, XHRPartialRoute):
    """
    The queue status page
    """
    template_name = 'queue/status.mako'
    partial_template_name = 'queue/_status.mako'
    path = '/queue/'
    role_xhr_method_whitelist = ['GET']

    @staticmethod
    def closing_time():
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        return to_timestamp(tomorrow)

    def get(self):
        stats = ContentItem.candidate_stats()
        bin_limit = exts.config['bin.capacity']
        pct_cap = (stats.size / bin_limit) * 100 if stats.count else 0
        return {
            'capacity': bin_limit,
            'size': stats.size or 0,
            'count': stats.count or 0,
            'pct_capacity': pct_cap,
            'closing': self.closing_time(),
            'last_update': exts.last_update,
            'today': utcnow().date(),
            'timestamp': to_timestamp(tomorrow())
        }


class Candidates(ItemListMixin, XHRPartialRoute):
    """
    Daily bin candidate list
    """
    path = '/queue/candidates/'
    template_name = 'queue/candidates.mako'
    partial_template_name = 'queue/_candidates.mako'
    item_type = ContentItem.CANDIDATES


class Review(ItemListMixin, XHRPartialRoute):
    """
    Review list with non-candidate items
    """
    path = '/queue/review/'
    template_name = 'queue/review.mako'
    partial_template_name = 'queue/_review.mako'
    item_type = ContentItem.NON_CANDIDATES

    def get_items(self):
        items = super(Review, self).get_items()
        return sorted(items, key=lambda i: i.created, reverse=True)


class Vote(ModeratorOnlyMixin, ActionTemplateRoute):
    path = '/queue/<item_id:re:[0-9a-f]{32}>/'
    success_message = _('Your vote has been saved')
    error_message = _('Your vote could not be saved')

    def get_success_url(self):
        return self.back_to or self.app.get_url('queue:status')
    get_error_url = get_success_url

    def get_success_url_label(self):
        return _('previous page') if self.back_to else _('status page')
    get_error_url_label = get_success_url_label

    def post(self, item_id):
        self.back_to = self.request.params.get('next')
        username = self.request.user.username
        is_upvote = self.request.forms.get('upvote', 'yes') == 'yes'
        ipaddr = self.request.remote_addr
        try:
            item = ContentItem.get(item_id)
        except ContentItem.NotFound:
            self.abort(404)
        try:
            item.cast_vote(username, is_upvote, ipaddr)
        except Exception:
            # TODO: Tell user exactly why
            logging.exception('Vote could not be saved')
            self.status = False
        else:
            self.status = True


class Download(ModeratorOnlyMixin, StaticRoute):
    path = '/download/<item_id:re:[0-9a-f]{32}>'

    def get_base_dirs(self):
        return [exts.config['content.upload_root']]

    def get(self, item_id):
        try:
            item = ContentItem.get(item_id)
        except ContentItem.NotFound:
            self.abort(404)
        return self.create_file_response(item.path)


class LastUpdate(XHRJsonRoute):
    path = '/queue/last-update'
    exclude_plugins = ['session']

    def get(self):
        return exts.last_update


def route():
    exts.last_update = {'timestamp': to_timestamp(ContentItem.last_activity())}
    exts.template_defaults['last_update'] = exts.last_update
    return (Status, Candidates, Review, Vote, Download, LastUpdate)
