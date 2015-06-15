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
    function previewPath() {
        var prefix = $('.content-path .path-prefix').val(),
            previewSource = $('#id_path'),
            previewTarget = $('.content-path .preview');

        function update() {
            previewTarget.text(prefix + previewSource.val());
        }
        previewSource.keyup(update);
        update();
    }

    previewPath();
}(this, this.jQuery));
