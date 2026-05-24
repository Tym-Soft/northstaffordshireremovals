#!/usr/bin/env python3
"""
northstaffordshireremovals.co.uk content audit.
Adapted from markratcliffemoving.co.uk/tools/audit.py.

NSR-specific differences:
  - No BAR / British Association of Removers signal (NSR is not a member)
  - "Fully covered" preferred over "fully insured" — never use the latter
  - EEAT signals adapted to NSR brand identity
  - Org @id and domain swapped to NSR

Verifies the 41 build rules described in the MRM audit.
"""

from __future__ import annotations
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BLOG_MIN_WORDS     = 2000
LOCATION_MIN_WORDS = 1500
PAGE_MIN_WORDS     = 1600    # NSR sitewide rule (404 exempt)
BODY_LINKS_MIN     = 10
BLOG_INDEX_MAX     = 9
META_DESC_MAX      = 145
TITLE_PX_MAX       = 550
ALT_TEXT_MAX       = 100
IMAGE_MAX_BYTES    = 200 * 1024
BASE_URL           = 'https://www.northstaffordshireremovals.co.uk'
ORG_ID             = BASE_URL + '/#organization'

NON_DESCRIPTIVE_ANCHORS = {
    'click here','clickhere','read more','learn more','more','here',
    'this','click','continue reading','continue','link','this link',
    'more info','read','see more','view more','find out more','tap here',
}

CHAR_PX = {
    ' ':5,'!':5,'"':6,'#':11,'$':11,'%':17,'&':13,"'":4,'(':7,')':7,'*':8,
    '+':12,',':5,'-':7,'.':5,'/':6,'0':11,'1':11,'2':11,'3':11,'4':11,'5':11,
    '6':11,'7':11,'8':11,'9':11,':':6,';':6,'<':12,'=':12,'>':12,'?':11,'@':18,
    'A':12,'B':13,'C':14,'D':14,'E':13,'F':12,'G':15,'H':14,'I':6,'J':9,'K':13,
    'L':11,'M':16,'N':14,'O':15,'P':13,'Q':15,'R':14,'S':13,'T':12,'U':14,
    'V':12,'W':18,'X':12,'Y':12,'Z':12,'[':6,'\\':6,']':6,'^':9,'_':11,'`':6,
    'a':11,'b':12,'c':10,'d':12,'e':11,'f':7,'g':12,'h':12,'i':5,'j':5,'k':11,
    'l':5,'m':17,'n':12,'o':12,'p':12,'q':12,'r':7,'s':10,'t':7,'u':12,'v':10,
    'w':16,'x':11,'y':10,'z':10,'{':6,'|':5,'}':6,'~':12,
    '–':11,'—':14,'‘':4,'’':4,'“':8,'”':8,'·':5,'•':7,'…':13,
}
DEFAULT_PX = 11

NAV_END_RE   = re.compile(r'</header>', re.S)
FOOTER_RE    = re.compile(r'<footer', re.S)
WORD_HEAD_RE = re.compile(r'<head.*?</head>', re.S | re.I)
WORD_SCRIPT  = re.compile(r'<script.*?</script>', re.S | re.I)
WORD_STYLE   = re.compile(r'<style.*?</style>',  re.S | re.I)
TAG_RE       = re.compile(r'<[^>]+>')
ENT_RE       = re.compile(r'&[a-z]+;')


def title_pixel_width(text: str) -> int:
    decoded = (text.replace('&amp;','&').replace('&ndash;','–').replace('&mdash;','—')
                   .replace('&middot;','·').replace('&rsquo;','’').replace('&lsquo;','‘')
                   .replace('&rdquo;','”').replace('&ldquo;','“').replace('&quot;','"')
                   .replace('&apos;',"'"))
    return sum(CHAR_PX.get(c, DEFAULT_PX) for c in decoded)


def is_redirect_stub(html: str) -> bool:
    return 'http-equiv="refresh"' in html or 'window.location.replace' in html


