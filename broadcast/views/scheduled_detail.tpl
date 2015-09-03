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
                        % if value == "file_path":
                            <td><a href="https://uplink.outernet.is/admin/scheduled/${value}>${value}</a></td>
                        % endif
                        <td>${value}</td>
                    </tr>
                    % endfor
                </table>
            </div>
        </div>
    </div>
</div>
</%block>
