<%inherit file='base.tpl'/>

<%block name="main">
<div class="grid">
    <div class="grid-container">
        <div class="grid-row scheduled-list">
            <div class="col">
                % if items:
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Type</th>
                        <th>E-mail</th>
                        <th>Created</th>
                        <th>Charge ID</th>
                    </tr>
                    % for item in items:
                    <tr>
                        <td><a href="${url('scheduled_detail', item_type=item.type, item_id=item.id)}">${item.id}</a></td>
                        <td>${item.type}</td>
                        <td>${item.email}</td>
                        <td>${item.created}</td>
                        <td>${item.charge_id}</td>
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
