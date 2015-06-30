${ _("""Dear user,

You're receiving this e-mail because you or someone else has requested a password reset using your email address.
It can be safely ignored if you did not request it.


Click the link below to reset your password:

    %(link)s

--
Outernet Team
hello@outernet.is
""") % {'link': host_url + url('password_reset', key=reset_key)} }
