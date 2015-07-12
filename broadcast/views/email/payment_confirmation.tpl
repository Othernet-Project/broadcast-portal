${ _("""Dear user,

Thank you for using Outernet Broadcast Center. This is a payment confirmation message. Your card has not been charged yet, and is awaiting approval of your %(item_type)s from staff. Please keep this email for the record:

Email: %(email)s
Card: **** %(last4digits)s
Time: %(timestamp)s GMT
Total: %(total_amount)s
Service: %(item_type)s broadcast
""") % {'email': email,
        'item_type': item_type,
        'last4digits': last4digits,
        'timestamp': timestamp,
        'total_amount': total_amount} }

% if is_subscription:
${ _("This is a %(interval)s subscription service. If you wish to unsubscribe at any moment, please contact us at hello@outernet.is.") % {'interval': interval} }
% endif

--
Outernet Team
hello@outernet.is
