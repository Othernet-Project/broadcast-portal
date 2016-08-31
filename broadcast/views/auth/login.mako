<%inherit file="/_inner.mako"/>
<%namespace name="login" file="_login.mako"/>

<h1>${_('Log in')}</h1>

<div id="login-form" class="login-form">
    ${login.body()}
</div>
