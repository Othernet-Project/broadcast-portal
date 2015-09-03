<%inherit file='base.tpl'/>

<%block name="main">
<div class="grid">
    <div class="grid-container">
        <div class="grid-row scheduled-detail">
            <div class="col">
                <table>
                    % for name, value in item.items():
                    <tr>
                        <td>${name}</td>
                        % if name == "file_path":
                            <td><a href="http://127.0.0.1:8080/admin/content/${value}">${value}</a></td>
                        % else:
                            <td>${value}</td>
                        % endif
                    </tr>
                    % endfor
                </table>
            </div>
        </div>
    </div>
</div>
</%block>
