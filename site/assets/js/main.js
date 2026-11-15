/* Hoa Tay Việt — behaviour: nav dropdown, off-canvas menu, back-to-top, search, gallery. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function each(list, fn) { Array.prototype.forEach.call(list, fn); }

  /* ---------------------------------------------------------------------
     4. Main-nav dropdowns — hover on pointer devices, tap on touch
     --------------------------------------------------------------------- */
  (function navDropdowns() {
    var hoverable = window.matchMedia('(hover: hover)').matches;

    each(document.querySelectorAll('.main-nav > li.has-dropdown'), function (li) {
      var link = li.querySelector('a');
      var closeTimer;

      function open()  { li.classList.add('is-open');    link.setAttribute('aria-expanded', 'true'); }
      function close() { li.classList.remove('is-open'); link.setAttribute('aria-expanded', 'false'); }

      if (hoverable) {
        li.addEventListener('mouseenter', function () { clearTimeout(closeTimer); open(); });
        li.addEventListener('mouseleave', function () { closeTimer = setTimeout(close, 120); });
        li.addEventListener('focusin', open);
        li.addEventListener('focusout', function (e) {
          if (!li.contains(e.relatedTarget)) close();
        });
      } else {
        link.addEventListener('click', function (e) {
          e.preventDefault();
          if (li.classList.contains('is-open')) { close(); } else { open(); }
        });
      }
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    });
  })();

  /* ---------------------------------------------------------------------
     5. Off-canvas mobile menu
     --------------------------------------------------------------------- */
  (function offcanvas() {
    var panel    = document.getElementById('mobile-menu');
    var backdrop = document.querySelector('.offcanvas-backdrop');
    if (!panel || !backdrop) return;

    var lastFocus = null;

    function open(trigger) {
      lastFocus = trigger || document.activeElement;
      panel.classList.add('is-open');
      backdrop.classList.add('is-open');
      document.body.classList.add('no-scroll');
      panel.setAttribute('aria-hidden', 'false');
      var first = panel.querySelector('button, a, input');
      if (first) first.focus();
    }
    function close() {
      panel.classList.remove('is-open');
      backdrop.classList.remove('is-open');
      document.body.classList.remove('no-scroll');
      panel.setAttribute('aria-hidden', 'true');
      if (lastFocus) lastFocus.focus();
    }

    each(document.querySelectorAll('[data-open-menu]'), function (b) {
      b.addEventListener('click', function (e) { e.preventDefault(); open(b); });
    });
    each(document.querySelectorAll('[data-close-menu]'), function (b) {
      b.addEventListener('click', function (e) { e.preventDefault(); close(); });
    });
    backdrop.addEventListener('click', close);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel.classList.contains('is-open')) close();
    });

    each(panel.querySelectorAll('.toggle-sub'), function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var li = btn.parentNode.parentNode;
        li.classList.toggle('is-open');
        btn.setAttribute('aria-expanded', li.classList.contains('is-open') ? 'true' : 'false');
      });
    });
  })();

  /* ---------------------------------------------------------------------
     6. Back to top
     --------------------------------------------------------------------- */
  (function backToTop() {
    var btn = document.querySelector('.back-to-top');
    if (!btn) return;
    var ticking = false;

    function update() {
      btn.classList.toggle('is-active', window.pageYOffset > 300);
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(update);
    }, { passive: true });

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
    update();
  })();

  /* ---------------------------------------------------------------------
     7. Search — the original posts to WordPress; here it goes to the
        static search page, which filters the bundled product JSON.
     --------------------------------------------------------------------- */
  each(document.querySelectorAll('.searchform'), function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var qField = form.querySelector('.search-field');
      var cField = form.querySelector('.search-cats');
      var q   = qField ? qField.value.trim() : '';
      var cat = cField ? cField.value : '';
      var base = form.getAttribute('data-base') || '';
      var url = base + 'tim-kiem.html?s=' + encodeURIComponent(q);
      if (cat) url += '&cat=' + encodeURIComponent(cat);
      window.location.href = url;
    });
  });

  /* ---------------------------------------------------------------------
     8. Product-detail gallery
     --------------------------------------------------------------------- */
  (function productGallery() {
    var main   = document.querySelector('.gallery-main img');
    var thumbs = document.querySelectorAll('.gallery-thumbs button');
    if (!main || !thumbs.length) return;

    each(thumbs, function (btn) {
      btn.addEventListener('click', function () {
        each(thumbs, function (b) { b.setAttribute('aria-selected', 'false'); });
        btn.setAttribute('aria-selected', 'true');
        main.src = btn.getAttribute('data-full');
        main.alt = btn.getAttribute('data-alt') || '';
      });
    });
  })();
})();
