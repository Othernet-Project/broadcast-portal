// Generated by CoffeeScript 1.10.0
(function(window, $) {
  var body;
  body = $(window.document.body);
  return body.on('input', 'input, select, textarea', function(e) {
    var el;
    el = $(this);
    return (el.siblings('.field-error-message')).remove();
  });
})(this, this.jQuery);