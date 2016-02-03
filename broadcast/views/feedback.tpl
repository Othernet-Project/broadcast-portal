<%inherit file="base.tpl"/>

<%block name="title">
${page_title}
</%block>

<div class="feedback ${status}">
    <h2>${page_title}</h2>
    <p class="main">${message}</p>
</div>
