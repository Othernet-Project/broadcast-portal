<%inherit file='base.tpl'/>
<%namespace name='broadcast_switch' file='_broadcast_switch.tpl'/>

<%block name="title">
    ${_("Upload content")}
</%block>

<%block name="main">
<div class="h-bar">
    ${broadcast_switch.body()}
</div>
<div class="full-page-form">
    <div class="content">
        ${h.form('post', action=url('broadcast_content', item_type=item_type), enctype="multipart/form-data")}
            % if form.error:
            ${form.error}
            % endif
            ${csrf_tag()}
            ${form.id}
            ${form.signature}
            <p class="field form-input-required form-input-file">
                ${form.content_file.label}
                ${form.content_file}
                <span class="field-help">${_("The file should not be larger than %(limit)s" % {'limit': size_limit})}</span>
                % if form.content_file.error:
                ${form.content_file.error}
                % endif
            </p>
            <p class="field form-input-required required">
                ${form.title.label}
                ${form.title}
                % if form.title.error:
                ${form.title.error}
                % endif
            </p>
            <p class="field">
                ${form.language.label}
                ${form.language}
                % if form.language.error:
                ${form.language.error}
                % endif
            </p>
            <p class="buttons">
                <button type="submit" class="primary"><span class="icon"></span> ${_('Continue')}</button>
            </p>
            <div class="progress-feedback">
                <div class="loader"></div>
                <p class="help-text">${_("Uplinking to teleport, please wait...")}</p>
            </div>
        </form>
    </div>
</div>
</%block>

<%block name="extra_scripts">
    <script src="${assets['js/broadcast']}"></script>
</%block>
