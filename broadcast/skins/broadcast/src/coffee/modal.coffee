((window, $) ->

  win = $ window
  body = $ window.document.body

  body.on 'click', '.modal-close', (e) ->
    el = $ @
    (el.parents '.modal').remove()

  $.modal = (name, url) ->
    modal = $ $.template 'modal', { name: name, url: url }
    body.append modal
    modalBody = modal.find '.modal-body'
    modalBody.rocaLoad()

    # when content is loaded into modal, adjust it's position and fire
    # the modal load complete event
    win.on "modal-#{name}-roca-load", (e) ->
      modal.css {
        'margin-left': -(modal.width() / 2),
        'margin-top': -(modal.height() / 2)
      }
      win.trigger "modal-#{name}-loaded"

    # after successful modal submission, remove modal
    win.on "modal-#{name}-submit", (e) ->
      cleanUp = () ->
        iframe = $ "#modal-#{name}-submit-frame"
        iframe.remove()
        modal.remove() 
        return
      modal.fadeOut()
      setTimeout cleanUp, 3000

) this, this.jQuery

