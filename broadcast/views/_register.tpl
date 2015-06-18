${h.form('post', action=url('register'))}
    % if registration_form.error:
    ${registration_form.error}
    % endif

    ${csrf_tag()}
    <p class="field form-input-required">
        ${registration_form.username.label}
        ${registration_form.username}
        % if registration_form.username.error:
        ${registration_form.username.error}
        % endif
    </p>
    <p class="field form-input-required">
        ${registration_form.email.label}
        ${registration_form.email}
        % if registration_form.email.error:
        ${registration_form.email.error}
        % endif
    </p>
    <p class="field form-input-required">
        ${registration_form.password1.label}
        ${registration_form.password1}
        % if registration_form.password1.error:
        ${registration_form.password1.error}
        % endif
    </p>
    <p class="field form-input-required">
        ${registration_form.password2.label}
        ${registration_form.password2}
        % if registration_form.password2.error:
        ${registration_form.password2.error}
        % endif
    </p>
    <p class="buttons">
        <button type="submit" class="primary"><span class="icon"></span> ${_('Register')}</button>
    </p>
</form>
