<p class="feedback-message feedback-${'success' if success else 'error'}">
    ${message}
</p>

<p>
    ${_('You will be redirected to {page} shortly.').format(page=h.A(url_label, href=url)) | n,unicode}
</p>