def word_count(html: str) -> int:
    h = WORD_HEAD_RE.sub('', html)
    h = WORD_SCRIPT.sub('', h)
    h = WORD_STYLE.sub('', h)
    t = TAG_RE.sub(' ', h)
    t = ENT_RE.sub(' ', t)
    return len(t.split())


def body_internal_links(html: str) -> set[str]:
    m_start = NAV_END_RE.search(html)
    m_end   = FOOTER_RE.search(html)
    start   = m_start.end() if m_start else 0
    end     = m_end.start() if m_end else len(html)
    body    = html[start:end]
    refs    = re.findall(r'<a\b[^>]*?\bhref="([^"]+)"', body)
    seen = set()
    for href in refs:
        h = href.split('#')[0].split('?')[0].strip()
        if not h or h in ('/','./','../'): continue
        if h.startswith(('mailto:','tel:','javascript:','#')): continue
        if h.startswith(('http://','https://','//')):
            if 'northstaffordshireremovals.co.uk' not in h: continue
            m = re.search(r'northstaffordshireremovals\.co\.uk(/.+)', h)
            if m: h = m.group(1).lstrip('/')
        if h.startswith('../'): h = h[3:]
        elif h.startswith('./'): h = h[2:]
        if h.endswith('.html') or h.endswith('/'):
            seen.add(h)
    return seen


def all_pages() -> list[str]:
    paths = (
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('blog/*.html')
        + glob.glob('services/*.html')
        + glob.glob('resources/*.html')
    )
    def is_verification_stub(p: str) -> bool:
        name = os.path.basename(p)
        return (name.startswith('google') and len(name) > 16
                or name.startswith('BingSiteAuth')
                or name.startswith('yandex_'))
    return sorted(p for p in paths if os.path.isfile(p) and not is_verification_stub(p))


def is_blog_post(path: str) -> bool:
    return path.startswith('blog/') and os.path.basename(path) != 'index.html'


def is_location_page(path: str) -> bool:
    return path.startswith('areas-covered/') and os.path.basename(path) != 'index.html'


def indexable_pages(pages: list[str]) -> list[str]:
    out = []
    for p in pages:
        try:
            html = open(p, encoding='utf-8').read(4096)
        except OSError:
            continue
        if is_redirect_stub(html): continue
        m = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', html, re.I)
        if m and 'noindex' in m.group(1).lower():
            continue
        out.append(p)
    return out


def expected_loc(path: str) -> str:
    if path == 'index.html':
        return BASE_URL + '/'
    if path.endswith('/index.html'):
        return BASE_URL + '/' + path[:-len('index.html')]
    return BASE_URL + '/' + path


def sitemap_locs() -> set[str]:
    try:
        xml = open('sitemap.xml', encoding='utf-8').read()
    except OSError:
        return set()
    return set(re.findall(r'<loc>([^<]+)</loc>', xml))


# ── SEO keyword placement (per [[seo-keyword-placement-rule]]) ───
# Derives the primary keyword phrase from each page's slug
# (slugs ARE keyword-engineered on this site, so the slug is the
# authoritative source) and checks placement in title / meta desc /
# image alt / body density. Skips legal/utility/404 pages.

SEO_SKIP_PAGES = {
    '404.html', 'privacy-policy.html', 'terms.html', 'careers.html',
    'blog/index.html', 'sitemap.xml',
}
SEO_STOP_WORDS = {
    # Standard English stops
    'a', 'an', 'the', 'of', 'in', 'on', 'at', 'for', 'with', 'to',
    'and', 'or', 'is', 'are', 'how', 'what', 'why', 'when', 'where',
    'who', 'which', 'this', 'that', 'these', 'those', 'be', 'been',
    'has', 'have', 'had', 'do', 'does', 'did', 'vs', 'versus', 'about',
    'before', 'after', 'from',
    # Site-wide boilerplate
    'guide', 'staffordshire', 'uk',
}
SEO_BODY_DENSITY_MIN = 0.15     # hard floor — under = clearly under-targeted
SEO_BODY_DENSITY_MAX = 4.0      # hard ceiling — over = stuffing risk
SEO_BODY_DENSITY_IDEAL = (0.5, 1.5)  # informational sweet spot (memory rule)
SEO_BODY_MIN_WORDS = 400        # too-short pages skip the body check


