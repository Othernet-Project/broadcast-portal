<%inherit file="/_inner.mako"/>
<%namespace name="register" file="_register.mako"/>

<h1>${_('Register')}</h1>

<p>${_('Please fill out the registration form below.')}</p>

<div id="register-form" class="register-form">
    ${register.body()}
</div>
