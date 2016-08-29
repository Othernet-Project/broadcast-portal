// Generated by CoffeeScript 1.10.0
(function(window, $) {
  var win;
  win = $(window);
  $.fn.loading = function() {
    var el;
    el = $(this);
    return el.each(function() {
      el = $(this);
      el.data('loading-orig-html', el.html());
      return el.html($.template('loading'));
    });
  };
  $.fn.cancelLoading = function() {
    var el;
    el = $(this);
    return el.each(function() {
      var origHtml;
      origHtml = el.data('loading-orig-html');
      if (!origHtml) {
        return;
      }
      return el.html(origHtml);
    });
  };
  $.fn.funnelSubmit = function() {
    var el;
    el = $(this);
    return el.on('submit', 'form', function(e) {
      var action, form, formData, res;
      e.preventDefault();
      form = $(this);
      formData = form.serialize();
      action = (form.attr('action')) || window.location.pathname;
      res = $.post(action, formData);
      res.done(function(resp) {
        return el.html(resp);
      });
      return res.fail(function(xhr) {
        return el.html(xhr.responseText);
      });
    });
  };
  $.fn.rocaLoad = function() {
    var el;
    el = $(this);
    return el.each(function() {
      var target, url;
      el = $(this);
      url = el.attr('href');
      target = $("#" + (el.data('roca-target')));
      if (!target.length) {
        return;
      }
      target.loading().load(url, function(res, status, xhr) {
        switch (xhr.status) {
          case 200:
            win.trigger('roca-load', [el, target]);
            break;
          default:
            ($(target)).cancelLoading();
            win.trigger('roca-error', [el, target]);
        }
      });
      if ((el.data('roca-trap-submit')) === 'yes') {
        return target.funnelSubmit();
      }
    });
  };
  return ($('a[data-roca-target]')).rocaLoad();
})(this, this.jQuery);
