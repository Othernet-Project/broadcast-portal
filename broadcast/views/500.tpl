<%inherit file='skeleton.tpl'/>

<%block name="main">
    <div class="error">
        <h2>500: ${_('Application error')}</h2>
        <p>
        ${_('''An unexpected error occurred.''')}
        </p>
    </div>
</%block>
