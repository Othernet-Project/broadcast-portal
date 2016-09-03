((window, $) ->

  RELOAD_INTERVAL = 10000  # 10s

  win = $ window
  body = $ 'body'
  lastUpdate = parseInt (body.data 'last-update'), 10
  updateURL = body.data 'update-url'
  timer = null

  reloadState = (forced) ->
    $.getJSON updateURL, (data) ->
      data.forced = forced
      stateReloaded(data)

  stateReloaded = (data) ->
    return if lastUpdate is data.timestamp
    win.trigger 'state-update', [data]
    lastUpdate = data.timestamp
    return

  scheduleReload = () ->
    timer = setInterval reloadState, RELOAD_INTERVAL

  $.forceStateUpdate = () ->
    clearTimeout timer
    reloadState(yes)
    scheduleReload()

  scheduleReload()


) this, this.jQuery
