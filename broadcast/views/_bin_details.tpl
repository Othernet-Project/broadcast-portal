% if items:
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
    % for item in items:
        <tr>
            <td class="datestamp">${th.hdatetime(item.created)}</td>
            <td class="trunc">
                <% download_url = url('download_queue_item', item_id=item.id, filename=item.filename) %>
                <a href="${download_url}">${item.title or 'n/a'}</a>
            </td>
            <td class="trunc">${item.url or 'n/a'}</td>
            <td class="trunc">${item.license or 'n/a'}</td>
            <td class="trunc">${h.hsize(item.size)}</td>
        </tr>
    % endfor
    </tbody>
</table>
% else:
    <p class="noitems">${_("No items on the list.")}</p>
% endif
