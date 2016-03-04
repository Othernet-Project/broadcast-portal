from bottle import request, redirect, abort
from bottle_utils.ajax import roca_view
from bottle_utils.i18n import dummy_gettext as _

from ..forms.queue import QueueItemForm, ACCEPTED_QUEUE, REVIEW_QUEUE
from ..models.bins import Bin
from ..models.items import ContentItem
from ..util.auth.decorators import login_required
from ..util.template import template


@roca_view('queue_list', '_queue_list', template_func=template)
def queue_list():
    query = request.params.get('query', '')
    query_args = {'title__like': query} if query else {}
    queue_type = request.params.get('type')
    current_bin = Bin.current()
    if queue_type == ACCEPTED_QUEUE:
        items = ContentItem.filter(status=ContentItem.ACCEPTED,
                                   bin=current_bin.id,
                                   **query_args)
    elif queue_type == REVIEW_QUEUE:
        processing = ContentItem.filter(status=ContentItem.PROCESSING,
                                        bin=None,
                                        **query_args)
        rejected = ContentItem.filter(status=ContentItem.REJECTED,
                                      bin=None,
                                      **query_args)
        items = sorted(processing + rejected, key=lambda x: x.created)
    else:
        redirect(request.app.get_url('queue_list', type=ACCEPTED_QUEUE))

    hidden_queue_type = (ACCEPTED_QUEUE,
                         REVIEW_QUEUE)[queue_type == ACCEPTED_QUEUE]
    return dict(bin=current_bin,
                items=items,
                queue_type=queue_type,
                hidden_queue_type=hidden_queue_type,
                query=query,
                ACCEPTED_QUEUE=ACCEPTED_QUEUE,
                REVIEW_QUEUE=REVIEW_QUEUE)


@roca_view('queue_item', '_queue_item', template_func=template)
def queue_item(item_id):
    try:
        item = ContentItem.get(id=item_id)
    except ContentItem.DoesNotExist:
        abort(404, _("The requested item was not found."))
    else:
        return dict(item=item)


@login_required(groups='superuser')
def save_queue_item(item_id):
    form = QueueItemForm(request.forms)
    if form.is_valid():
        current_bin = Bin.current()
        queue_type = form.processed_data['queue_type']
        target_bin = None if queue_type == ACCEPTED_QUEUE else current_bin.id
        try:
            item = ContentItem.get(id=item_id, bin=target_bin)
        except ContentItem.DoesNotExist:
            abort(404, _("The specified item is no longer modifiable."))

        if queue_type == ACCEPTED_QUEUE:
            try:
                current_bin.add(item)
            except Bin.NotEnoughSpace:
                message = _("The chosen item exceeds the bin's "
                            "capacity and thus cannot be added to it.")
                redirect_url = request.app.get_url('queue_list',
                                                   type=REVIEW_QUEUE)
                return template('feedback',
                                status='error',
                                page_title=_('Item unacceptable'),
                                message=message,
                                redirect_url=redirect_url,
                                redirect_target=_('review page'))
            else:
                redirect(request.app.get_url('queue_list', type=REVIEW_QUEUE))
        current_bin.remove(item)
        redirect(request.app.get_url('queue_list', type=ACCEPTED_QUEUE))
    return template('queue_item', form=form, item=None)


def route(conf):
    return (
        (
            '/queue/',
            'GET',
            queue_list,
            'queue_list',
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

