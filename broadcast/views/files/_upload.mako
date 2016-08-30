<%namespace name="forms" file="/_forms.mako"/>

%if request.is_xhr:
    <h2>
        <span class="icon icon-plus-outline"></span>
        ${_('Add files')}
    </h2>
%endif

<form action="${url('files:upload')}" method="POST" enctype="multipart/form-data">
    ${forms.form_errors([form.error])}
    ${forms.csrf_token()}
    ${forms.field(form.content_file, help=_('Max {size_limit}').format(size_limit=h.hsize(size_limit)))}
    ${forms.field(form.is_authorized)}
    <p class="buttons">
        <button type="submit">${_('Upload')}</button>
    </p>
</form>
