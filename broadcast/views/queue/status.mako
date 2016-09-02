<%inherit file="/_inner.mako"/>
<%namespace name="status" file="_status.mako"/>

<%block name="page_title">${_('Filecast queue overview')}</%block>
<%block name="body_class">status</%block>

<h1>${_('Filecast queue overview')}</h1>

<div class="float-container">
    <section id="stats" class="stats">
        ${status.body()}
        <a href="${url('queue:status')}" data-roca-target="stats" data-roca-refresh-interval="5"></a>
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
    <section id="upload" class="upload">
    <a href="${url('files:upload')}" data-roca-target="upload" data-roca-trap-submit="yes" data-roca-submit-complete-event="file-upload-complete" data-roca-refresh-on="file-upload-complete" data-roca-refresh-delay="3">
        ${_('Upload a file')}
    </a>
    </section>

    <section id="review" class="review">
    <a href="${url('queue:review')}" data-roca-target="review" data-roca-refresh-on="file-upload-complete">
        ${_('See the review queue')}
    </a>
    </section>

    <section id="candidates" class="candidates">
    <a href="${url('queue:candidates')}" data-roca-target="candidates" data-roca-refresh-on="file-upload-complete">
        ${_('See the daily filecast candidates')}
    </a>
    </section>
</div>
