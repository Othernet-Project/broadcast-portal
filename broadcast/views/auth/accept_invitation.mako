<%inherit file="/_inner.mako"/>
<%namespace name="accept_invitation" file="_accept_invitation.mako"/>

<h1>${_('Just one more thing')}</h1>

<section id="accept-invitation" class="accept-invitation">
<p>${_('In order to join the Filecaster community, you will need a user account.')}</p>

<div id="register-form" class="register-form">
    ${accept_invitation.body()}
</div>
</section>
