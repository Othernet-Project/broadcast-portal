<%inherit file="/_inner.mako"/>
<%namespace name="review" file="_review.mako"/>

<%block name="page_title">${_('Filecast review list')}</%block>

<h1>${_('Review list')}</h1>

${review.body()}
