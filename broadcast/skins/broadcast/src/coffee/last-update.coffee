((window, $) ->

  RELOAD_INTERVAL = 5000

  win = $ window
  body = $ 'body'
  lastUpdate = parseInt (body.data 'last-update'), 10
  updateURL = body.data 'update-url'

  stateReloaded = (data) ->
    return if lastUpdate is data.timestamp
    win.trigger 'state-update', [data]
    lastUpdate = data.timestamp
    return

  reloadState = () ->
    res = $.getJSON updateURL, stateReloaded

  setInterval reloadState, RELOAD_INTERVAL

) this, this.jQuery
