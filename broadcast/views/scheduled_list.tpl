<%inherit file='base.tpl'/>

<%block name="main">
    <div class="submissions">
        % if items:
            <table>
                <thead>
                    <tr>
                        <th>Paid</th>
                        <th>Type</th>
                        <th>Created</th>
                        <th>Title/Handle</th>
                        <th>E-mail</th>
                        <th>Submitted content</th>
                    </tr>
                </thead>
                <tbody>
                    % for item in items:
                    <tr${' class="paid-submission"' if item.charge_id else ''}>
                        <td>
                            <span class="${'paid' if item.charge_id else 'unpaid'}"></span>
                        </td>
                        <td><span class="${item.type}-icon"></span></td>
                        <td class="datestamp">${item.created.strftime('%b %d, %H:%M UTC')}</td>
                        <td class="trunc"><a href="${url('scheduled_detail', item_type=item.type, item_id=item.id)}">
                        % if item.type == "twitter":
                            ${item.content()}
                        % else:
                            ${item.title or 'n/a'}
                        % endif
                        </a></td>
                        <td class="trunc">${item.email}</td>
                        <td class="trunc"><a href="${url('expose_content', item_type=item.type, item_id=item.id, name=item.content())}"> ${item.content()} </a></td>
                    </tr>
                % endfor
                </tbody>
            </table>
        % else:
        <p>${_("No items scheduled so far for broadcasting.")}</p>
        % endif
    </div>
</%block>
