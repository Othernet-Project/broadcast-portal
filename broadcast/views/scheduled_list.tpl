<%inherit file='base.tpl'/>

<%block name="main">
<div class="grid">
    <div class="grid-container">
        <div class="grid-row scheduled-list">
            <div class="col">
                % if items:
                <table>
                    <tr>
                        <th>Paid</th>
                        <th>Type</th>
                        <th>Title/Handle</th>
                        <th>E-mail</th>
                        <th>Created</th>
                        <th>Submitted content</th>
                    </tr>
                    % for item in items:
                    <tr>
                        <td><span class="
                        % if bool(item.charge_id):
                            paid-icon
                        % else:
                            unpaid-icon
                        % endif
                        "></span> </td>
                        <td><span class="${item.type}-icon"></span></td>
                        <td><a href="${url('scheduled_detail', item_type=item.type, item_id=item.id)}">
                        % if item.type == "twitter":
                            ${item.content()}
                        % else:
                            ${h.trunc(item.title, 24)}
                        % endif
                        </a></td>
                        <td>${h.trunc(item.email or '', 24)}</td>
                        <td class="datestamp">${item.created.strftime('%Y-%m-%d %H:%M')}</td>
                        <td><a href="${url('expose_content', item_type=item.type, item_id=item.id, name=item.content())}"> ${item.content()} </a></td>
                    </tr>
                    % endfor
                </table>
                % else:
                <p>${_("No items scheduled so far for broadcasting.")}</p>
                % endif
            </div>
        </div>
    </div>
</div>
</%block>
