#!/usr/bin/env python3
"""Rebuild blog/index.html — newest posts first, capped at 9."""
from __future__ import annotations
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BLOG_INDEX_MAX = 9


def post_meta(path: str) -> dict | None:
    html = open(path, encoding='utf-8').read()
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try: data = json.loads(m.group(1))
        except: continue
        items = data if isinstance(data, list) else [data]
        for it in items:
            if isinstance(it, dict) and it.get('@type') == 'BlogPosting':
                desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html, re.I)
                hero_m = re.search(r'<img[^>]+src="([^"]+)"[^>]+alt', html, re.I)
                return {
                    'slug': os.path.basename(path),
                    'date': it.get('datePublished'),
                    'headline': it.get('headline') or '',
                    'desc': desc_m.group(1) if desc_m else '',
                    'img': hero_m.group(1) if hero_m else 'images/family-celebrating-keys-new-home.jpg',
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
            <a class="blog-card-link" href="{p['slug']}">Read article →</a>
          </div>
        </article>''')

    grid = '\n'.join(cards)
    # Read blog/index.html and replace the .np-blog-grid block
    idx_path = 'blog/index.html'
    if not os.path.exists(idx_path):
        print('blog/index.html missing — create it first'); return 1
    html = open(idx_path).read()
    new = re.sub(r'(<div class="np-blog-grid">)(.*?)(</div>\s*</div>)',
                 lambda m: m.group(1) + '\n' + grid + '\n      ' + m.group(3),
                 html, count=1, flags=re.S)
    open(idx_path, 'w').write(new)
    print(f'blog/index.html updated with {len(posts)} posts')
    return 0

if __name__ == '__main__': sys.exit(main())
