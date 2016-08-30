<%namespace name="items_partial" file="_items.mako"/>
%if request.is_xhr:
<h2>
    <span class="icon icon-ok-outline"></span>
    ${_('Filecast candidates')}
</h2>
%endif
<% count = 0 %>
<ul class="item-list candidate-list">
    %for item in items:
        <% count += 1 %>
        <li class="item candidate-item" id="item-${item.id}">
            ${items_partial.content_item(item)}
        </li>
    %endfor
    %if not count:
        <li class="note">
        ${_('There are no candidates right now.')}
        </li>
    %endif
</ul>
