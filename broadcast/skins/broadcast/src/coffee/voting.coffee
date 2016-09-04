((window, $) ->

  win = $ window
  body = $ 'body'
  review = $ '#review'
  candidates = $ '#candidates'
  listCount = review.length + candidates.length
  lastVotedItem = null

  onRocaLoad = (e, parent) ->
    return if lastVotedItem is null
    item = parent.find "##{lastVotedItem}"
    return if not item.length
    lastVotedItem = null
    item.scrollTo () ->
      item.addClass 'highlighted'
      setTimeout () ->
        item.removeClass 'highlighted'
        return
      , 4000
      return
    return

  onVote = (e) ->
    e.preventDefault()
    el = $ @
    form = el.parents '.vote-form'
    item = el.parents '.item'
    itemId = item.attr 'id'
    action = form.attr 'action'
    button_value = el.val()

    res = $.post action, upvote: button_value
    res.done () ->
      lastVotedItem = itemId
      win.trigger 'vote-submit'
      $.popup $.template 'vote-success'
      $.forceStateUpdate()
      return
    res.fail () ->
      $.popup $.template 'vote-fail'
      return
    return

  win.on 'review-roca-load', onRocaLoad
  win.on 'candidates-roca-load', onRocaLoad
  body.on 'click', '.vote-icon', onVote

) this, this.jQuery
