<%namespace name="forms" file="/_forms.mako"/>

<form action="${url('feedback:submit')}" method="POST">
    ${forms.form_errors([form.error])}
    ${forms.csrf_token()}
    %if request.user.is_guest:
    ${forms.field(form.email)}
    %endif
    ${forms.field(form.message, required=True)}
    <p class="buttons">
        <button type="submit">${_('Send')}</button>
    </p>
</form>

