<%inherit file='base.tpl'/>
<%namespace name='priority_switch' file='_priority_switch.tpl'/>

${priority_switch.body()}

<div class="full-page-form">
    <div class="free">
        <p>
        ${_('''Your content will be reviewed by staff and broadcast at earliest
        occasion possible. This depends on total volume of content being
        submitted by other users.''')}
        </p>
        <p>
        <a class="button primary" href="${url('broadcast_content_form')}">
            ${_('Broadcast something else')}
        </a>
        </p>
    </div>
</div>
