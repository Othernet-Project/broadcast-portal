<%inherit file='base.tpl'/>

<div class="hero">
    <div class="overlay">
        <h2>${_('File sharing from space')}</h2>
        <p class="buttons">
            <a class="button" href="${url('broadcast_content_form', item_type='content')}">${_("Share your files")}</a>
        </p>
        <p class="blurb">${_("Share your favorite files with the world. Broadcast your blog posts, documents, music, and videos from six geostationary satellites.")}</p>
        <div class="daily-bin">
            <h3 class="bin-usage-data">${_("Daily bin: {size} / {usage}%".format(size=h.hsize(bin.size), usage=round(bin.usage, 2)))}</h3>
            <span class="bin-usage-bar">
                <span class="bin-usage-bar-indicator" style="width: ${bin.usage}%"></span>
            </span>
            <p>
                <a class="button" href="${url('queue_list', type='accepted')}">${_("See the bin")}</a>
            </p>
            <p class="previous-bins">
                <a href="${url('bin_list')}">${_("See previous bins")}</a>
            </p>
        </div>
    </div>
</div>
