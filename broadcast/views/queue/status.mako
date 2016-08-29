<%inherit file="/_base.mako"/>
<%namespace name="status" file="_status.mako"/>

<%block name="page_title">${_('Filecast queue overview')}</%block>

<h1>${_('Filecast queue overview')}</h1>

<section id="stats" class="stats">
${status.body()}
</section>

<section id="upload" class="upload">
<a href="${url('files:upload')}" data-roca-target="upload" data-roca-trap-submit="yes">
    ${_('Upload a file')}
</a>
</section>

<section id="review" class="review">
<a href="${url('queue:review')}" data-roca-target="review">
    ${_('See the review queue')}
</a>
</section>

<section id="candidates" class="candidates">
<a href="${url('queue:candidates')}" data-roca-target="candidates">
    ${_('See the daily filecast candidates')}
</a>
</section>
