<%namespace name="forms" file="/_forms.mako"/>

<form action="${url('auth:reset_password', key=key)}" method="POST">
    ${forms.form_errors([form.error])}

    ${forms.csrf_token()}

    ${h.HIDDEN('next', next_path) | n,unicode}
    ${h.HIDDEN('key', key) | n,unicode}

    ${forms.field(form.new_password1)}
    ${forms.field(form.new_password2)}
    <p class="buttons">
        <button type="submit">${_('Reset password')}</button>
    </p>
</form>
