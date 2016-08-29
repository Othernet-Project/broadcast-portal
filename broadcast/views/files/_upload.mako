<%namespace name="forms" file="/_forms.mako"/>

<p class="tip">
    ${_('Because of the limited bandwidth on the Outernet L-band service, '
    'upload files size is limited to {size_limit} each').format(
    size_limit=h.hsize(size_limit))}
</p>

<form action="${url('files:upload')}" method="POST" enctype="multipart/form-data">
    ${forms.form_errors([form.error])}
    ${forms.csrf_token()}
    ${forms.field(form.content_file)}
    ${forms.field(form.is_authorized)}
    <p class="buttons">
        <button type="submit">${_('Upload')}</button>
    </p>
</form>
