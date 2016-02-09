/**
 * forms.js: forms utility functions
 *
 * Copyright 2015, Outernet Inc.
 * Some rights reserved.
 * 
 * This software is free software licensed under the terms of GPLv3. See
 * COPYING file that comes with the source code, or
 * http://www.gnu.org/licenses/gpl.txt.
 */

(function (window, $) {

  $.fn.clearErrors = function () {
    var el = $(this);
    el.removeClass('field-error');
    el.find('.field-error-message').remove();
    return el;
  };

  $.fn.markError = function (message) {
    var el = $(this).clearErrors();
    var error = $('<span>');
    error.html(message);
    error.addClass('field-error-message');
    el.append(error);
    el.addClass('field-error');
  }

}(this, this.jQuery));
