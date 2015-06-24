<%inherit file="base.tpl"/>
<%namespace name='register_form' file='_register.tpl'/>
<%namespace name='messages' file='_messages.tpl'/>

<div class="h-bar">
    <h2>${_('Get started')}</h2>
</div>
<div class="full-page-form" data-url="${url('check_available')}" id="register-form">
    ${register_form.body()}
</div>

<%block name="extra_scripts">
${messages.messages(registration_form)}
<script type="text/javascript">
    window.pwlen = ${registration_form.min_password_length};
</script>
<script src="${assets['js/accounts']}"></script>
</%block>
