% if processing:
<table>
    <thead>
        <tr>
            <th>${_("Submitted")}</th>
            <th>${_("Title")}</th>
            <th>${_("Source")}</th>
            <th>${_("License")}</th>
            <th>${_("Size")}</th>
            % if request.user.is_superuser:
            <th>${_("Accept")}</th>
            % endif
        </tr>
    </thead>
    <tbody>
    % for item in processing:
        <tr>
            <td class="datestamp">${item.created.strftime('%b %d, %H:%M UTC')}</td>
            <td class="trunc">
                <a href="${url('queue_item', item_id=item.id)}">${item.title or 'n/a'}</a>
            </td>
            <td class="trunc">${item.url}</td>
            <td class="trunc">${item.license}</td>
            <td class="trunc">${item.file_size}</td>
            % if request.user.is_superuser:
            <td>
                ${h.form('post', action=url('save_queue_item', item_id=item.id))}
                    ${csrf_tag()}
                    <button type="submit" name="status" value="${item.ACCEPTED}"></button>
                </form>
            </td>
            % endif
        </tr>
    % endfor
    </tbody>
</table>
% else:
<p>${_("No items waiting for review.")}</p>
% endif
