<div class="choose-broadcast-type">
    <div class="tab">
        % if form.type == 'content':
        <span class="tab-link active content">${_("Files")}</span>
        <a class="tab-link twitter" href="${url('broadcast_twitter_form')}">${_("Twitter")}</a>
        % else:
        <a class="tab-link content" href="${url('broadcast_content_form')}">${_("Files")}</a>
        <span class="tab-link active twitter">${_("Twitter")}</span>
        % endif
    </div>
    <div class="clear"></div>
</div>
