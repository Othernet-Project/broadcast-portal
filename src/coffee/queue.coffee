((window, $, templates) ->
  'use strict'

  queues = $ '.queue'
  handles = $ '.handles a.handle'
  searchForm = $ 'form.search'
  searchUrl = searchForm.attr 'action'
  searchQTElem = $ '.search input#type'
  actionFormSelector = '.action form'
  plusSign = /\+/g
  queryRegEx = /([^&=]+)=?([^&]*)/g

  decode = (src) ->
    return decodeURIComponent(src.replace(plusSign, " "))

  getQueryParams = () ->
    params = {}
    query = window.location.search.substring(1)
    while (match = queryRegEx.exec(query))
       params[decode(match[1])] = decode(match[2])
    return params

  getFormData = (form) ->
    data = {}
    arr = form.serializeArray()
    $(arr).each (index, obj) ->
      data[obj.name] = obj.value;
    return data;

  modifyQueue = (e) ->
    e.preventDefault()
    form = $ @
    btn = form.find 'button'
    formData = getFormData form
    formData[btn.attr 'name'] = btn.val()
    actionUrl = form.attr 'action'
    res = $.ajax actionUrl,
      method: 'POST'
      data: formData
    res.done (data) ->
      row = form.parents 'tr'
      row.remove()
    res.fail () ->
      alert(templates.queueModifyError)

  loadQueue = (url, container) ->
    res = $.get url
    res.done (data) ->
      container.html(data)
      actionForms = $ actionFormSelector
      actionForms.off 'submit', modifyQueue
      actionForms.on 'submit', modifyQueue
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
      handles.removeClass 'active'
      elem.addClass 'active'
      queues.addClass 'hidden'
      container.removeClass 'hidden'
      res = loadQueue url, container
      res.done (data) ->
        window.history.pushState null, null, url

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

  # apply action handlers to initially visible forms
  actionForms = $ actionFormSelector
  actionForms.on 'submit', modifyQueue

  $(window).on 'popstate', (e) ->
    params = getQueryParams()
    container = queues.filter('.' + params.type)
    activeHandle = $('.handle.' + params.type)
    handles.removeClass 'active'
    activeHandle.addClass 'active'
    queues.addClass 'hidden'
    container.removeClass 'hidden'
    loadQueue window.location, container

) this, this.jQuery, this.templates

