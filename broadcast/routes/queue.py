from bottle import request, redirect
from bottle_utils.ajax import roca_view
from bottle_utils.csrf import csrf_token, csrf_protect

from ..forms.queue import QueueItemForm
from ..util.auth import login_required
from ..util.broadcast import ContentItem, filter_items, get_item
from ..util.template import template, view


@csrf_token
@roca_view('queue_list', '_accepted_list', template_func=template)
def queue_accepted():
    accepted = filter_items(ContentItem.type, status=ContentItem.ACCEPTED)
    return dict(accepted=accepted)


@csrf_token
@roca_view('queue_list', '_processing_list', template_func=template)
def queue_processing():
    processing = filter_items(ContentItem.type, status=ContentItem.PROCESSING)
    return dict(processing=processing)


@view('queue_item')
def queue_item(item_id):
    return {}


@csrf_protect
@view('queue_item')
@login_required(superuser_only=True)
def save_queue_item(item_id):
    form = QueueItemForm(request.forms)
    if form.is_valid():
        status = form.processed_data['status']
        item = get_item(ContentItem.type, id=item_id)
        item.update(status=status)
        if status == ContentItem.ACCEPTED:
            url = request.app.get_url('queue_accepted')
        else:
            url = request.app.get_url('queue_processing')
        redirect(url)
    return dict(form=form)


def route(conf):
    return (
        (
            '/queue/accepted/',
            'GET',
            queue_accepted,
            'queue_accepted',
            {}
        ), (
            '/queue/processing/',
            'GET',
            queue_processing,
            'queue_processing',
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

