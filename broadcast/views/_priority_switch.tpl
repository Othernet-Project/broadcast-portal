<div class="choose-priority">
    <h1>${_('Broadcast schedule:')}</h1>
    <div class="switch">
        % if mode == 'free':
        <span class="left active free">
            <span class="icon"></span>
            ${_("Wait in line")}
        </span>
        <a href="${url('broadcast_content_details_form', item_type=item.type, item_id=item.id) + h.set_qparam(mode='priority').to_qs()}" class="right priority">
            ${_("Today (%(amount)s)") % {'amount': item.priority_price}}
        </a>
        % else:
        <a href="${url('broadcast_content_details_form', item_type=item.type, item_id=item.id) + h.set_qparam(mode='free').to_qs()}" class="left free">
            ${_("Wait in line")}
        </a>
        <span class="right active priority">
            <span class="icon"></span>
            ${_("Today (%(amount)s)") % {'amount': item.priority_price}}
        </span>
        % endif
    </div>
    <p class="priority-help">
    % if mode == 'free':
    ${_('''Your content will be reviewed by staff and broadcast at earliest
    occasion possible. This depends on total volume of content being
    submitted by other users.''')}
    % else:
    ${_('''After completing the payment, your content will be reviewed by
    Outernet staff and broadcast during Outernet's working hours (week days
    between 11am and 7pm Chicago time).''')} <br>
    <strong>
    ${_('Pricing for priority content broadcast is {price} per MB').format(price=item.unit_price)}
    </strong>
    % endif
    </p>
</div>
