<%namespace name="forms" file="/_forms.mako"/>

%if request.is_xhr:
    <h2>${_('Join the filecaster community')}</h2>
%endif

<form action="${url('auth:register')}" method="POST">
    ${forms.form_errors([form.error])}

    ${forms.csrf_token()}

    ${forms.field(form.username)}
    ${forms.field(form.email)}
    <%
        legal_url = url('main:terms')
        tos = h.A(_("Terms"), href=legal_url + '#tos', target="_blank")
        priv = h.A(_("Privacy Policy"), href=legal_url + '#privacy', target="_blank")
    %>
    <p>${_('By registering an account, you agree to our {tos} and {priv}').format(tos=tos, priv=priv) | n,unicode}</p>
    <p class="buttons">
        <button type="submit">${_('Register')}</button>
    </p>
</form>
