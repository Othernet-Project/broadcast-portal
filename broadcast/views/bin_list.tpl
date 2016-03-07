<%inherit file='base.tpl'/>
<%namespace name="bin_list" file="_bin_list.tpl"/>

<%block name="main">
    <div class="bin-heading">
        <h1 class="title">${_("Bin List")}</h1>
    </div>

    <div class="bin">
        <div class="items">
            ${bin_list.body()}
        </div>
    </div>
</%block>

