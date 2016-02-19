((window, $, templates) ->
  'use strict'

  queues = $ '.queue'
  handles = $ '.handles a.handle'

  loadData = (url, container) ->
    res = $.get url
    res.done (data) ->
      container.html(data)
    res.fail () ->
      container.html(templates.queueLoadError)
    return res

  handles.on 'click', (e) ->
    e.preventDefault()
    elem = $ @
    target = elem.data 'target'
    container = queues.filter('.' + target)
    if container.hasClass 'hidden'
      url = elem.attr 'href'
      queues.addClass 'hidden'
      container.removeClass 'hidden'
      loadData(url, container)

) this, this.jQuery, this.templates

