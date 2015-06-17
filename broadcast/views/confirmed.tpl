<%inherit file='base.tpl'/>

<%block name="main">
<div class="grid">
    <div class="grid-container">
        <div class="grid-row auth">
            <div class="col broadcast">
                % if error:
                    <p class="error">${error}</p>
                % else:
                    <p>${_("E-mail address successfully confirmed. Proceed to the login page.")}</p>
                    <a href="${url('login')}">${_("Login")}</a>
                % endif
            </div>
        </div>
    </div>
</div>
</%block>