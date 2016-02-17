<%inherit file='base.tpl'/>
<%namespace name="forms" file="/ui/forms.tpl"/>

<%block name="title">
    ${_("Password reset")}
</%block>

<%block name="main">
    <div class="form">
        ${h.form('post', action=url('password_reset_request'))}
            % if form.error:
            ${forms.form_errors([form.error])}
            % endif

            ${csrf_tag()}
            <input type="hidden" name="next" value="${next_path}">
            ${forms.field(form.email, required=True)}
            <p class="buttons">
                <button type="submit" class="primary"><span class="icon"></span> ${_('Send password reset link')}</button>
            </p>
        </form>
    </div>
</%block>
