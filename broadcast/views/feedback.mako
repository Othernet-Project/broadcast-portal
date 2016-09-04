<%inherit file="/_inner.mako"/>
<%namespace name="feedback" file="_feedback.mako"/>

<%block name="page_title">${title}</%block>
<%block name="body_class">default feedback-${'success' if success else 'error'}</%block>
<%block name="extra_head">
    <meta http-equiv="refresh" content="${pause}; url=${redirect_url}">
</%block>

<h1>
    %if success:
        <span class="icon icon-ok-outline"></span>
    %else:
        <span class="icon icon-alert-outline"></span>
    %endif
    <span class="heading-text">${title}</span>
</h1>

<section id="feedback" class="feedback">
${feedback.body()}

<p>
    ${_('You will be redirected to {page} shortly.').format(page=h.A(url_label, href=redirect_url)) | n,unicode}
</p>
</section>
