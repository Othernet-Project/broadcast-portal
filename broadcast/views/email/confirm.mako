<%namespace name="signature" file="_signature.mako"/>

${ _("""Dear user,

Welcome to the Outernet Filecaster.

Please follow this link and verify your email address:

{link}
""").format(link=host_url + url('auth:reset_password', key=key))}

${signature.body()}
