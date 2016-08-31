<%inherit file="/_inner.mako"/>
<%namespace name="upload" file="_upload.mako"/>

<h1>${_('Upload a file')}</h1>

<div id="upload" class="upload">
    ${upload.body()}
</div>
