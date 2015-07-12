<%inherit file='base.tpl'/>

<div class="h-bar h-bar-main">
    <div class="choose-broadcast-type">
        <h2>${_('What would you like to broadcast?')}</h2>
        <div class="switch">
            <a class="left content" href="${url('broadcast_content_form', item_type='content')}">${_("Content")}</a>
            <a class="center tv" href="${url('broadcast_content_form', item_type='tv')}">${_("TV")}</a>
            <a class="right twitter" href="${url('broadcast_twitter_form')}">${_("Tweets")}</a>
        </div>
    </div>
</div>
