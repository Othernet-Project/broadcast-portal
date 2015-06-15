<%inherit file="base.tpl"/>
<%namespace name='register_form' file='_register.tpl'/>

<%block name="main">
<div class="grid">
    <div class="grid-container">
        <div class="grid-row auth">
            <div class="col login">
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
                    <p>
                        <button type="submit"><span class="icon"></span> ${_('Login')}</button>
                    </p>
                </form>
            </div>
            <div class="col registration">
                ${register_form.body()}
            </div>
        </div>
    </div>
</div>
</%block>
