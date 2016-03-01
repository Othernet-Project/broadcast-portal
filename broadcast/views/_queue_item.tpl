<dl class="queue-item">
    <dt>${_("ID")}</dt>
    <dd>${item.id}</dd>

    <dt>${_("Created")}</dt>
    <dd>${item.created.strftime('%b %d, %H:%M UTC')}</dd>

    <dt>${_("Size")}</dt>
    <dd>${h.hsize(item.size)}</dd>

    <dt>${_("Title")}</dt>
    <dd>${item.title}</dd>

    <dt>${_("Source")}</dt>
    <dd>${item.url}</dd>

    <dt>${_("License")}</dt>
    <dd>${item.license}</dd>

    <dt>${_("Language")}</dt>
    <dd>${item.language}</dd>

    <dt>${_("Status")}</dt>
    <dd>${item.status}</dd>
</dl>
