<%inherit file='base.tpl'/>
<%namespace name='priority_switch' file='_priority_switch.tpl'/>

<%block name="main">
${priority_switch.body()}

<div class="full-page-form">
    <div class="free">
        <h2>${_("Share your broadcast to skip the queue")}</h2>
    </div>
</div>
</%block>
