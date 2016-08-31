<%inherit file="/_inner.mako"/>
<%namespace name="candidates" file="_candidates.mako"/>

<%block name="page_title">${_('Filecast candidates')}</%block>

<h1>${_('Filecast candidates')}</h1>

${candidates.body()}
