<div class="h-bar">
    <div class="choose-priority">
        <h1>${_('Broadcast schedule:')}</h1>
        <div class="switch">
            % if mode == 'free':
            <span class="left active free">
                <span class="icon"></span>
                ${_("Wait in line")}
            </span>
            <a href="${url('broadcast_priority_form', item_type=item.type, item_id=item.id)}" class="right priority">
                ${_("Today (%(amount)s)") % {'amount': item.priority_price}}
            </a>
            % else:
            <a href="${url('broadcast_free_form', item_type=item.type, item_id=item.id)}" class="left free">
                ${_("Wait in line")}
            </a>
            <span class="right active priority">
                <span class="icon"></span>
                ${_("Today (%(amount)s)") % {'amount': item.priority_price}}
            </span>
            % endif
        </div>
    </div>
</div>
