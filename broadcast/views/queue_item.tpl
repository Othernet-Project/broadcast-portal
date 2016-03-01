<%inherit file='base.tpl'/>
<%namespace name="queue_item" file="_queue_item.tpl"/>

<%block name="main">
    ${queue_item.body()}
</%block>
