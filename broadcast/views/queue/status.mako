<%inherit file="/_inner.mako"/>
<%namespace name="status" file="_status.mako"/>

<%block name="page_title">${_('Filecast queue overview')}</%block>
<%block name="body_class">status</%block>

<h1>${_('Filecast queue overview')}</h1>

<div class="float-container">
    <section id="stats" class="stats" data-roca-url="${url('queue:status')}" data-roca-refresh-on="state-update">
        ${status.body()}
    </section>

    <section id="info" class="info">
    <h2>
        <span class="icon icon-info"></span>
        <span class="heading-text">${_('Filecast queues')}</span>
    </h2>
    <p>
        ${_('The candidates are chosen by moderator vote, and the top-voted files '
        'that fit the daily bandwidth quota are selected for the daily filecast '
        'queue every midnight UTC.')}
    </p>
    </section>
</div>

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

<div class="float-container">
    <section id="upload" class="upload" data-roca-trap-submit="yes">
    <a href="${url('files:upload')}" data-roca-target="upload">
        ${_('Upload a file')}
    </a>
    </section>

    <section id="review" class="review" data-roca-refresh-on="state-update">
    <a href="${url('queue:review')}" data-roca-target="review">
        ${_('See the review queue')}
    </a>
    </section>

    <section id="candidates" class="candidates" data-roca-refresh-on="state-update">
    <a href="${url('queue:candidates')}" data-roca-target="candidates">
        ${_('See the daily filecast candidates')}
    </a>
    </section>
</div>
