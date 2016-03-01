((window, $, templates) ->
  'use strict'

  queues = $ '.queue'
  handles = $ '.handles a.handle'
  searchForm = $ '.search form'
  searchUrl = searchForm.attr 'action'
  searchQTElem = $ '.search input#type'
  actionFormSelector = '.action form'

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
      res = $.get url
      res.done (data) ->
        container.html(data)
        actionForms = $ actionFormSelector
        actionForms.off 'submit', modifyQueue
        actionForms.on 'submit', modifyQueue
      res.fail () ->
        container.html(templates.queueLoadError)

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

