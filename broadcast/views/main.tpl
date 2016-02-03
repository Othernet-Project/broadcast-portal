<%inherit file='base.tpl'/>

<div class="h-bar h-bar-main">
    <div class="choose-broadcast-type">
        <h2>${_('File sharing from space')}</h2>
        <div class="help-text">
            <p class="buttons">
                <a class="button primary" href="${url('broadcast_content_form', item_type='content')}">${_("Share your files")}</a>
                <a class="button primary" href="${url('broadcast_twitter_form')}">${_("Share your tweets")}</a>
            </p>
            <p>${_("Share your favorite content with the world.  Fill Outernet's library in space with your favorite ebooks, applications, blog posts, and videos. Help us collect news, information, and education to share with the entire world. Content uploaded through the Uplink Center may be transmitted over a network of %(link)s.") % {'link': '<a href="https://wiki.outernet.is/wiki/Coverage_and_transponder_settings">7 geostationary satellites</a>'}}</p>
        </div>
    </div>
</div>
