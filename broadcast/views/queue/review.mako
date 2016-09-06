<%inherit file="/_inner.mako"/>
<%namespace name="review" file="_review.mako"/>

<%block name="page_title">${_('Filecast latest uploads')}</%block>

<h1>${_('Latest uploads')}</h1>

${review.body()}
