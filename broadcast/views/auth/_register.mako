<%namespace name="forms" file="/_forms.mako"/>

<form action="${url('auth:register')}" method="POST">
    ${forms.form_errors([form.error])}

    ${forms.csrf_token()}

    ${forms.field(form.username)}
    ${forms.field(form.email)}
    ${forms.field(form.password1)}
    ${forms.field(form.password2)}
    ${forms.field(form.tos_agree)}
    ${forms.field(form.priv_read)}
    <p class="buttons">
        <button type="submit">${_('Register')}</button>
    </p>
</form>
