<%inherit file='base.tpl'/>

<%block name="main">
<div class="grid">
    <div class="grid-container">
        <div class="grid-row priority">
            <div class="col">
                <h2>${_("Priority broadcast has been successfully scheduled.")}</h2>
                <a href="${url('main')}">${_("Return to homepage")}</a>
            </div>
        </div>
    </div>
</div>
</%block>
