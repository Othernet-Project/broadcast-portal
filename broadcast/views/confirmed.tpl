<%inherit file='base.tpl'/>

<%block name="main">
% if error:
    <p class="error">${error}</p>
% else:
    <p>${_("E-mail address successfully confirmed. Proceed to the login page.")}</p>
    <a href="${url('login')}">${_("Login")}</a>
% endif

</%block>
