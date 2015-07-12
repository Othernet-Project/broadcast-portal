<%inherit file='base.tpl'/>

<%block name="title">
    ${_("Upload content")}
</%block>

<%block name="main">
<div class="h-bar">
    <h1>${_('Broadcast schedule')}</h1>
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
            <div class="buttons">
                <div class="left">
                    <button type="submit" class="primary" name="mode" value="priority"><span class="icon"></span> ${_("Today (%(amount)s)") % {'amount': item.priority_price}}</button>
                    <p class="help">${_("After completing the payment, your content will be reviewed by Outernet staff and broadcast during Outernet's working hours (week days between 11am and 7pm Chicago time)")}
                        <br />
                        <strong>${_('Pricing for priority content broadcast is {price} per MB').format(price=item.unit_price)}</strong>
                    </p>
                </div><div class="right">
                    <button type="submit" class="secondary" name="mode" value="free"><span class="icon"></span> ${_("Wait in line")}</button>
                    <p class="help">${_('Your content will be reviewed by staff and broadcast at earliest occasion possible. This depends on total volume of content being submitted by other users.')}</p>
                </div>
            </div>
        </form>
    </div>
</div>
</%block>

<%block name="extra_scripts">
    <script src="${assets['js/broadcast']}"></script>
</%block>
