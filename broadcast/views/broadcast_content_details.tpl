<%inherit file='base.tpl'/>

<%block name="title">
    ${_("Upload content")}
</%block>

<%block name="main">
<div class="h-bar">
    <h1>${_('Uplink schedule')}</h1>
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
            <p class="field">
                ${form.email.label}
                ${form.email}
                % if form.email.error:
                ${form.email.error}
                % endif
            </p>
            <div class="buttons">
                <div class="left">
                    <button type="submit" class="primary" name="mode" value="priority"><span class="icon"></span> ${_("Today (%(amount)s)") % {'amount': item.priority_price}}</button>
                    <p class="help">${_("After completing the payment, your content will be reviewed by Outernet staff and uplinked during Outernet's business hours (Monday-Friday 0900-1700 PDT).")}
                        <br />
                        <strong>${_('Pricing for priority content uplinked is {price}/MB').format(price=item.unit_price)}</strong>
                    </p>
                </div><div class="right">
                    <button type="submit" class="secondary" name="mode" value="free"><span class="icon"></span> ${_("Wait in line")}</button>
                    <p class="help">${_('Your content will be reviewed by staff and uplinked at earliest occasion possible. This depends on total volume of content being submitted by other users.')}</p>
                </div>
            </div>
        </form>
    </div>
</div>
</%block>
