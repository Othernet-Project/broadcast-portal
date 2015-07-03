${ _("""Dear user,

Thank you registering at the Outernet Broadcast Center.

In order to complete the registration, please follow this link and verify your
email address:

    %(link)s

--
Outernet Team
hello@outernet.is
""") % {'link': host_url + url('confirm', key=confirmation_key) + '?next=' + next_path} }
