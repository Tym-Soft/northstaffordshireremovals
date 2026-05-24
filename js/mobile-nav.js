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
  // Two cases under file:// (no server to do directory resolution):
  //   1. href="/"          → site-root index.html, found by walking back up
  //                          based on the current file's depth in the project.
  //   2. href ending in /  → that-dir/index.html, e.g. services/ → services/index.html
  // Production hosts (Cloudflare Pages, Netlify, GitHub Pages, nginx, Apache)
  // handle both natively, so this shim is a no-op everywhere else.
  if (location.protocol === 'file:') {
    // Detect project root depth by looking for the deepest folder that
    // doesn't appear in our known project subfolders.
    var KNOWN_SUBFOLDERS = ['services', 'areas-covered', 'blog', 'resources', 'images', 'css', 'js', 'documents', 'tools'];
    function pathToSiteRoot() {
      var segs = location.pathname.split('/').filter(Boolean);
      // Drop the filename
      segs.pop();
      // Walk back from the end, counting how many segments match known
      // project subfolders.
      var up = 0;
      for (var i = segs.length - 1; i >= 0; i--) {
        if (KNOWN_SUBFOLDERS.indexOf(segs[i]) !== -1) up++;
        else break;
      }
      return up === 0 ? './' : new Array(up + 1).join('../');
    }

    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a');
      if (!a) return;
      var href = a.getAttribute('href');
      if (!href) return;
      if (/^(mailto:|tel:|javascript:|#)/i.test(href)) return;
      if (/^(?:https?:)?\/\//.test(href)) return;

      // Case 1: bare "/" → site-root index.html
      if (href === '/') {
        e.preventDefault();
        window.location.href = pathToSiteRoot() + 'index.html';
        return;
      }

      // Case 2: relative dir URL ending in "/" → that-dir/index.html
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
