<%inherit file='base.tpl'/>

<%block name="main">
<div class="full-page-form">
    <div class="confirmation-sent">
        <p>${_("A confirmation e-mail has been sent to the following e-mail address")}: ${email} . ${_("Please follow the link to complete the registration process.")}</p>
    </div>
</div>
</%block>
