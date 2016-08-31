<%namespace name="signature" file="_signature.mako"/>

${ _("""Dear user,
Thank you registering at the Outernet Filecast Center.

In order to complete the registration, please follow this link and verify your
email address:
    %(link)s
""") % {'link': host_url + url('auth:confirm_email', key=key)} }

${signature.body()}
