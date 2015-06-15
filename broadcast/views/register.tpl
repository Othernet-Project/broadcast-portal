<%inherit file="base.tpl"/>
<%namespace name='register_form' file='_register.tpl'/>

<%block name="main">
<div class="grid">
    <div class="grid-container">
        <div class="grid-row register">
            <div class="col">
                ${register_form.body()}
            </div>
        </div>
    </div>
</div>
</%block>
