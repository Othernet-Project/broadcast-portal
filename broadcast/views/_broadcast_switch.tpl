<div class="grid">
    <div class="grid-container">
        <div class="grid-row choose-broadcast-type">
            <div class="col">
                <div class="switch-broadcast-type">
                    % if form.type == 'content':
                    <span class="content">${_("Files")}</span>
                    <a href="${url('broadcast_twitter_form')}" class="priority">${_("Twitter")}</a>
                    % else:
                    <a href="${url('broadcast_content_form')}" class="priority">${_("Files")}</a>
                    <span class="content">${_("Twitter")}</span>
                    % endif
                </div>
            </div>
        </div>
    </div>
</div>
