<%inherit file='base.tpl'/>

<%block name="main">
<div class="grid">
    <div class="grid-container">
        <div class="grid-row scheduled-list">
            <div class="col">
                % if items:
                <table>
                    <tr>
                        <th>Title/Handle</th>
                        <th>Type</th>
                        <th>E-mail</th>
                        <th>Created</th>
                        <th>Charged</th>
                        <th>Submitted content</th>
                    </tr>
                    % for item in items:
                    <tr>
                        <td><a href="${url('scheduled_detail', item_type=item.type, item_id=item.id)}">
                        % if item.type == "twitter":
                            ${item.content()}
                        % else:
                            ${item.title}
                        % endif
                        </a></td>
                        <td>${item.type}</td>
                        <td>${h.trunc(item.email or '', 32)}</td>
                        <td>${item.created.strftime('%Y-%m-%d %H:%M')}</td>
                        <td>${h.yesno(item.charge_id)}</td>
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
