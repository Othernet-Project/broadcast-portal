<%inherit file="/_base.mako"/>
<%namespace name="feedback" file="_feedback.mako"/>

<%block name="page_title">${title}</%block>
<%block name="body_class">feedback feedback-${'success' if success else 'error'}</%block>
<%block name="extra_head">
    <meta http-equiv="refresh" content="10; url=${url}">
</%block>

<h1>${title}</h1>

${feedback.body()}
