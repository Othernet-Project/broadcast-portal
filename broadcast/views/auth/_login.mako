<%namespace name="forms" file="/_forms.mako"/>

<form action="${url('auth:login')}" method="POST">
    ${forms.form_errors([form.error])}

    ${forms.csrf_token()}

    ${h.HIDDEN('next', request.params.get('next', url('main:home'))) |n,unicode}
    ${forms.field(form.username)}
    ${forms.field(form.password)}
    <p class="buttons">
        <button type="submit">${_('Log in')}</button>
    </p>
    <p>
        <a href="${url('auth:password_reset_request')}">${_("Forgot your password?")}</a>
    </p>
    <p>
        <a href="${url('auth:resend_confirmation')}">${_("Didn't receive the confirmation e-mail?")}</a>
    </p>
</form>
