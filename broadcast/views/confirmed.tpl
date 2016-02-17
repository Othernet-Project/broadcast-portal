<%inherit file='base.tpl'/>

<%block name="title">
    ${_("Confirmation")}
</%block>

<%block name="main">
<div class="form">
    <div class="confirmed">
        % if error:
            <p class="error">${error}</p>
        % else:
            <p>${_("E-mail address successfully confirmed. Proceed to the login page.")}</p>
            <p class="buttons">
                <a class="button primary" href="${url('login')}">${_("Login")}</a>
            </p>
        % endif
    </div>
</div>
</%block>
