((window, $) ->

  review = $ '#review'
  candidates = $ '#candidates'
  listCount = review.length + candidates.length

  getReloadCallback = (itemId) ->
    $.afterNCalls listCount, () ->
      item = $ "##{itemId}"
      item.scrollTo () ->
        item.addClass 'highlighted'
        setTimeout () ->
          item.removeClass 'highlighted'
          return
        , 4000
        return
      return

  ($ 'body').on 'click', '.vote-icon', (e) ->
    e.preventDefault()
    el = $ @
    form = el.parents '.vote-form'
    item = el.parents '.item'
    itemId = item.attr 'id'
    action = form.attr 'action'
    button_value = el.val()

    reloadCallback = getReloadCallback itemId

    res = $.post action, upvote: button_value
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
