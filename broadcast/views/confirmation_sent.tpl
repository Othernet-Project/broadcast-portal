<%inherit file='base.tpl'/>

<%block name="main">
<div class="h-bar">
    <h2>
    ${_('Check your inbox')}
    </h2>
</div>
<div class="full-page-form">
    <p class="single confirm">
    ${_("A confirmation link has been sent to %(email)s.") % {'email': email}}
    </p>
</div>
</%block>
