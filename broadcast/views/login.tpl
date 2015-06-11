<%inherit file="base.tpl"/>

<%block name="main">
${h.form('post')}
    % if form.error:
    ${form.error}
    % endif

    ${csrf_tag()}
    <input type="hidden" name="next" value="${next_path}">
    <p>
        ${form.username.label}
        ${form.username}
        % if form.username.error:
        ${form.username.error}
        % endif
    </p>
    <p>
        ${form.password.label}
        ${form.password}
        % if form.password.error:
        ${form.password.error}
        % endif
    </p>
    <p>
        <button type="submit"><span class="icon"></span> ${_('Login')}</button>
    </p>
</form>
</%block>
