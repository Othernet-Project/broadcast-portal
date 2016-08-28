((window, $, Mustache) ->

  $.templates = {}

  $.template = (name, substs) ->
    Mustache.render $.templates[name], substs

  $.fn.template = (name, substs) ->
    el = $ @
    el.html $.template name, subst

  ($ 'script[type="text/x-template"]').each () ->
    src = $ @
    html = $.trim src.html()
    id = src.attr 'id'
    Mustache.parse html
    $.templates[id] = html
    return

) this, this.jQuery, this.Mustache
