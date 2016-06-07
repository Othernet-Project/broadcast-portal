% if items:
<table>
    <thead>
        <tr>
            <th>${_("Submitted")}</th>
            <th>${_("Download")}</th>
            <th>${_("Title")}</th>
            <th>${_("Source")}</th>
            <th>${_("License")}</th>
            <th>${_("Size")}</th>
            % if bin.is_open and queue_type == REVIEW_QUEUE:
                <th>${_("Flags")}</th>
            % endif
            % if bin.is_open and request.user.is_in_group('superuser'):
                <th>${_("Action")}</th>
            % endif
        </tr>
    </thead>
    <tbody>
    % for item in items:
        <tr>
            <td class="datestamp">${th.hdatetime(item.created)}</td>
            <td class="download">
                <a href="${url('download_queue_item', item_id=item.id, filename=item.filename)}"></a>
            </td>
            <td class="trunc">${item.title or 'n/a'}</td>
            <td class="trunc">${item.url or 'n/a'}</td>
            <td class="trunc">${item.license or 'n/a'}</td>
            <td class="trunc">${h.hsize(item.size)}</td>
            % if bin.is_open and queue_type == REVIEW_QUEUE:
                <td class="trunc">
                    % if item.is_rejected:
                        <span class="flagged">!</span>
                    % endif
                </td>
            % endif
            % if bin.is_open and request.user.is_in_group('superuser'):
            <td class="action">
                ${h.form('post', action=h.full_url(path=url('save_queue_item', item_id=item.id)))}
                    <button type="submit" name="queue_type" value="${hidden_queue_type}">
                        % if hidden_queue_type == 'accepted':
                            +
                        % else:
                            -
                        % endif
                    </button>
                </form>
            </td>
            % endif
        </tr>
    % endfor
    </tbody>
</table>
% else:
    <p class="noitems">${_("No items on the list.")}</p>
% endif
