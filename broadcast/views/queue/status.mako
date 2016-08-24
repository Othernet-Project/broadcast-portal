<%inherit file="/_base.mako"/>
<%namespace name="status" file="_status.mako"/>

<%block name="title">${_('Filecast queue overview')}</%block>

<h1>${_('Filecast queue overview')}</h1>

<section id="stats" class="stats">
${status.body()}
</section>

<section id="review" class="review">
<a href="${url('queue:review')}">${_('See the review queue')}</a>
</section>

<section id="candidates" class="candidates">
<a href="${url('queue:review')}">${_('See the daily filecast candidates')}</a>
</section>
