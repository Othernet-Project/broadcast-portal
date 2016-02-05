<%inherit file='base.tpl'/>
<%namespace name="forms" file="/ui/forms.tpl"/>

<%block name="title">
    ${_("Share your tweets")}
</%block>

<%block name="main">
    <div class="form">
        <h2>${_('Share your tweets')}</h2>
        ${h.form('post', action=url('broadcast_twitter'), enctype="multipart/form-data")}
            ${forms.form_errors([form.error]) if form.error else ''}
            ${csrf_tag()}
            ${forms.field(form.handle)}
            ${forms.field(form.plan)}
            <p class="buttons">
                <button type="submit" class="primary"><span class="icon"></span> ${_('Share')}</button>
            </p>
        </form>
    </div>
</%block>
