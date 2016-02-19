% if accepted:
<table>
    <thead>
        <tr>
            <th>${_("Submitted")}</th>
            <th>${_("Title")}</th>
            <th>${_("Source")}</th>
            <th>${_("License")}</th>
            <th>${_("Size")}</th>
        </tr>
    </thead>
    <tbody>
    % for item in accepted:
        <tr>
            <td class="datestamp">${item.created.strftime('%b %d, %H:%M UTC')}</td>
            <td class="trunc">
                <a href="${url('queue_detail', item_id=item.id)}">${item.title or 'n/a'}</a>
            </td>
            <td class="trunc">${item.url}</td>
            <td class="trunc">${item.license}</td>
            <td class="trunc">${item.file_size}</td>
        </tr>
    % endfor
    </tbody>
</table>
% else:
<p>${_("No accepted items so far.")}</p>
% endif
