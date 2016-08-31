((window, $) ->

  $.win = $ window
  $.body = $ 'body'
  $.htmlBody = $ 'html, body'

  $.afterNCalls = (count, fn) ->
    () ->
      count -= 1
      if count < 1
        fn.apply this, [].slice.call arguments, 0

  $.fn.scrollTo = (cb) ->
    el = $ @
    $.htmlBody.animate {scrollTop: el.offset().top}, 1000, cb
    el

) this, this.jQuery
