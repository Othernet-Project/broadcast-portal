<%inherit file='skeleton.tpl'/>

<%block name="main">
    <div class="error">
        <h2>403: ${_('Authorization error')}</h2>
        <p>
        ${_('''The form you are trying to submit has expired. If you used a
        reload button to resubmit the form, please go back to the form page
        using links.''')}
        </p>
    </div>
</%block>
