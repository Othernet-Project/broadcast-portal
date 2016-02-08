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
            ${forms.field(form.handle, help=_("Your Twitter handle/username. You cannot use another person's handle/username unless you have their permission to do so."), required=True)}
            ${forms.field(form.plan, help=_("All payments are recurring (auto-renewed). If you want to cancel your plan later, please email us."), required=True)}
            <p class="buttons">
                <button type="submit" class="primary"><span class="icon"></span> ${_('Share')}</button>
            </p>
        </form>
    </div>
</%block>
