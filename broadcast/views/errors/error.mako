<%inherit file="/_base.mako"/>

<%block name="page_title">${err.status}</%block>

<%block name="body_class">error</%block>

<section class="error-description">
<h1 class="error-code error-${err.status_code}">${err.status}</h1>
%if err.status_code == 404:
    <p class="error-message">
        ${_("Oops, there's no page here!")}
        <a href="${url('main:home')}">${_('Start from the main page.')}</a>
    </p>
%elif err.status_code == 500:
    <p>${_('Sorry! Filecast center tripped and fell on its head. The '
        'staff has been notified.')}</p>
%else:
    <p class="error-message">${err.body}</p>
%endif

%if DEBUG and err.traceback:
    <textarea class="error-traceback">${err.traceback}</textarea>
%endif
</section>
