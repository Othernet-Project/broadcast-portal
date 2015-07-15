<%inherit file='base.tpl'/>
<%namespace name='broadcast_switch' file='_broadcast_switch.tpl'/>

<%block name="title">
    ${_("Share Twitter feed")}
</%block>

<%block name="main">
<div class="h-bar">
    ${broadcast_switch.body()}
</div>
<div class="full-page-form">
    <div class="twitter">
        ${h.form('post', action=url('broadcast_twitter'), enctype="multipart/form-data")}
            % if form.error:
            ${form.error}
            % endif
            ${csrf_tag()}
            <p class="field form-input-required">
                ${form.handle.label}
                ${form.handle}
                % if form.handle.error:
                ${form.handle.error}
                % endif
            </p>
            <p class="field form-input-required form-select">
                ${form.plan.label}
                ${form.plan}
                % if form.plan.error:
                ${form.plan.error}
                % endif
            </p>
            <p class="buttons">
                <button type="submit" class="primary"><span class="icon"></span> ${_('Continue')}</button>
            </p>
        </form>
    </div>
</div>
</%block>
