(function () {
  var MOBILE = '(max-width: 980px)';

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

  // ── Mobile-only: whole dropdown row toggles its sub-menu ───────
  // On mobile the entire .has-dropdown > a row acts as the toggle:
  // first tap expands, second tap navigates to the hub page (or use
  // the "All X →" link at the top of the expanded list). On desktop
  // hover handles the menu and the link navigates as normal.
  var ddLinks = document.querySelectorAll('.has-dropdown > a');
  for (var i = 0; i < ddLinks.length; i++) {
    ddLinks[i].addEventListener('click', function (e) {
      if (!window.matchMedia(MOBILE).matches) return;
      var li = this.closest('.has-dropdown');
      if (!li) return;
      if (!li.classList.contains('is-expanded')) {
        e.preventDefault();
        li.classList.add('is-expanded');
        this.setAttribute('aria-expanded', 'true');
      }
      // second tap: allow default navigation to the hub page
    });
  }

  // Reset expanded state when crossing back to desktop
  if (window.matchMedia) {
    var mq = window.matchMedia(MOBILE);
    var resetExpanded = function () {
      if (!mq.matches) {
        var open = document.querySelectorAll('.has-dropdown.is-expanded');
        for (var j = 0; j < open.length; j++) {
          open[j].classList.remove('is-expanded');
        }
      }
    };
    if (mq.addEventListener) mq.addEventListener('change', resetExpanded);
    else if (mq.addListener) mq.addListener(resetExpanded);
  }

  // ── file:// browsing fallback ──────────────────────────
  // Two cases under file:// (no server to do directory resolution):
  //   1. href="/"          → site-root index.html, found by walking back up
  //                          based on the current file's depth in the project.
  //   2. href ending in /  → that-dir/index.html, e.g. services/ → services/index.html
  // Production hosts (Cloudflare Pages, Netlify, GitHub Pages, nginx, Apache)
  // handle both natively, so this shim is a no-op everywhere else.
  if (location.protocol === 'file:') {
    var KNOWN_SUBFOLDERS = ['services', 'areas-covered', 'blog', 'resources', 'images', 'css', 'js', 'documents', 'tools'];
    function pathToSiteRoot() {
      var segs = location.pathname.split('/').filter(Boolean);
      segs.pop();
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

      if (href === '/') {
        e.preventDefault();
        window.location.href = pathToSiteRoot() + 'index.html';
        return;
      }

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
