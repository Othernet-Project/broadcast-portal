<%inherit file='base.tpl'/>
<%namespace name="forms" file="/ui/forms.tpl"/>

<%block name="title">
    ${_("Password reset")}
</%block>

<%block name="main">
    <div class="form">
        ${h.form('post', action=url('password_reset', key=form.key.value))}
            % if form.error:
            ${forms.form_errors([form.error])}
            % endif

            ${csrf_tag()}
            <input type="hidden" name="next" value="${next_path}">
            ${forms.field(form.key)}
            ${forms.field(form.new_password1, required=True)}
            ${forms.field(form.new_password2, required=True)}
            <p class="buttons">
                <button type="submit" class="primary"><span class="icon"></span> ${_('Reset password')}</button>
            </p>
        </form>
    </div>
</%block>
