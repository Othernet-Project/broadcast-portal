<%namespace name="signature" file="_signature.mako"/>

${ _("""Dear user,
Welcome to the Outernet Filecast Center.

Please follow this link and verify your email address:
    %(link)s
""") % {'link': host_url + url('auth:confirm_email', key=key)} }

${signature.body()}
