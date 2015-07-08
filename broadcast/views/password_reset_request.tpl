<%inherit file='base.tpl'/>

<%block name="title">
    ${_("Password reset")}
</%block>

<%block name="main">
<div class="full-page-form">
    <div class="password-reset-request">
        ${h.form('post', action=url('password_reset_request'))}
            % if form.error:
            ${form.error}
            % endif
            ${csrf_tag()}
            <input type="hidden" name="next" value="${next_path}">
            <p>
                ${form.email.label}
                ${form.email}
                % if form.email.error:
                ${form.email.error}
                % endif
            </p>
            <p class="buttons">
                <button type="submit" class="primary"><span class="icon"></span> ${_('Send password reset link')}</button>
            </p>
        </form>
    </div>
</div>
</%block>
