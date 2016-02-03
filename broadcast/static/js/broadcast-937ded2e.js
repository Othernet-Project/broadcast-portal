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

    $('input[type="file"]').each(function () {
        var input = $(this),
            fileProxy = $('<a class="button small">Choose File</a>'),
            fileValue = $('<span>No file chosen</span>'),
            fileWrapper = $('<span class="file-wrapper"></span>');

        fileProxy.on('click', function () {
            input.click();
        });
        input.addClass('hidden');
        input.on('change', function () {
            fileValue.text($(this).val().split(/(\\|\/)/g).pop());
        });

        fileWrapper.append(fileProxy).append(fileValue);
        input.after(fileWrapper);
    });

    $('button').on('click', function () {
        var form = $(this).parents('form');
        // disabling the buttin in click handler will neutralize click event
        setTimeout(function () {
            form.find('button').attr('disabled', 'disabled');
        }, 0);
        $('.progress-feedback').css('visibility', 'visible');
    });
}(this, this.jQuery));
