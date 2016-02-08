<%inherit file='skeleton.tpl'/>

<%block name="main">
    <div class="error">
        <h2>404: ${_('Not Found')}</h2>
        <p>
        ${_('''The requested page cannot be found.''')}
        </p>
    </div>
</%block>
