<%inherit file='base.tpl'/>
<%namespace name="forms" file="/ui/forms.tpl"/>

<%block name="title">
    ${_("Share your files")}
</%block>

<%block name="main">
    <div class="form">
        <h2>${_('Share your files')}</h2>
        ${h.form('post', action=url('broadcast_content', item_type=item_type), enctype="multipart/form-data")}
            ${forms.form_errors([form.error]) if form.error else ''}
            ${csrf_tag()}
            ${forms.field(form.id)}
            ${forms.field(form.signature)}
            <div class="file">
                ${forms.field(form.content_file)}
            </div>
            ${forms.field(form.title)}
            ${forms.field(form.language)}
            ${forms.field(form.is_authorized)}
            ${forms.field(form.license)}
            ${forms.field(form.url)}
            % if request.user.is_authenticated:
            ${h.HIDDEN('email', request.user.email)}
            % else:
            ${forms.field(form.email)}
            % endif
            <p class="buttons">
                <button type="submit" name="mode" value="free" class="primary"><span class="icon"></span> ${_('Share')}</button>
                <span class="separator">${_("or")}</span>
                <button type="submit" name="mode" value="priority" class="primary"><span class="icon"></span> ${_('Rocket Share')}</button>
                <span class="field-help-message">${_("Rocket share is a paid option with a one-time accelerated review fee of $5")}</span>
            </p>
        </form>
    </div>
</%block>

<%block name="extra_scripts">
    <script src="${assets['js/broadcast']}"></script>
</%block>
