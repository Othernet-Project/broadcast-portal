<%inherit file='base.tpl'/>
<%namespace name='broadcast_switch' file='_broadcast_switch.tpl'/>

<%block name="main">
<div class="full-page-form">
    ${broadcast_switch.body()}
    <div class="content">
        ${h.form('post', action=url('broadcast_content'), enctype="multipart/form-data")}
            % if form.error:
            ${form.error}
            % endif
            ${csrf_tag()}
            ${form.id}
            ${form.signature}
            <p class="field form-input-required form-input-file">
                ${form.content_file.label}
                ${form.content_file}
                <span class="field-help">
                Package your content into a zip file containing at least a 
                single HTML page.
                </span>
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
                ${_("Use All rights reserved if unusure. If you are the author, we recommend Creative Commons Attribution")}
                </span>
            </p>
            <p class="field form-input-required content-url required">
                ${form.url.label}
                ${form.url}
                % if form.url.error:
                ${form.url.error}
                % endif
                <span class="field-help preview" data-prefix="${url_prefix}">${url_prefix}</span>
                <span class="field-help">${_("This will be the direct link to your content on Outernet. It's similar to a regular internet link. You are free to use any URL provided that it only consists of letters (a-z), numbers (0-9), dashes (-), underscores (_) and slashes (/).")}</span>
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
