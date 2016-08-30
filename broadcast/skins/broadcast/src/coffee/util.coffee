((window, $) ->

  $.afterNCalls = (count, fn) ->
    () ->
      count -= 1
      if count < 1
        fn.apply this, [].slice.call arguments, 0

) this, this.jQuery
