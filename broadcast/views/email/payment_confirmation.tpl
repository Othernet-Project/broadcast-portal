<% 
services = {'content': _('24-hour priority review'),
            'twitter': _('Twitter feed uplink')}
verbose_types = {'twitter': _("twitter feed"),
                 'content': _("content")}
intervals = {'month': _("a monthly"),
             'year': _("an annual")}

is_subscription = stripe_object.object == 'customer'
if is_subscription:
    card = stripe_object.sources.data[-1]
    last4digits = card.last4
    subscription = stripe_object.subscriptions.data[-1]
    interval = subscription.plan.interval
    timestamp = th.from_ts(subscription.start)
    amount = subscription.plan.amount
else:
    last4digits = stripe_object.source.last4
    interval = None
    timestamp = th.from_ts(stripe_object.created)
    amount = stripe_object.amount
%>
${_("""Dear user,

Thank you for using Outernet Uplink Center. This is a payment confirmation
message. Your card has not been charged yet, and is awaiting approval of your
{item_type} from staff. Please keep this email for the record:

Email: {email}
Card: **** {last4digits}
Time: {timestamp} GMT
Total: {total_amount}
Service: {service}
""".format(email=item.email,
           service=services[item.type],
           item_type=verbose_types[item.type],
           last4digits=last4digits,
           timestamp=timestamp,
           total_amount=th.hamount(amount)))} 

% if is_subscription:
${_("This is {interval} subscription service. If you wish to unsubscribe at "
    "any moment, please contact us at hello@outernet.is.".format(
        interval=intervals[interval]
))}
% endif

--
Outernet Team
hello@outernet.is