def seo_primary_keyword(path: str) -> str | None:
    """Derive the primary keyword phrase from a page slug.
    Returns lowercased phrase, or None to skip this page."""
    if path in SEO_SKIP_PAGES:
        return None
    if path == 'index.html':
        return 'staffordshire removals'  # brand keyword for home page

    base = os.path.basename(path).replace('.html', '')
    # Hub pages (services/index.html, areas-covered/index.html) —
    # derive from the parent directory name, not the basename 'index'
    if base == 'index':
        parent = os.path.basename(os.path.dirname(path))
        if not parent:
            return None
        parent_words = [w for w in parent.replace('-', ' ').split()
                        if w.lower() not in SEO_STOP_WORDS]
        return ' '.join(parent_words[:2]).lower() if parent_words else None

    # Strip year-suffixes (2024, 2025, 2026, etc.) and stop words
    all_words = [w for w in base.replace('-', ' ').split()
                 if not (len(w) == 4 and w.isdigit())]
    words = [w for w in all_words if w.lower() not in SEO_STOP_WORDS]
    # If stop-stripping leaves us with less than 2 meaningful words
    # (e.g. about-us → just 'us'), fall back to the un-stripped slug
    # so the keyword stays semantically useful.
    if len(words) < 2:
        words = all_words
    if not words:
        return None
    # First 2 words = the primary keyword for the page
    return ' '.join(words[:2]).lower()


def blog_post_meta(path: str) -> dict | None:
    html = open(path, encoding='utf-8').read()
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if isinstance(item, dict) and item.get('@type') == 'BlogPosting':
                return {
                    'slug': os.path.basename(path),
                    'date': item.get('datePublished'),
                    'headline': item.get('headline'),
                }
    return None


