<%inherit file='skeleton.tpl'/>

<%block name="main">
<div class="h-bar">
    <h2>500: ${_('Application error')}</h2>
</div>
<div class="full-page-form">
    <p class="single error">
    ${_('''An unexpected error occurred.''')}
    </p>
</div>
</%block>
