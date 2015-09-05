<div class="choose-broadcast-type">
    <h2>${_('What would you like to share from space?')}</h2>
    <div class="switch">
        % if form.type == 'content':
        <span class="left active content"><span class="icon"></span> ${_("Content")}</span>
        <a class="right twitter" href="${url('broadcast_twitter_form')}">${_("Tweets")}</a>
        % else:
        <a class="left content" href="${url('broadcast_content_form', item_type='content')}">${_("Content")}</a>
        <span class="right active twitter"><span class="icon"></span> ${_("Tweets")}</span>
        % endif
    </div>
</div>
