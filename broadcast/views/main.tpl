<%inherit file='base.tpl'/>

<div class="hero">
    <div class="overlay">
        <h2>${_('File sharing from space')}</h2>
        <p class="buttons">
            <a class="button" href="${url('broadcast_content_form', item_type='content')}">${_("Share your files")}</a>
            <a class="button" href="${url('broadcast_twitter_form')}">${_("Share your tweets")}</a>
        </p>
        <p>${_("Share your favorite files with the world. Broadcast your blog posts, documents, music, and videos from six geostationary satellites.")}</p>
    </div>
</div>
