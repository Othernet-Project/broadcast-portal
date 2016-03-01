((window, $, templates) ->
  'use strict'

  queues = $ '.queue'
  handles = $ '.handles a.handle'
  searchForm = $ '.search form'
  searchUrl = searchForm.attr 'action'
  searchQTElem = $ '.search input#type'

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

  getFormData = (form) ->
    data = {}
    arr = form.serializeArray()
    $(arr).each (index, obj) ->
      data[obj.name] = obj.value;
    return data;

  searchForm.on 'submit', (e) ->
    e.preventDefault()
    container = queues.not '.hidden'
    formData = getFormData searchForm
    formData.type = container.data 'source'
    res = $.ajax searchUrl,
      method: 'GET'
      data: formData
    res.done (data) ->
      container.html(data)
    res.fail () ->
      container.html(templates.queueLoadError)

) this, this.jQuery, this.templates

