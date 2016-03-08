<%inherit file='base.tpl'/>
<%namespace name="item_list" file="_item_list.tpl"/>

<%block name="main">
    <div class="bin-heading">
        <h1 class="title">${_("Bin Details")}</h1>
        <div class="bin-info-display">
            <span class="line">${_("Current bin size: {size} / {usage}%".format(size=h.hsize(bin.size), usage=round(bin.usage, 2)))}</span>
            <br />
            <span class="line">${_("Broadcast date: {time}".format(time=th.hdatetime(bin.closes)))}</span>
        </div>
        <span class="bin-usage-bar light">
            <span class="bin-usage-bar-indicator" style="width: ${bin.usage}%"></span>
        </span>
    </div>

    <div class="bin">
        <div class="items">
            ${item_list.body()}
        </div>
    </div>
</%block>

