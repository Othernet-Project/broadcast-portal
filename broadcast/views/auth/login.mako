<%inherit file="/_inner.mako"/>
<%namespace name="login" file="_login.mako"/>

<%block name="page_title">${_('Log in')}</%block>

<h1>${_('Log in')}</h1>

<section id="login-form" class="login-form">
${login.body()}
</section>
