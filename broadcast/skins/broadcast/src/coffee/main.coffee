((window, $) ->
  win = $ window

  ($ 'a[data-roca-target]').rocaLoad()
  ($ '*[data-roca-url]').rocaConfigureContainer()

  ($ '#jump-list').on 'click', 'a', (e) ->
    e.preventDefault()
    el = $ @
    target = el.attr 'href'
    ($ target).scrollTo()

  win.on 'upload-submit', (e, uploadSection) ->
    setTimeout () ->
      uploadSection.reload()
    , 7000

  win.on 'state-update', (e) ->
    $.popup $.template 'status-update'

) this, this.jQuery


