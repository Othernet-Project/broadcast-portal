<%inherit file='base.tpl'/>

<%block name="main">
<div class="grid">
    <div class="grid-container">
        <div class="grid-row scheduled-list">
            <div class="col">
                % for item in items:
                    ${item}
                    ${type(item)}
                % endfor
                % if items:
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Type</th>
                        <th>E-mail</th>
                        <th>Created</th>
                        <th>Charge ID</th>
                        <th>Submitted content</th>
                    </tr>
                    % for item in items:
                    <tr>
                        <td><a href="${url('scheduled_detail', item_type=item.type, item_id=item.id)}">${item.id}</a></td>
                        <td>${item.type}</td>
                        <td>${item.email}</td>
                        <td>${item.created}</td>
                        <td>${item.charge_id}</td>
                        % if item.type == "content":
                            <td><a href="http://127.0.0.1:8080/admin/content/${item.file_path}">${item.file_path}</a></td>
                        % elif item.type == "twitter": 
                            <td><a href="http://twitter.com/${item.handle}">${item.handle}</a></td>
                        % endif
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
