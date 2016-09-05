((window, $) ->
  win = $ window

  ($ 'a[data-roca-target]').rocaLoad()
  ($ '*[data-roca-url]').rocaConfigureContainer()

  ($ '#jump-list').on 'click', 'a', (e) ->
    e.preventDefault()
    el = $ @
    target = el.attr 'href'
    ($ target).scrollTo()

  sectionReload = (e, section) ->
    setTimeout () ->
      section.reload()
    , 7000

  win.on 'upload-submit', sectionReload
  win.on 'beta-signup-submit', sectionReload

  win.on 'state-update', (e, data) ->
    return if data.forced
    $.popup $.template 'status-update'

) this, this.jQuery


