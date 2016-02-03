<%inherit file='base.tpl'/>
<%namespace name="forms" file="/ui/forms.tpl"/>

<%block name="title">
    ${_("Share your files")}
</%block>

<%block name="main">
<div class="full-page-form">
    <div class="content">
        ${h.form('post', action=url('broadcast_content', item_type=item_type), enctype="multipart/form-data")}
            ${forms.form_errors([form.error]) if form.error else ''}
            ${csrf_tag()}
            ${forms.field(form.id)}
            ${forms.field(form.signature)}
            ${forms.field(form.content_file)}
            ${forms.field(form.title)}
            ${forms.field(form.language)}
            ${forms.field(form.license)}
            ${forms.field(form.url)}
            ${forms.field(form.email)}
            <p class="buttons">
                <button type="submit" name="mode" value="free" class="primary"><span class="icon"></span> ${_('Share')}</button>
            </p>
            <p>${_("or")}</p>
            <p class="buttons">
                <button type="submit" name="mode" value="priority" class="primary"><span class="icon"></span> ${_('Fast Share')}</button>
            </p>
            <p>${_("Fast Share is a paid option with a one-time accelerated review fee of $5")}</p>
            <div class="progress-feedback">
                <div class="loader"></div>
                <p class="help-text">${_("Uplinking, please wait...")}</p>
            </div>
        </form>
    </div>
</div>
</%block>

<%block name="extra_scripts">
    <script src="${assets['js/broadcast']}"></script>
</%block>
