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
                        <td>${value}</td>
                    </tr>
                    % endfor
                    <tr>
                        <td>Content</td>
                        <td><a href="${url('expose_content', item_type=item.type, item_id=item.id, name=item.content())}">${item.content()}</a></td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</div>
</%block>
