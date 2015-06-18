<div class="h-bar">
    <div class="choose-priority">
        <h1><strong>${_("All done!")}</strong> We expect to broadcast your file(s) around:</h1>
        <div class="switch">
            % if mode == 'free':
            <span class="left active free"><span class="icon"></span>${_("I'm ok with waiting!")}</span>
            <a href="${url('broadcast_priority_form', item_type=item.type, item_id=item.id)}" class="right priority"><span class="icon"></span>${_("Broadcast today for only %s") % item.priority_price}</a>
            % else:
            <a href="${url('broadcast_free_form', item_type=item.type, item_id=item.id)}" class="left free"><span class="icon"></span>${_("I'm ok with waiting!")}</a>
            <span class="right active priority"><span class="icon"></span>${_("Broadcast today for only %s") % item.priority_price}</span>
            % endif
        </div>
    </div>
</div>
