import math

import stripe

from bottle import request
from bottle_utils.i18n import dummy_gettext as _

from ..util.basemodel import Model
from .items import BaseItem


def rounded_megabytes(size):
    return int(math.ceil(float(size) / 1024 / 1024))


class Charge(Model):
    database = 'main'
    table = 'charges'
    columns = (
        'id',
        'charged_at',
        'captured_at',
        'plan',
        'item_id',
        'item_type',
    )
    pk_field = 'id'

    @property
    def is_executed(self):
        return self.id is not None and self.charged_at is not None

    def _fetch_item(self):
        item_cls = BaseItem.cast(self.item_type)
        return item_cls.get(id=self.item_id)

    def _match_price(self, price_map):
        for pair in price_map:
            (plan, price) = pair.split(':')
            if plan == self.plan:
                return int(price)
        raise KeyError('No plan found for {}'.format(self.plan))

    def _get_human_context(self, item):
        context_generators = {
            'content': lambda item: {
                'hsize': '{} MB'.format(rounded_megabytes(item.size)),
            },
            'twitter': lambda item: {},
        }
        return context_generators.get(item.type, lambda item: {})(item)

    def _charge(self, token, price, currency, description):
        try:
            return stripe.Charge.create(amount=price,
                                        currency=currency,
                                        source=token,
                                        capture=False,
                                        description=description)
        except stripe.error.CardError as exc:
            raise self.Error(exc.message)
        except Exception:
            raise self.Error(_("Payment processing failed."))

    def _subscribe(self, token, plan, email):
        try:
            return stripe.Customer.create(source=token,
                                          plan=plan,
                                          email=email)
        except Exception:
            raise self.Error(_("Subscription to the chosen plan failed."))

    def execute(self, token, item=None, config=None):
        item = item or self._fetch_item()
        config = config or request.app.config
        stripe.api_key = config['stripe.secret_key']
        subscription_key = '{}.subscription_plans'.format(item.type)
        if self.plan in config.get(subscription_key, []):
            stripe_object = self._subscribe(token, self.plan, item.email)
        else:
            price_map = config['{}.prices'.format(item.type)]
            price = self._match_price(price_map)
            desc_template = config['{}.description_template'.format(item.type)]
            context = self._get_human_context()
            context.update(self.to_native())
            context.update(item.to_native())
            description = desc_template.format(**context)
            currency = config['charge.currency']
            stripe_object = self._charge(token, price, currency, description)

        self.update(id=stripe_object.id, charged_at=stripe_object.created)
        return stripe_object

