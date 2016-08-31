<%namespace name="forms" file="/_forms.mako"/>

<form action="${url('auth:login')}" method="POST">
    ${forms.form_errors([form.error])}

    ${forms.csrf_token()}

    ${forms.field(form.username)}
    ${forms.field(form.password)}
    <p class="buttons">
        <button type="submit">${_('Log in')}</button>
        ${_('or')}
        <a class="button" href="${url('auth:register') + h.set_qparam(next=next_path).to_qs()}">${_("Register now")}</a>
    </p>
    <p class="help">
        <a href="${url('auth:password_reset_request') + h.set_qparam(next=next_path).to_qs()}">${_("Forgot your password?")}</a>
        <a href="${url('auth:resend_confirmation')}">${_("Didn't receive the confirmation e-mail?")}</a>
    </p>
</form>
