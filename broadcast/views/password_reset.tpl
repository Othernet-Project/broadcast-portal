<%inherit file='base.tpl'/>

<%block name="main">
<div class="full-page-form">
    <div class="confirm">
        ${h.form('post', action=url('send_confirmation'))}
            % if form.error:
            ${form.error}
            % endif
            ${csrf_tag()}
            ${form.key}
            <p class="field form-input-required">
                ${registration_form.new_password1.label}
                ${registration_form.new_password1}
                % if registration_form.new_password1.error:
                ${registration_form.new_password1.error}
                % endif
            </p>
            <p class="field form-input-required">
                ${registration_form.new_password2.label}
                ${registration_form.new_password2}
                % if registration_form.new_password2.error:
                ${registration_form.new_password2.error}
                % endif
            </p>
            <p class="buttons">
                <button type="submit" class="primary"><span class="icon"></span> ${_('Reset password')}</button>
            </p>
        </form>
    </div>
</div>
</%block>
