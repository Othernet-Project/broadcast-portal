<%namespace name="signature" file="_signature.mako"/>

${ _("""Dear user,
You're receiving this e-mail because you or someone else has requested a password reset using your email address.
It can be safely ignored if you did not request it.
Click the link below to reset your password:
    %(link)s
""") % {'link': host_url + url('auth:reset_password', key=key)} }

${signature.body()}
