(function (window, $) {
  var body = $('body');
  var hamburger = $('.hamburger');

  hamburger.on('click', toggleMenu);

  function toggleMenu(e) {
    e.preventDefault();
    body.toggleClass('menu-open');
  }
}(this, this.jQuery));
