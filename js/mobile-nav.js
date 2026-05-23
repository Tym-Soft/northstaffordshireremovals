(function () {
  var toggle = document.querySelector('.menu-toggle');
  var menu = document.getElementById('primary-nav');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function (e) {
      if (!menu.classList.contains('is-open')) return;
      if (menu.contains(e.target) || toggle.contains(e.target)) return;
      menu.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  }

  // ── file:// browsing fallback ──────────────────────────
  // Directory URLs like services/ don't resolve to services/index.html under
  // file:// (no server). On file:// only, intercept any click on a link whose
  // href ends in / and navigate to <href>index.html instead. Production hosts
  // (Cloudflare Pages, Netlify, GitHub Pages, nginx, Apache) handle this
  // natively, so the shim is a no-op everywhere else.
  if (location.protocol === 'file:') {
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a');
      if (!a) return;
      var href = a.getAttribute('href');
      if (!href) return;
      if (/^(mailto:|tel:|javascript:|#)/i.test(href)) return;
      if (/^(?:https?:)?\/\//.test(href)) return;
      // Strip query/hash for the test
      var clean = href.split('#')[0].split('?')[0];
      if (clean && clean.charAt(clean.length - 1) === '/') {
        e.preventDefault();
        var suffix = href.indexOf('#') >= 0
          ? href.substring(href.indexOf('#'))
          : (href.indexOf('?') >= 0 ? href.substring(href.indexOf('?')) : '');
        window.location.href = clean + 'index.html' + suffix;
      }
    });
  }
})();
