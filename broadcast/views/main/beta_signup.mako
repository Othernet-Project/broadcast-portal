<%inherit file="/_inner.mako"/>
<%namespace name="beta_signup" file="_beta_signup.mako"/>

<h1>${_('Sign up for closed beta')}</h1>

<div class="beta-signup-form">
    ${beta_signup.body()}
</div>
