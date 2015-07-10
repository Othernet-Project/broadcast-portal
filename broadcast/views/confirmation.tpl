<%inherit file='base.tpl'/>

<%block name="title">
    ${_("Confirmation")}
</%block>

<%block name="main">
<div class="full-page-form">
    <div class="confirm">
        ${h.form('post', action=url('send_confirmation'))}
            % if form.error:
            ${form.error}
            % endif
            ${csrf_tag()}
            <p>
                ${form.email.label}
                ${form.email}
                % if form.email.error:
                ${form.email.error}
                % endif
            </p>
            <p class="buttons">
                <button type="submit" class="primary"><span class="icon"></span> ${_('Send confirmation')}</button>
            </p>
        </form>
    </div>
</div>
</%block>
