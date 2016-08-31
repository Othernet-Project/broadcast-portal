<%inherit file="/_inner.mako"/>
<%namespace name="password_reset_request" file="_password_reset_request.mako"/>

<h1>${_('Password Reset')}</h1>

<section id="password-reset-request-form" class="password-reset-request-form">
    ${password_reset_request.body()}
</section>
