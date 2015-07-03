<%inherit file='base.tpl'/>
<%namespace name='priority_switch' file='_priority_switch.tpl'/>

<div class="h-bar">
    ${priority_switch.body()}
</div>

<div class="full-page-form">
    <div class="free center">
        <a class="button" href="${url('broadcast_content_form')}">
            <span class="icon"></span> ${_('Broadcast something else')}
        </a>
        </p>
    </div>
</div>
