<%namespace name="forms" file="/_forms.mako"/>

<form action="${url('auth:register')}" method="POST">
    ${forms.form_errors([form.error])}

    ${forms.csrf_token()}

    ${forms.field(form.username)}
    ${forms.field(form.email)}
    ${forms.field(form.password1)}
    ${forms.field(form.password2)}
    ${forms.field(form.tos_agree, label=_('I agree to the <a href="{url}#tos" target="_blank">Terms of Service</a>').format(url=url('main:terms')))}
    ${forms.field(form.priv_read, label=_('I have read the <a href="{url}#privacy" target="_blank">Privacy Policy</a>').format(url=url('main:terms')))}
    <p class="buttons">
        <button type="submit">${_('Register')}</button>
    </p>
</form>
