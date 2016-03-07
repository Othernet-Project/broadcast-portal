from bottle_utils.ajax import roca_view

from ..models.bins import Bin
from ..models.items import ContentItem
from ..util.template import template


@roca_view('bin_list', '_bin_list', template_func=template)
def bin_list():
    return dict(bins=Bin.filter(status=Bin.CLOSED))


@roca_view('bin_details', '_bin_details', template_func=template)
def bin_details(bin_id):
    return dict(bin=Bin.get(id=bin_id),
                items=ContentItem.filter(bin=bin_id))


def route(conf):
    return (
        (
            '/bins/',
            'GET',
            bin_list,
            'bin_list',
            {}
        ), (
            '/bins/<bin_id:re:[0-9a-f]{32}>/',
            'GET',
            bin_details,
            'bin_details',
            {}
        )
    )

