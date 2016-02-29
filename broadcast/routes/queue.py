from bottle import request, redirect, abort
from bottle_utils.ajax import roca_view
from bottle_utils.csrf import csrf_token, csrf_protect
from bottle_utils.i18n import dummy_gettext as _

from ..forms.queue import QueueItemForm
from ..util.auth.decorators import login_required
from ..util.bins import Bin
from ..util.broadcast import ContentItem, filter_items, get_item
from ..util.template import template, view


@csrf_token
@roca_view('queue_list', '_accepted_list', template_func=template)
def queue_accepted():
    current_bin = Bin.current()
    accepted = filter_items(ContentItem.type,
                            status=ContentItem.ACCEPTED,
                            bin=current_bin.id)
    return dict(accepted=accepted)


@csrf_token
@roca_view('queue_list', '_review_list', template_func=template)
def queue_review():
    processing = filter_items(ContentItem.type, status=ContentItem.PROCESSING)
    rejected = filter_items(ContentItem.type, status=ContentItem.REJECTED)
    pending = processing + rejected
    return dict(pending=sorted(pending, key=lambda x: x.created))


@view('queue_item')
def queue_item(item_id):
    return {}


@csrf_protect
@login_required(groups='superuser')
def save_queue_item(item_id):
    form = QueueItemForm(request.forms)
    if form.is_valid():
        item = get_item(ContentItem.type, id=item_id, bin=None)
        if not item:
            abort(404, _("The specified item is no longer modifiable."))

        current_bin = Bin.current()
        status = form.processed_data['status']
        if status == ContentItem.ACCEPTED:
            try:
                current_bin.add(item)
            except Bin.NotEnoughSpace:
                message = _("The chosen item exceeds the bin's "
                            "capacity and thus cannot be added to it.")
                redirect_url = request.app.get_url('queue_review')
                return template('feedback',
                                status='error',
                                page_title=_('Item unacceptable'),
                                message=message,
                                redirect_url=redirect_url,
                                redirect_target=_('review page'))
            else:
                redirect(request.app.get_url('queue_review'))
        else:
            current_bin.remove(item)
            redirect(request.app.get_url('queue_accepted'))
    return template('queue_item', form=form)


def route(conf):
    return (
        (
            '/queue/accepted/',
            'GET',
            queue_accepted,
            'queue_accepted',
            {}
        ), (
            '/queue/review/',
            'GET',
            queue_review,
            'queue_review',
            {}
        ), (
            '/queue/<item_id:re:[0-9a-f]{32}>/',
            'GET',
            queue_item,
            'queue_item',
            {}
        ), (
            '/queue/<item_id:re:[0-9a-f]{32}>/',
            'POST',
            save_queue_item,
            'save_queue_item',
            {}
        )
    )

