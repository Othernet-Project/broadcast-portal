<%namespace name="forms" file="/ui/forms.tpl"/>

${h.form('post', action=url('register'))}
    % if registration_form.error:
    ${registration_form.errors}
    % endif

    ${csrf_tag()}
    <input type="hidden" name="next" value="${next_path}">
    ${forms.field(registration_form.username, required=True)}
    % if request.user.is_anonymous:
    ${h.HIDDEN('email', request.user.email)}
    % else:
    ${forms.field(registration_form.email, required=True)}
    % endif
    ${forms.field(registration_form.password1, required=True)}
    ${forms.field(registration_form.password2, required=True)}
    ${forms.field(registration_form.tos_agree, required=True)}
    ${forms.field(registration_form.priv_read, required=True)}
    <p class="buttons">
        <button type="submit" class="primary"><span class="icon"></span> ${_('Register')}</button>
        <span class="separator">${_('or')}</span>
        <a class="button" href="${url('login') + h.set_qparam(next=next_path).to_qs()}">${_('Log in')}</a>
    </p>
</form>
