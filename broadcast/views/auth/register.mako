<%inherit file="/_inner.mako"/>
<%namespace name="register" file="_register.mako"/>

<h1>${_('Register')}</h1>

<section id="register-form" class="register-form">
<p>${_('Please fill out the registration form below.')}</p>
${register.body()}
</section>
