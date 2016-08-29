<%inherit file="/_base.mako"/>
<%namespace name="error" file="_error.mako"/>

<%block name="page_title">${err.status}</%block>

<%block name="body_class">error</%block>

<section class="error-description">
<h1 class="error-code error-${err.status_code}">${err.status}</h1>
${error.body()}
</section>
