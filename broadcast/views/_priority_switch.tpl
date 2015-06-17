<div class="grid">
    <div class="grid-container">
        <div class="grid-row choose-priority">
            <div class="col">
                <h1><strong>${_("All done!")}</strong> We expect to broadcast your file(s) around:</h1>
                <div class="switch-priority">
                    % if mode == 'free':
                    <span class="free">${_("I'm ok with waiting!")}</span>
                    <a href="${url('broadcast_priority_form', item_type=item.type, item_id=item.id)}" class="priority">${_("Broadcast today for only %s") % item.priority_price}</a>
                    % else:
                    <a href="${url('broadcast_free_form', item_type=item.type, item_id=item.id)}" class="free">${_("I'm ok with waiting!")}</a>
                    <span class="priority">${_("Broadcast today for only %s") % item.priority_price}</span>
                    % endif
                </div>
            </div>
        </div>
    </div>
</div>
