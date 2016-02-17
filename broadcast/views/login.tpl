<%inherit file="base.tpl"/>
<%namespace name="forms" file="/ui/forms.tpl"/>
<%namespace name='register_form' file='_register.tpl'/>

<%block name="title">
    ${_("Login")}
</%block>

<%block name="main">
    <div class="form">
        <h2>${_('Log in')}</h2>
        ${h.form('post', action=url('login'))}
            % if login_form.error:
            ${forms.form_errors([login_form.error])}
            % endif

            ${csrf_tag()}
            <input type="hidden" name="next" value="${next_path}">
            ${forms.field(login_form.username, required=True)}
            ${forms.field(login_form.password, required=True)}
            <p class="buttons">
                <button type="submit" class="primary"><span class="icon"></span> ${_('Log in')}</button>
                ## Translators, appears as separator between Login button and
                ## Register now button.
                <span class="separator">${_('or')}</span>
                <a class="button" href="${url('register') + h.set_qparam(next=next_path).to_qs()}">${_("Register now")}</a>
            </p>
            <div class="form-help">
                <h3>${_("Can't access your account?")}</h3>
                <p class="help">
                    <a href="${url('password_reset_request') + h.set_qparam(next=next_path).to_qs()}">${_("Forgot your password?")}</a>
                </p>
                <p class="help">
                    <a href="${url('send_confirmation_form')}">${_("Didn't receive the confirmation e-mail?")}</a>
                </p>
            </div>
        </form>
    </div>
</%block>
