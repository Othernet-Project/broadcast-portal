<%inherit file="/_base.mako"/>
<%namespace name="status" file="_status.mako"/>

<%block name="page_title">${_('Filecast queue overview')}</%block>
<%block name="body_class">status</%block>

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

<nav id="jump-list" class="jump-list">
<a href="#top">
    <span class="icon icon-arrow-up"></span>
    <span class="text-label">${_('Top')}</span>
</a>
<a href="#upload">
    <span class="icon icon-plus-outline"></span>
    <span class="text-label">${_('Upload')}</span>
</a>
<a href="#review">
    <span class="icon icon-edit-outline"></span>
    <span class="text-label">${_('Review')}</span>
</a>
<a href="#candidates">
    <span class="icon icon-ok-outline"></span>
    <span class="text-label">${_('Candidates')}</span>
</a>
</nav>
