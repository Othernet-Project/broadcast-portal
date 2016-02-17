<%inherit file='base.tpl'/>
<%namespace name="forms" file="/ui/forms.tpl"/>

<%block name="title">
    ${_("Confirmation")}
</%block>

<%block name="main">
    <div class="form">
        ${h.form('post', action=url('send_confirmation'))}
            % if form.error:
            ${form.error}
            % endif

            ${csrf_tag()}
            ${forms.field(form.email, required=True)}
            <p class="buttons">
                <button type="submit" class="primary"><span class="icon"></span> ${_('Send confirmation')}</button>
            </p>
        </form>
    </div>
</%block>
