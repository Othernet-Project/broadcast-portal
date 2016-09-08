<%inherit file="/_inner.mako"/>
<%namespace name="moderator" file="_moderator.mako"/>

<%block name="page_title">${_('Welcome, new filecast moderator!')}</%block>

<%block name="body_class">default narrow</%block>

<h1>
    <span class="icon icon-user-shield"></span>
    <span>${_('Welcome, moderator!')}</span>
</h1>

<section id="moderator" class="moderator">
${moderator.body()}
</section>
