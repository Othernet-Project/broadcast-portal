<%inherit file='base.tpl'/>
<%namespace name='priority_switch' file='_priority_switch.tpl'/>

<%block name="title">
    ${_("Upload content")}
</%block>

<%block name="main">
<div class="h-bar">
    ${priority_switch.body()}
</div>
<div class="full-page-form">
    <div class="content">
        ${h.form('post', action=url('broadcast_content_details', item_type=item.type, item_id=item.id), enctype="multipart/form-data")}
            % if form.error:
            ${form.error}
            % endif
            ${csrf_tag()}
            ${form.id}
            ${form.signature}
            ${form.mode}
            <p class="field form-input-required required">
                ${form.language.label}
                ${form.language}
                % if form.language.error:
                ${form.language.error}
                % endif
            </p>
            <p class="field form-input-required form-select required">
                ${form.license.label}
                ${form.license}
                % if form.license.error:
                ${form.license.error}
                % endif
                <span class="field-help">
                ${_("Use All rights reserved if unsure. If you are the author, we recommend Creative Commons Attribution. Get more information about licenses %(link)s.") % {'link': '<a target="_blank" href="http://wiki.outernet.is/wiki/Content_license">here</a>'}}
                </span>
            </p>
            <p class="buttons">
                <button type="submit" class="primary"><span class="icon"></span> ${_('Continue')}</button>
            </p>
        </form>
    </div>
</div>
</%block>

<%block name="extra_scripts">
    <script src="${assets['js/broadcast']}"></script>
</%block>
