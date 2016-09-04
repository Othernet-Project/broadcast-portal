<%namespace name="forms" file="/_forms.mako"/>

<form action="${url('auth:password_reset_request')}" method="POST">
    ${forms.form_errors([form.error])}

    ${forms.csrf_token()}

    ${h.HIDDEN('next', next_path) | n,unicode}
    ${forms.field(form.email)}

    <p class="buttons">
        <button type="submit">${_('Send password reset link')}</button>
    </p>
</form>
