((window, $) ->
  MULTIPART = 'multipart/form-data'

  win = $ window
  doc = $ window.document.body

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
      el.removeData 'loading-orig-html'

  $.createSubmitFrame = (id) ->
    # Create a hidden iframe for form submission
    submitFrame = $ '<iframe></iframe>'
    submitFrame.hide()
    submitFrame.attr 'id', id
    submitFrame.attr 'name', id
    doc.append submitFrame
    submitFrame

  $.fn.makePartial = () ->
    # Append a hidden field to the selected element, that causes it to be
    # treated as XHR submission even though it may be submitted without XHR.
    el = $ @
    el.append '<input type="hidden" name="partial" value="yes">'

  $.fn.funnelSubmit = () ->
    # Causes the forms within the selected element to be submitted using XHR,
    # or hidden iframe, and results loaded within the selected element.
    el = $ @
    containerId = el.attr 'id'
    submitTarget = "#{containerId}-submit-frame"
    submitFrame = $.createSubmitFrame submitTarget

    submitFrameHandler = (e) ->
      el.html (submitFrame.contents().find 'body').html()

    submitHandler = (e) ->
      form = $ @
      if (form.attr 'enctype') is MULTIPART
        form.makePartial().attr 'target', submitTarget
        submitFrame.one 'load', submitFrameHandler
      else
        e.preventDefault()
        formData = form.serialize()
        action = (form.attr 'action') or window.location.pathname
        res = $.post action, formData
        res.done (resp) -> el.html resp
        res.fail (xhr) -> el.html xhr.responseText

    el.on 'submit', 'form', submitHandler

  $.fn.reload = (fn) ->
    el = $ @
    url = el.data 'roca-url'
    el.load (url), (res, status, xhr) ->
      switch xhr.status
        when 200
          fn?(xhr.status)
          win.trigger 'roca-load', [el]
        else
          fn?(xhr.status)
          el.cancelLoading()
          win.trigger 'roca-error', [el]
      return

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
      target.data 'roca-url', url
      target.loading().reload()
      if (el.data 'roca-trap-submit') is 'yes'
        target.funnelSubmit()

) this, this.jQuery
