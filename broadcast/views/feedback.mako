<%inherit file="/_base.mako"/>
<%namespace name="feedback" file="_feedback.mako"/>

<%block name="page_title">${title}</%block>
<%block name="body_class">feedback feedback-${'success' if success else 'error'}</%block>
<%block name="extra_head">
    <meta http-equiv="refresh" content="${pause}; url=${url}">
</%block>

<h1>${title}</h1>

${feedback.body()}

<p>
    ${_('You will be redirected to {page} shortly.').format(page=h.A(url_label, href=url)) | n,unicode}
</p>
