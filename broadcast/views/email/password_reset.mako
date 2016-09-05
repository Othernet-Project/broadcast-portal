<%namespace name="signature" file="_signature.mako"/>

${ _("""Dear user,

You are receiving this e-mail because you (or someone else using your email)
has requested a password reset. It can be safely ignored if you did not request
it.

Please follow the link below to reset your password:

{link}
""").format(link=host_url + url('auth:reset_password', key=key))}

${signature.body()}
