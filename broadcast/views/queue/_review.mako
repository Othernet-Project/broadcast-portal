<%namespace name="items_partial" file="_items.mako"/>
<ul class="item-list review-list">
    %for item in items:
        <li class="item review-item">
            ${items_partial.content_item(item)}
        </li>
    %endfor
</ul>
