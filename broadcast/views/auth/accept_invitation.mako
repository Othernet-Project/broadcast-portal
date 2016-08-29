<%inherit file="/_base.mako"/>
<%namespace name="accept_invitation" file="_accept_invitation.mako"/>

<h1>${_('Just one more thing')}</h1>

<p>${_('In order to join the Filecast center community, you will need a user account.')}</p>

<div id="register-form" class="register-form">
    ${accept_invitation.body()}
</div>
