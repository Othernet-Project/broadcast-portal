// Generated by CoffeeScript 1.10.0
(function(window, $, Mustache) {
  $.templates = {};
  $.template = function(name, substs) {
    return Mustache.render($.templates[name], substs);
  };
  $.fn.template = function(name, substs) {
    var el;
    el = $(this);
    return el.html($.template(name, subst));
  };
  return ($('script[type="text/x-template"]')).each(function() {
    var html, id, src;
    src = $(this);
    html = $.trim(src.html());
    id = src.attr('id');
    Mustache.parse(html);
    $.templates[id] = html;
  });
})(this, this.jQuery, this.Mustache);