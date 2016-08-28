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

  ($ 'a[data-roca-target]').rocaLoad()

) this, this.jQuery