def audit():
    pages = all_pages()
    failures = {k: [] for k in (
        'blog_word_count','location_word_count','internal_links','blog_index_listing',
        'blog_index_order','sitemap','duplicate_titles','meta_description','title_pixel_width',
        'image_alt','canonical','duplicate_h1','links_to_non_canonical','canonical_target',
        'canonical_in_head','img_dimensions','non_descriptive_anchor','empty_anchor',
        'h1_not_first','alt_too_long','security_meta','image_size','headers_file',
        'redirects_file','url_parameters','duplicate_descriptions','h1_count','mixed_content',
        'robots_txt','eeat','org_jsonld','json_valid','faq_schema','one_meta_desc',
        'js_canonical','dir_trailing_slash','file_exists','html_trailing_slash',
        'microdata','fully_insured_violation','page_min_words','min_faqs',
        'seo_keyword_placement'
    )}
    # Soft-warning category — informational, doesn't fail the audit
    # (image alt-text including the keyword is a recommendation, not
    # a structural requirement like title/meta-desc/body density).
    seo_alt_recommendations = []

    blog_posts = []

    for path in pages:
        try:
            html = open(path, encoding='utf-8').read()
        except OSError:
            continue
        if is_redirect_stub(html):
            continue

        wc = word_count(html)
        link_count = len(body_internal_links(html))

        if is_blog_post(path):
            blog_posts.append(path)
            if wc < BLOG_MIN_WORDS:
                failures['blog_word_count'].append((wc, path))

        if is_location_page(path):
            if wc < LOCATION_MIN_WORDS:
                failures['location_word_count'].append((wc, path))

        if link_count < BODY_LINKS_MIN:
            failures['internal_links'].append((link_count, path))

        # NSR-specific: never use "fully insured"
        if re.search(r'\bfully[\s-]?insured\b', html, re.I):
            failures['fully_insured_violation'].append(path)

        # NSR-specific: every page ≥1600 words (404 exempt)
        if os.path.basename(path) != '404.html' and wc < PAGE_MIN_WORDS:
            failures['page_min_words'].append((wc, path))

        # NSR-specific: every page must carry ≥4 on-topic FAQs (404 exempt)
        if os.path.basename(path) != '404.html':
            faq_count = len(re.findall(r'<details\b', html))
            if faq_count < 4:
                failures['min_faqs'].append((faq_count, path))

    # Rule 4 — blog index
    index_path = 'blog/index.html'
    if os.path.isfile(index_path):
        index_html = open(index_path, encoding='utf-8').read()
        listed = []
        m = re.search(r'<div class="np-blog-grid">(.*?)</div>\s*</div>', index_html, re.S)
        if not m:
            # fallback to any blog grid pattern
            m = re.search(r'<div class="blog-grid">(.*?)</div>\s*</div>', index_html, re.S)
        if m:
            grid = m.group(1)
            for href_m in re.finditer(r'<h3><a href="([^"]+)">', grid):
                listed.append(href_m.group(1).split('#')[0].split('?')[0])
        if len(listed) > BLOG_INDEX_MAX:
            failures['blog_index_listing'].append(f'visible count is {len(listed)} (>{BLOG_INDEX_MAX})')
        post_metas = [m for m in (blog_post_meta(p) for p in blog_posts) if m]
        post_metas.sort(key=lambda x: (x.get('date') or '', x.get('slug') or ''), reverse=True)
        expected = [m['slug'] for m in post_metas[:BLOG_INDEX_MAX]]
        if listed and listed != expected:
            failures['blog_index_order'].append(f'expected={expected}, got={listed}')

    # Sitemap
    indexable = indexable_pages(pages)
    sitemap = sitemap_locs()
    for p in indexable:
        if expected_loc(p) not in sitemap:
            failures['sitemap'].append(('missing', p))
    indexable_set = {expected_loc(p) for p in indexable}
    for loc in sitemap:
        if loc not in indexable_set:
            failures['sitemap'].append(('orphan', loc))

    # Per-page deep checks
    title_re = re.compile(r'<title>([^<]+)</title>', re.I)
    desc_re  = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.I)
    titles_seen, descs_seen, h1s_seen = {}, {}, {}

    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        head_end = html.find('</head>')
        head = html[:head_end] if head_end > 0 else html

        # Rule 6 — title
        tm = title_re.search(html)
        if not tm:
            failures['duplicate_titles'].append(('no-title', p)); continue
        title = ' '.join(tm.group(1).split()).strip()
        titles_seen.setdefault(title, []).append(p)

        # Rule 7 — meta desc length
        descs = desc_re.findall(html)
        if not descs:
            failures['meta_description'].append(('no-desc', p))
        else:
            dl = len(descs[0])
            if dl > META_DESC_MAX: failures['meta_description'].append((dl, p))
            descs_seen.setdefault(descs[0], []).append(p)
        if len(descs) != 1:
            failures['one_meta_desc'].append((len(descs), p))

        # Rule 8 — title pixel width
        px = title_pixel_width(title)
        if px > TITLE_PX_MAX: failures['title_pixel_width'].append((px, p))

        # Rule 9 — img alt
        for img in re.findall(r'<img\b[^>]*>', html):
            if 'alt=' not in img:
                failures['image_alt'].append(('no-alt', p)); break

        # Rule 10, 14 — canonical
        can = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', head, re.I)
        if not can:
            failures['canonical'].append(('no-canonical', p))
        else:
            if not can.group(1).startswith(BASE_URL):
                failures['canonical'].append(('wrong-domain', p))

        # Rule 15 — img dimensions
        for img in re.findall(r'<img\b[^>]*>', html):
            if 'width=' not in img or 'height=' not in img:
                failures['img_dimensions'].append(('no-dims', p)); break

        # Rule 19 — alt length
        for am in re.finditer(r'<img\b[^>]*\balt="([^"]*)"', html):
            if len(am.group(1)) > ALT_TEXT_MAX:
                failures['alt_too_long'].append((len(am.group(1)), p)); break

        # Rule 20 — security meta
        if 'Content-Security-Policy' not in head:
            failures['security_meta'].append(('no-csp', p))
        if not re.search(r'<meta\s+name="referrer"', head, re.I):
            failures['security_meta'].append(('no-referrer', p))

        # Rule 26 — exactly one H1
        h1s = re.findall(r'<h1\b[^>]*>(.*?)</h1>', html, re.S)
        if len(h1s) != 1:
            failures['h1_count'].append((len(h1s), p))
        elif h1s:
            text = re.sub(r'<[^>]+>', '', h1s[0]).strip()
            h1s_seen.setdefault(text, []).append(p)

        # Rule 27 — no mixed content
        # Filter out SVG xmlns (legitimate, not a network resource) and HTML DTD URL.
        for u in re.findall(r'\bhttp://[^\s"\'<>]+', html):
            if u.startswith('http://www.w3.org/'): continue
            if u.startswith('http://schema.org'): continue
            failures['mixed_content'].append((u, p)); break

        # Rule 30 — org JSON-LD with @id
        org_ok = False
        for s in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            try: data = json.loads(s.group(1))
            except: failures['json_valid'].append(p); continue
            items = data['@graph'] if (isinstance(data,dict) and '@graph' in data) else (data if isinstance(data,list) else [data])
            for it in items:
                if isinstance(it,dict) and it.get('@id') == ORG_ID:
                    org_ok = True
        if not org_ok:
            failures['org_jsonld'].append(p)

        # Rule 32 — FAQPage if visible FAQs
        if '<details>' in html or '<details ' in html:
            if '"@type":"FAQPage"' not in html and '"@type": "FAQPage"' not in html:
                failures['faq_schema'].append(p)

        # Rule 35 — directory URLs end in /
        for href in re.findall(r'<a\b[^>]*?\bhref="([^"]+)"', html):
            if re.match(r'^[\w-]+$', href):
                failures['dir_trailing_slash'].append((href, p))

        # Rule 38 — no .html/ trailing slash
        if re.search(r'\.html/(?:[#?]|")', html):
            failures['html_trailing_slash'].append(p)

        # Rule 41 — no microdata
        if re.search(r'\b(itemscope|itemtype|itemprop)\b', html):
            failures['microdata'].append(p)

        # SEO keyword placement (per [[seo-keyword-placement-rule]])
        # — primary keyword from slug. Each keyword WORD checked
        # independently (not exact-phrase match) because real content
        # uses natural word order: "Biddulph removals" and "removals
        # in Biddulph" both correctly target the "removals biddulph"
        # keyword. Combined word density 0.5-4.0% on the body.
        seo_kw = seo_primary_keyword(p)
        if seo_kw:
            kw_words = seo_kw.split()
            issues = []
            # Title — at least one keyword word should appear
            tm = re.search(r'<title>(.*?)</title>', html, re.S)
            title_text = tm.group(1).lower() if tm else ''
            if not any(w in title_text for w in kw_words):
                issues.append('not-in-title')
            # Meta description — at least one keyword word
            md = re.search(r'name="description"\s+content="([^"]*)"', html)
            desc_text = md.group(1).lower() if md else ''
            if not any(w in desc_text for w in kw_words):
                issues.append('not-in-meta-desc')
            # Image alt text — at least one alt should contain at
            # least one keyword word. SOFT check: recommendation,
            # not a build failure (logged separately below).
            alts = re.findall(r'<img[^>]+alt="([^"]*)"', html)
            if alts and not any(any(w in a.lower() for w in kw_words) for a in alts):
                seo_alt_recommendations.append((seo_kw, p))
            # Body density — sum of individual keyword-word occurrences
            # divided by total body word count, expressed as %
            main_m = re.search(r'<main[^>]*>(.*?)</main>', html, re.S)
            body_html = main_m.group(1) if main_m else html
            body_text = re.sub(r'<[^>]+>', ' ', body_html).lower()
            body_text = re.sub(r'\s+', ' ', body_text)
            body_word_count = len(body_text.split())
            if body_word_count >= SEO_BODY_MIN_WORDS:
                kw_count = sum(
                    len(re.findall(r'\b' + re.escape(w) + r'\b', body_text))
                    for w in kw_words
                )
                density = (kw_count / body_word_count) * 100
                if density < SEO_BODY_DENSITY_MIN:
                    issues.append(f'under-targeted({density:.2f}%)')
                elif density > SEO_BODY_DENSITY_MAX:
                    issues.append(f'stuffing-risk({density:.2f}%)')
            if issues:
                failures['seo_keyword_placement'].append((seo_kw, ', '.join(issues), p))

        # NSR EEAT — ≥4 of 7 signals (no BAR)
        signals = sum([
            'North Staffordshire Removals' in html,
            ('since 2010' in html.lower()) or ('15 years' in html.lower()) or ('fifteen years' in html.lower()),
            ('Stoke-on-Trent' in html) or ('Staffordshire' in html),
            '01782' in html,
            any(s in html.lower() for s in ('our team','our crew',"we've",'we have','we run')),
            ('fully covered' in html.lower()) or ('goods in transit' in html.lower()) or ('public liability' in html.lower()),
            'family-run' in html.lower() or 'family run' in html.lower(),
        ])
        if signals < 4:
            failures['eeat'].append((signals, p))

    # Cross-page duplicate detection
    for title, paths in titles_seen.items():
        if len(paths) > 1:
            failures['duplicate_titles'].append(f'"{title}" -> {paths}')
    for desc, paths in descs_seen.items():
        if len(paths) > 1:
            failures['duplicate_descriptions'].append(f'"{desc[:60]}…" -> {paths}')
    for h1, paths in h1s_seen.items():
        if len(paths) > 1:
            failures['duplicate_h1'].append(f'"{h1}" -> {paths}')

    # Image size check
    for f in glob.glob('images/*'):
        if os.path.isfile(f) and os.path.getsize(f) > IMAGE_MAX_BYTES:
            failures['image_size'].append((os.path.getsize(f), f))

    # Static files
    if not (os.path.exists('_headers') and
            all(h in open('_headers').read() for h in ('X-Frame-Options','X-Content-Type-Options','Referrer-Policy','Strict-Transport-Security'))):
        failures['headers_file'].append('missing or incomplete')
    if not os.path.exists('_redirects'):
        failures['redirects_file'].append('missing')
    if os.path.exists('robots.txt'):
        r = open('robots.txt').read()
        if 'Sitemap:' not in r or 'northstaffordshireremovals.co.uk' not in r:
            failures['robots_txt'].append('invalid')
    else:
        failures['robots_txt'].append('missing')

    # Report
    any_fail = False
    print('='*64)
    print('northstaffordshireremovals.co.uk — content rule audit')
    print('='*64)
    for name, fails in failures.items():
        if not fails:
            print(f'  ✓ {name}')
        else:
            any_fail = True
            print(f'  ✗ {name}: {len(fails)} failure(s)')
            for f in fails[:8]:
                if isinstance(f, tuple): print(f'      {f[0]}  →  {f[1]}')
                else: print(f'      {f}')
            if len(fails) > 8: print(f'      … +{len(fails)-8} more')
    print('='*64)
    print(f'  {sum(1 for v in failures.values() if not v)} / {len(failures)} rules pass.')
    # Soft recommendations — informational only, don't fail the build
    if seo_alt_recommendations:
        print()
        print(f'  ℹ {len(seo_alt_recommendations)} page(s) could improve image alt-text SEO')
        print(f'    (primary keyword absent from all <img alt> attributes — recommendation, not a failure):')
        for kw, p in seo_alt_recommendations[:8]:
            print(f'      kw="{kw}"  →  {p}')
        if len(seo_alt_recommendations) > 8:
            print(f'      … +{len(seo_alt_recommendations)-8} more')
    return 0 if not any_fail else 1


if __name__ == '__main__':
    sys.exit(audit())
