<%inherit file='base.tpl'/>

<%block name="main">
    <div class="submissions">
        <table>
            % for name, value in item.items():
            <tr>
                <th>${name.replace('_', ' ')}</th>
                % if name == 'status':
                    <td>
                        <span class="${'paid' if item.charge_id else 'unpaid'}"></span>
                    </td>
                % else:
                    <td>${value}</td>
                % endif
            </tr>
            % endfor
            <tr>
                <th>Content</th>
                <td><a href="${url('expose_content', item_type=item.type, item_id=item.id, name=item.content())}">${item.content()}</a></td>
            </tr>
        </table>
    </div>
</%block>
