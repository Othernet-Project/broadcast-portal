<%inherit file="base.tpl"/>
<%namespace name='register_form' file='_register.tpl'/>

<%block name="main">
<div class="full-page-form">
    <div class="register">
        ${register_form.body()}
    </div>
</div>
</%block>
