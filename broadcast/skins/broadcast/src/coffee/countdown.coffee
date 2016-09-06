((window, $) ->
  HOUR = 60 * 60
  MINUTE = 60

  formatTimeDiff = (td) ->
    hours = Math.floor td / HOUR
    td = td - hours * HOUR
    minutes = Math.floor td / MINUTE
    td = td - minutes * MINUTE
    seconds = td
    "#{hours}:#{$.zeroPad minutes}:#{$.zeroPad seconds}"

  getTd = () ->
    Math.round (new Date()).getTime() / 1000

  $.fn.toCountdown = () ->
    el = $ @
    targetTime = el.data 'timestamp'
    now = getTd()
    formattedDiff = formatTimeDiff targetTime - now
    el.text $.template 'countdown', time: formattedDiff

  setInterval () ->
    ($ '#filecast-time').toCountdown()
  , 1000

) this, this.jQuery
