<%inherit file='base.tpl'/>

<%block name="main">
<div class="full-page-form">
    <div class="password-reset">
        ${h.form('post', action=url('password_reset', key=form.key.value))}
            % if form.error:
            ${form.error}
            % endif
            ${csrf_tag()}
            ${form.key}
            <p class="field form-input-required">
                ${form.new_password1.label}
                ${form.new_password1}
                % if form.new_password1.error:
                ${form.new_password1.error}
                % endif
            </p>
            <p class="field form-input-required">
                ${form.new_password2.label}
                ${form.new_password2}
                % if form.new_password2.error:
                ${form.new_password2.error}
                % endif
            </p>
            <p class="buttons">
                <button type="submit" class="primary"><span class="icon"></span> ${_('Reset password')}</button>
            </p>
        </form>
    </div>
</div>
</%block>
