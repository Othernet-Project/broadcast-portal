from bottle_utils.ajax import roca_view

from ..util.broadcast import ContentItem, filter_items
from ..util.template import template, view


@roca_view('queue_list', '_accepted_list', template_func=template)
def queue_accepted():
    accepted = filter_items(ContentItem.type, status=ContentItem.ACCEPTED)
    return dict(accepted=accepted)


@roca_view('queue_list', '_processing_list', template_func=template)
def queue_processing():
    processing = filter_items(ContentItem.type, status=ContentItem.PROCESSING)
    return dict(processing=processing)


@view('queue_detail')
def queue_detail(item_id):
    return {}


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
            queue_detail,
            'queue_detail',
            {}
        )
    )

