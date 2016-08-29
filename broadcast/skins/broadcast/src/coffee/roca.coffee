((window, $) ->
  win = $ window

  $.fn.loading = () ->
    el = $ @
    el.each () ->
      el = $ @
      el.data 'loading-orig-html', el.html()
      el.html $.template 'loading'

  $.fn.cancelLoading = () ->
    el = $ @
    el.each () ->
      origHtml = el.data 'loading-orig-html'
      if not origHtml
        return
      el.html origHtml

  $.fn.funnelSubmit = () ->
    # Causes the forms within the selected element to be submitted using XHR,
    # and results loaded within the selected element.
    el = $ @

    el.on 'submit', 'form', (e) ->
      e.preventDefault()
      form = $ @
      formData = form.serialize()
      action = (form.attr 'action') or window.location.pathname
      res = $.post action, formData
      res.done (resp) -> el.html resp
      res.fail (xhr) -> el.html xhr.responseText

  $.fn.rocaLoad = () ->
    # Load content from the URL pointed to by elements' `href` attribute into
    # target specified by the `data-roca-target` attribute.
    el = $ @
    el.each () ->
      el = $ @
      url = el.attr 'href'
      target = $ "##{el.data 'roca-target'}"
      if not target.length
        return
      target.loading().load (url), (res, status, xhr) ->
        switch xhr.status
          when 200
            win.trigger 'roca-load', [el, target]
          else
            ($ target).cancelLoading()
            win.trigger 'roca-error', [el, target]
        return
      if (el.data 'roca-trap-submit') is 'yes'
        target.funnelSubmit()


  ($ 'a[data-roca-target]').rocaLoad()

) this, this.jQuery
