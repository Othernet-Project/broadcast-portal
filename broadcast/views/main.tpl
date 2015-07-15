<%inherit file='base.tpl'/>

<div class="h-bar h-bar-main">
    <div class="choose-broadcast-type">
        <h2>${_('What would you like to share from space?')}</h2>
        <div class="switch">
            % if item_type == 'content':
            <span class="left active content"><span class="icon"></span> ${_("Content")}</span>
            <a class="center tv" href="${url('main') + h.set_qparam(item_type='tv').to_qs()}">${_("TV")}</a>
            <a class="right twitter" href="${url('main') + h.set_qparam(item_type='twitter').to_qs()}">${_("Tweets")}</a>
            % elif item_type == 'tv':
            <a class="left content" href="${url('main') + h.set_qparam(item_type='content').to_qs()}">${_("Content")}</a>
            <span class="center active tv"><span class="icon"></span> ${_("TV")}</span>
            <a class="right twitter" href="${url('main') + h.set_qparam(item_type='twitter').to_qs()}">${_("Tweets")}</a>
            % elif item_type == 'twitter':
            <a class="left content" href="${url('main') + h.set_qparam(item_type='content').to_qs()}">${_("Content")}</a>
            <a class="center tv" href="${url('main') + h.set_qparam(item_type='tv').to_qs()}">${_("TV")}</a>
            <span class="right active twitter"><span class="icon"></span> ${_("Tweets")}</span>
            % else:
            <a class="left content" href="${url('main') + h.set_qparam(item_type='content').to_qs()}">${_("Content")}</a>
            <a class="center tv" href="${url('main') + h.set_qparam(item_type='tv').to_qs()}">${_("TV")}</a>
            <a class="right twitter" href="${url('main') + h.set_qparam(item_type='twitter').to_qs()}">${_("Tweets")}</a>
            % endif
        </div>
    </div>
</div>

<div class="full-page-form main">
    % if item_type == 'content':
    <p>${_("Submit podcasts, PDF files, or other information of your choosing.")}</p>
    <p class="buttons">
        <a class="button primary" href="${url('broadcast_content_form', item_type='content')}">${_("Continue")}</a>
    </p>
    % elif item_type == 'tv':
    <p>${_("Place high-quality public domain or Creative Commons videos on the Outernet TV channel, which airs on <a href="https://wiki.outernet.is/wiki/Coverage_and_transponder_settings">IS-10</a>.")}</p>
    <p class="buttons">
        <a class="button primary" href="${url('broadcast_content_form', item_type='tv')}">${_("Continue")}</a>
    </p>
    % elif item_type == 'twitter':
    <p>${_("Send your tweets to the far corners of the world. We take your Twitter feed and regularly uplink them to our <a href="https://wiki.outernet.is/wiki/Coverage_and_transponder_settings">global satellite network.</a>")}</p>
    <p class="buttons">
        <a class="button primary" href="${url('broadcast_twitter_form')}">${_("Continue")}</a>
    </p>
    % else:
    <p>${_("Share your favorite content with the world.  Fill Outernet's library in space with your favorite ebooks, applications, blog posts, and videos. Help us collect news, information, and education to share with the entire world. Content uploaded through the Uplink Center will be transmitted over a network of <a href="https://wiki.outernet.is/wiki/Coverage_and_transponder_settings">7 geostationary satellites.</a>")}</p>
    % endif
</div>
