(function ($) {
    $.fn.input = function (cb) {
        var el = $(this);
        el.one('input', function() {
            el.off('change', cb);
            el.off('keyup', cb);
        });
        el.on('input', cb);
        el.on('change', cb);
        el.on('keyup', cb);
        return el;
    };
}(this.jQuery));
