from bottle_utils import form
from bottle_utils.i18n import lazy_gettext as _

from ..util.broadcast import ContentItem


STATUSES = (
    (ContentItem.ACCEPTED, _("Accepted")),
    (ContentItem.PROCESSING, _("Processing")),
    (ContentItem.REJECTED, _("Rejected")),
)


class QueueItemForm(form.Form):
    status = form.SelectField(
        # Translators, used as label for item status field
        _("Status"),
        choices=STATUSES,
        validators=[form.Required()]
    )

