((window, $, Mustache) ->

  $.templates = {}

  $.template = (name, ctx) ->
    Mustache.render $.templates[name], ctx

  $.fn.template = (name, ctx) ->
    el = $ @
    el.html $.template name, ctx

  ($ 'script[type="text/x-template"]').each () ->
    src = $ @
    html = $.trim src.html()
    id = src.attr 'id'
    Mustache.parse html
    $.templates[id] = html
    return

) this, this.jQuery, this.Mustache
