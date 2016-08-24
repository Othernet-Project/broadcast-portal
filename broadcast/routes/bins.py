from bottle import abort
from bottle_utils.ajax import roca_view
from bottle_utils.i18n import dummy_gettext as _

from ..models.bins import Bin
from ..models.items import ContentItem
from ..util.template import render as template


@roca_view('bin_list', '_bin_list', template_func=template)
def bin_list():
    return dict(bins=Bin.filter(status=Bin.CLOSED))


@roca_view('bin_details', '_bin_details', template_func=template)
def bin_details(bin_id):
    try:
        bin = Bin.get(id=bin_id)
    except Bin.DoesNotExist:
        abort(404, _("Invalid bin id specified."))
    else:
        if bin.is_open:
            abort(404, _("Invalid bin id specified."))
        return dict(bin=bin, items=ContentItem.filter(bin=bin_id))


def route():
    return tuple()
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
