%if err.status_code == 404:
    <p class="error-message">
        ${_("Oops, there's no page here!")}
        <a href="${url('main:home')}">${_('Start from the main page.')}</a>
    </p>
%elif err.status_code == 500:
    <p class="error-message">
        ${_('This error is caused by a bug in the program. The staff has been '
        'have been notified.')}
    </p>
%else:
    <p class="error-message">${err.body}</p>
%endif

%if DEBUG and err.traceback:
    <textarea class="error-traceback">${err.traceback}</textarea>
%endif
