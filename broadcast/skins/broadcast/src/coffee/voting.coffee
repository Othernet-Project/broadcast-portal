((window, $) ->

  win = $ window
  htmlBody = $ 'html, body'
  review = $ '#review'
  candidates = $ '#candidates'
  listCount = review.length + candidates.length

  getReloadCallback = (itemId) ->
    $.afterNCalls listCount, () ->
      item = $ "##{itemId}"
      htmlBody.animate {scrollTop: item.offset().top}, 1000
      item.addClass 'highlighted'
      setTimeout () ->
        item.removeClass 'highlighted'
      , 4000
      return


  ($ 'body').on 'submit', '.vote-form', (e) ->
    e.preventDefault()
    el = $ @
    item = el.parents '.item'
    itemId = item.attr 'id'
    action = el.attr 'action'
    data = el.serialize()

    reloadCallback = getReloadCallback itemId

    res = $.post action, data
    res.done () ->
      $.popup $.template 'vote-success'
      review.reload(reloadCallback)
      candidates.reload(reloadCallback)
      return
    res.fail () ->
      $.popup $.template 'vote-fail'
      return
    return


) this, this.jQuery
