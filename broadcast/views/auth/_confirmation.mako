<%namespace name="forms" file="/_forms.mako"/>

<form action="${url('auth:resend_confirmation')}" method="POST">
    ${forms.form_errors([form.error])}

    ${forms.csrf_token()}

    ${forms.field(form.email)}

    <p class="buttons">
        <button type="submit">${_('Send confirmation')}</button>
    </p>
</form>
