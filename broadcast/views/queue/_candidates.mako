<%namespace name="items_partial" file="_items.mako"/>
<ul class="item-list candidate-list">
    %for item in items:
        <li class="item candidate-item">
            ${items_partial.content_item(item)}
        </li>
    %endfor
</ul>
