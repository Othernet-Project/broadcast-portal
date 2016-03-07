% if bins:
<table>
    <thead>
        <tr>
            <th>${_("Created")}</th>
            <th>${_("Closes")}</th>
            <th>${_("Capacity")}</th>
            <th>${_("Size")}</th>
            <th>${_("Item Count")}</th>
            <th>${_("Status")}</th>
            <th>${_("Contents")}</th>
        </tr>
    </thead>
    <tbody>
    % for bin in bins:
        <tr>
            <td class="datestamp">${bin.created.strftime('%b %d, %H:%M UTC')}</td>
            <td class="datestamp">${bin.closes.strftime('%b %d, %H:%M UTC')}</td>
            <td>${h.hsize(bin.capacity)}</td>
            <td>${h.hsize(bin.size)}</td>
            <td>${bin.count}</td>
            <td class="trunc">${bin.status}</td>
            <td class="trunc">
                <a href="${url('bin_details', bin_id=bin.id)}">${_("Contents")}</a>
            </td>
        </tr>
    % endfor
    </tbody>
</table>
% else:
    <p class="noitems">${_("No bins on the list.")}</p>
% endif
