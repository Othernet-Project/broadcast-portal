<%inherit file='skeleton.tpl'/>

<%block name="main">
<div class="h-bar">
    <h2>404: ${_('Not Found')}</h2>
</div>
<div class="full-page-form">
    <p class="single error">
    ${_('''The requested page cannot be found.''')}
    </p>
</div>
</%block>
