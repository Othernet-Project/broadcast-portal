<%inherit file="/_inner.mako"/>
<%namespace name="reset_password" file="_reset_password.mako"/>

<h1>${_('Set Your Password')}</h1>

<section id="reset-password-form" class="reset-password-form">
    ${reset_password.body()}
</section>
