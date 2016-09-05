<%namespace name="forms" file="/_forms.mako"/>

<form action="${url('auth:accept_invitation', key=key)}" method="POST">
    ${forms.form_errors([form.error])}

    ${forms.csrf_token()}

    ${h.HIDDEN('key', key) | n,unicode}
    ${h.HIDDEN('email', email) | n,unicode}

    ${forms.field(form.username, required=True)}
    ${forms.field(form.password1, required=True)}
    ${forms.field(form.password2, required=True)}
    ${forms.field(form.tos_agree, required=True)}
    ${forms.field(form.priv_read, required=True)}
    <p class="buttons">
        <button type="submit">${_('Register')}</button>
    </p>
</form>
