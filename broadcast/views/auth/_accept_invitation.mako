<%namespace name="forms" file="/_forms.mako"/>

<form action="${url('auth:accept_invitation', key=key)}" method="POST">
    ${forms.form_errors([form.error])}

    ${forms.csrf_token()}

    ${h.HIDDEN('key', key) | n,unicode}
    ${h.HIDDEN('email', email) | n,unicode}

    ${forms.field(form.username, required=True)}
    ${forms.field(form.password1, required=True)}
    ${forms.field(form.password2, required=True)}
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
