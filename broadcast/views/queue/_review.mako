<%namespace name="items_partial" file="_items.mako"/>
%if request.is_xhr:
<h2>
    <span class="icon icon-edit-outline"></span>
    <span class="header-text">${_('Review list')}</span>
</h2>
%endif

<p class="notes">
    ${_('Latest uploads')}
</p>

<% count = 0 %>
<ul class="item-list review-list">
    %for item in items:
        <% 
        count += 1 
        itemcls = ''
        if item.votes < -2:
            itemcls = ' review-item-warning'
        if item.votes < -4:
            itemcls = ' review-item-alert'
        %>
        <li class="item review-item${itemcls}" id="item-${item.id}">
            ${items_partial.content_item(item)}
        </li>
    %endfor
    %if not count:
        <li class="note">
        ${_('There are no items for review right now.')}
        </li>
    %endif
</ul>
