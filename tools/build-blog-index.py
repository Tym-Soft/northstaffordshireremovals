#!/usr/bin/env python3
"""Rebuild blog/index.html — newest posts first, ALL posts shown."""
from __future__ import annotations
import glob, importlib.util, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
# Show every blog post on the hub (previously capped at 9). The hub
# is the canonical browse-all-posts page; pagination can come later
# if the list grows much beyond 50 posts.
BLOG_INDEX_MAX = 9999

# Load BLOG_META + CTA shortcuts from render-pages.py so we can use
# the per-blog CTA text ("See 2026 pricing", "Read the piano guide",
# etc.) instead of spamming "Read article" on every card.
_rp_path = os.path.join(ROOT, 'tools', 'render-pages.py')
_spec = importlib.util.spec_from_file_location('_rp', _rp_path)
_rp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_rp)
_BLOG_META_BY_HREF = {m['href']: m for m in _rp.BLOG_META.values()}


def cta_for(slug: str) -> str:
    """Return the per-blog CTA text from BLOG_META, falling back to
    a generic 'Read article' if the slug isn't in the metadata."""
    href = f'blog/{slug}'
    meta = _BLOG_META_BY_HREF.get(href)
    return (meta.get('cta') if meta else None) or 'Read article'


def post_meta(path: str) -> dict | None:
    """Extract blog post metadata for the index card.
    Image comes from the BlogPosting schema's `image` field (reliable
    — always the hero image, always the correct filename) rather than
    scraping the first <img> in the HTML (which catches the nav logo)."""
    html = open(path, encoding='utf-8').read()
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try: data = json.loads(m.group(1))
        except: continue
        items = data if isinstance(data, list) else [data]
        for it in items:
            if isinstance(it, dict) and it.get('@type') == 'BlogPosting':
                desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html, re.I)
                # Schema image is typically a full URL — strip everything
                # before /images/ so we end up with just images/filename.jpg
                img_url = it.get('image') or ''
                if isinstance(img_url, list): img_url = img_url[0] if img_url else ''
                if isinstance(img_url, dict): img_url = img_url.get('url', '')
                img_m = re.search(r'images/[^/]+\.(?:jpg|jpeg|png|webp)$', img_url, re.I)
                img = img_m.group(0) if img_m else 'images/family-celebrating-keys-new-home.jpg'
                return {
                    'slug': os.path.basename(path),
                    'date': it.get('datePublished'),
                    'headline': it.get('headline') or '',
                    'desc': desc_m.group(1) if desc_m else '',
                    'img': img,
                }
    return None


def main() -> int:
    posts = []
    for p in sorted(glob.glob('blog/*.html')):
        if os.path.basename(p) == 'index.html': continue
        m = post_meta(p)
        if m: posts.append(m)
    posts.sort(key=lambda x: (x['date'] or '', x['slug']), reverse=True)
    posts = posts[:BLOG_INDEX_MAX]

    cards = []
    for p in posts:
        cards.append(f'''        <article class="blog-card">
          <a href="{p['slug']}" class="blog-card-img"><img src="../{p['img']}" alt="{p['headline']}" width="800" height="500" loading="lazy"></a>
          <div class="blog-card-body">
            <time datetime="{p['date']}">{p['date']}</time>
            <h3><a href="{p['slug']}">{p['headline']}</a></h3>
            <p>{p['desc']}</p>
            <a class="blog-card-link" href="{p['slug']}">{cta_for(p['slug'])}</a>
          </div>
        </article>''')

    grid = '\n'.join(cards)
    # Read blog/index.html and replace the .np-blog-grid block
    idx_path = 'blog/index.html'
    if not os.path.exists(idx_path):
        print('blog/index.html missing — create it first'); return 1
    html = open(idx_path).read()
    # Tolerate any attributes on the wrapper (style, data-*, etc.)
    # so the regex matches whether the template has inline styles or not.
    # Also strip the embedded <style> block that older templates put
    # inside the wrapper — modern .np-blog-grid CSS lives in site.css.
    new = re.sub(r'(<div class="np-blog-grid"[^>]*>)(.*?)(</div>\s*</div>)',
                 lambda m: '<div class="np-blog-grid">\n' + grid + '\n      ' + m.group(3),
                 html, count=1, flags=re.S)
    open(idx_path, 'w').write(new)
    print(f'blog/index.html updated with {len(posts)} posts')
    return 0

if __name__ == '__main__': sys.exit(main())
