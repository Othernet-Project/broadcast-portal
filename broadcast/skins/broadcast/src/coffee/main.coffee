((window, $) ->
  ($ 'a[data-roca-target]').rocaLoad()

  ($ '#jump-list').on 'click', 'a', (e) ->
    e.preventDefault()
    el = $ @
    target = el.attr 'href'
    ($ target).scrollTo()

) this, this.jQuery


