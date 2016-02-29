from bottle_utils import form
from bottle_utils.i18n import lazy_gettext as _


ACCEPTED_QUEUE = 'accepted'
REVIEW_QUEUE = 'review'
QUEUE_TYPES = (
    (ACCEPTED_QUEUE, _("Accepted")),
    (REVIEW_QUEUE, _("Review")),
)


class QueueItemForm(form.Form):
    queue_type = form.SelectField(
        # Translators, used as label for item queue type field
        _("Queue type"),
        choices=QUEUE_TYPES,
        validators=[form.Required()]
    )

