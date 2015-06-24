/**
 * broadcast.js: broadcast form ui code
 *
 * Copyright 2015, Outernet Inc.
 * Some rights reserved.
 *
 * This software is free software licensed under the terms of GPLv3. See
 * COPYING file that comes with the source code, or
 * http://www.gnu.org/licenses/gpl.txt.
 */

(function (window, $) {
    'use strict';

    var title = $('#id_title');
    var url = $('#id_url');
    var preview = $('.content-url .preview');
    var prefix = preview.data('prefix');

    title.on('input', function () {
      title.off('keyup');
      url.val(slugify(title.val())).trigger('change');
    });

    url.on('change', previewPath);
    url.on('input', previewPath);

    function slugify(s) {
      s = s.toLowerCase().
        replace(/[\s\\/.,+*"'()\[\]{}:;?!~`@#%$^&_=]/g, '-').
        replace(/-+/g, '-');
      return encodeURIComponent($.trim(s));
    }

    function previewPath() {
      console.log(prefix + url.val());
      var absUrl = prefix + url.val();
      preview.text(absUrl);
    }

    previewPath();
}(this, this.jQuery));
