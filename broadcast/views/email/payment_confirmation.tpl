<% 
if item_type in 'content':
    service = _('24-hour priority review')
elif item_type == 'twitter feed':
    service = _('Twitter feed uplink')
%>
${ _("""Dear user,

Thank you for using Outernet Uplink Center. This is a payment confirmation
message. Your card has not been charged yet, and is awaiting approval of your
%(item_type)s from staff. Please keep this email for the record:

Email: %(email)s
Card: **** %(last4digits)s
Time: %(timestamp)s GMT
Total: %(total_amount)s
Service: %(service)s
""") % {
    'email': email,
    'service': service,
    'item_type': item_type,
    'last4digits': last4digits,
    'timestamp': timestamp,
    'total_amount': total_amount
} }

% if is_subscription:
${ _("This is a %(interval)s subscription service. If you wish to unsubscribe at any moment, please contact us at hello@outernet.is.") % {'interval': interval} }
% endif

--
Outernet Team
hello@outernet.is
