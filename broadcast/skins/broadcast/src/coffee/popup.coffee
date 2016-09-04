((window, $) ->

  body = $ 'body'

  POPUP_TIMEOUT = 7000  # seconds

  body.on 'click', '.popup-close', (e) ->
    el = $ @
    (el.parents '.popup').remove()

  $.popup = (message, timeout) ->
    timeout ?= POPUP_TIMEOUT
    ($ '.popup').remove()
    popup = $ $.template 'popup', message: message
    body.append popup
    setTimeout () ->
      popup.remove()
    , timeout
    popup


) this, this.jQuery
