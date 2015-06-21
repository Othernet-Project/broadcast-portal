<%inherit file="base.tpl"/>
<%namespace name='register_form' file='_register.tpl'/>

<div class="h-bar">
    <h2>${_('Get started')}</h2>
</div>
<div class="full-page-form">
    ${register_form.body()}
</div>
