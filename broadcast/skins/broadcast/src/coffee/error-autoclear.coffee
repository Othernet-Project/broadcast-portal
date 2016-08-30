((window, $) ->

  body = $ window.document.body

  body.on 'input', 'input, select, textarea', (e) ->
    el = $ @
    (el.siblings '.field-error-message').remove()

) this, this.jQuery
