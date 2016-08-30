<script id="loading" type="text/x-template">
    <div class="loading">
        <span class="loading-text">
            ${_('Loading...')}
        </span>
    </div>
</script>

<script id="popup" type="text/x-template">
    <div class="popup">
        <div class="popup-body">
            {{&message}}
        </div>
        <a class="popup-close" href="javascript:void(0);">
            <span class="text-label">${_('close')}</span>
            <span class="icon icon-close"></span>
        </a>
    </div>
</script>

<script id="vote-success" type="text/x-template">
    <span class="icon icon-ok-outline"></span>
    ${_('Your vote was saved')}
</script>

<script id="vote-fail" type="text/x-template">
    <span class="icon icon-alert-stop"></span>
    ${_('Your vote could not be saved')}
</script>
