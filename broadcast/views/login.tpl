<%inherit file="base.tpl"/>
<%namespace name='register_form' file='_register.tpl'/>

<div class="h-bar">
    <h2>${_('Log in')}</h2>
</div>
<div class="full-page-form">
    <div class="login">
        ${h.form('post', action=url('login'))}
            % if login_form.error:
            ${login_form.error}
            % endif

            ${csrf_tag()}
            <input type="hidden" name="next" value="${next_path}">
            <p class="field form-input-required">
                ${login_form.username.label}
                ${login_form.username}
                % if login_form.username.error:
                ${login_form.username.error}
                % endif
            </p>
            <p class="field form-input-required">
                ${login_form.password.label}
                ${login_form.password}
                % if login_form.password.error:
                ${login_form.password.error}
                % endif
            </p>
            <p class="buttons">
                <button type="submit" class="primary"><span class="icon"></span> ${_('Log in')}</button>
                ## Translators, appears as separator between Login button and
                ## Register now button.
                ${_('or')}
                <a class="button" href="${url('register')}">${_("Register now")}</a>
            </p>
            <p class="help">
                <a href="${url('password_reset_request')}">${_("Forgot your password?")}</a>
            </p>
            <p class="help">
                <a href="${url('send_confirmation_form')}">${_("Didn't receive the confirmation e-mail?")}</a>
            </p>
        </form>
    </div>
</div>
