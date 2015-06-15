<%inherit file='base.tpl'/>

<%block name="main">
<div class="grid">
    <div class="grid-container">
        <div class="grid-row auth">
            <div class="col broadcast">
                <p>${_("A confirmation e-mail has been sent to the following e-mail address")}: ${email} . ${_("Please follow the link to complete the registration process.")}</p>
            </div>
        </div>
    </div>
</div>
</%block>
