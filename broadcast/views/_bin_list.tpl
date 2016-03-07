% if bins:
<table>
    <thead>
        <tr>
            <th>${_("Created")}</th>
            <th>${_("Capacity")}</th>
            <th>${_("Size")}</th>
            <th>${_("Item Count")}</th>
            <th>${_("Status")}</th>
        </tr>
    </thead>
    <tbody>
    % for bin in bins:
        <tr>
            <td class="datestamp">
                <a href="${url('bin_details', bin_id=bin.id)}">${bin.created.strftime('%b %d, %H:%M UTC')}</a>
            </td>
            <td>${h.hsize(bin.capacity)}</td>
            <td>${h.hsize(bin.size)}</td>
            <td>${bin.count}</td>
            <td class="trunc">${bin.status}</td>
        </tr>
    % endfor
    </tbody>
</table>
% else:
    <p class="noitems">${_("No bins on the list.")}</p>
% endif
