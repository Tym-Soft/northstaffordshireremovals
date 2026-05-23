#!/usr/bin/env python3
"""Single-page SEO + accessibility audit for the NSR home page.
Mirrors the 41 rules from markratcliffemoving.co.uk/tools/audit.py,
adapted: no BAR signal, NSR-specific EEAT set."""

from __future__ import annotations
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'index.html')
HTML = open(PAGE, encoding='utf-8').read()
BASE = 'https://www.northstaffordshireremovals.co.uk'

META_DESC_MAX = 145
TITLE_PX_MAX = 550
ALT_TEXT_MAX = 100
IMAGE_MAX_BYTES = 200 * 1024
BODY_LINKS_MIN = 10

CHAR_PX = {
    ' ':5,'!':5,'"':6,'#':11,'$':11,'%':17,'&':13,"'":4,'(':7,')':7,'*':8,
    '+':12,',':5,'-':7,'.':5,'/':6,'0':11,'1':11,'2':11,'3':11,'4':11,'5':11,
    '6':11,'7':11,'8':11,'9':11,':':6,';':6,'<':12,'=':12,'>':12,'?':11,'@':18,
    'A':12,'B':13,'C':14,'D':14,'E':13,'F':12,'G':15,'H':14,'I':6,'J':9,'K':13,
    'L':11,'M':16,'N':14,'O':15,'P':13,'Q':15,'R':14,'S':13,'T':12,'U':14,
    'V':12,'W':18,'X':12,'Y':12,'Z':12,'[':6,'\\':6,']':6,'^':9,'_':11,'`':6,
    'a':11,'b':12,'c':10,'d':12,'e':11,'f':7,'g':12,'h':12,'i':5,'j':5,'k':11,
    'l':5,'m':17,'n':12,'o':12,'p':12,'q':12,'r':7,'s':10,'t':7,'u':12,'v':10,
    'w':16,'x':11,'y':10,'z':10,'{':6,'|':5,'}':6,'~':12,'–':11,'—':14,
}
NON_DESC = {'click here','clickhere','read more','learn more','more','here',
            'this','click','continue reading','continue','link','this link',
            'more info','read','see more','view more','find out more','tap here'}

results = []
def check(name, ok, detail=''):
    results.append((name, ok, detail))

# ── parse body (between </header> and <footer>) ───
m_start = re.search(r'</header>', HTML)
m_end = re.search(r'<footer', HTML)
BODY = HTML[m_start.end():m_end.start()] if (m_start and m_end) else HTML
HEAD = HTML[:HTML.find('</head>')]

# Rule 3 — ≥10 in-body internal links
hrefs = re.findall(r'<a\b[^>]*?\bhref="([^"]+)"', BODY)
internal = set()
for h in hrefs:
    h0 = h.split('#')[0].split('?')[0]
    if not h0 or h0 in ('/','./','../'): continue
    if h0.startswith(('mailto:','tel:','javascript:','#')): continue
    if h0.startswith(('http://','https://','//')):
        if 'northstaffordshireremovals.co.uk' not in h: continue
        h0 = re.sub(r'^https?://(?:www\.)?northstaffordshireremovals\.co\.uk/', '', h0).lstrip('/')
    if h0.endswith('.html') or h0.endswith('/'):
        internal.add(h0)
check('R3  ≥10 in-body internal links', len(internal) >= BODY_LINKS_MIN, f'{len(internal)} unique')

# Rule 6 — title present (uniqueness across pages = not testable here)
title_m = re.search(r'<title>([^<]+)</title>', HTML, re.I)
title = title_m.group(1).strip() if title_m else ''
check('R6  Title present', bool(title), repr(title))

# Rule 7 — meta description ≤145
descs = re.findall(r'<meta\s+name="description"\s+content="([^"]*)"', HTML, re.I)
desc = descs[0] if descs else ''
check('R7  Meta description ≤145 chars', 0 < len(desc) <= META_DESC_MAX, f'{len(desc)} chars')

# Rule 8 — title pixel width ≤550
px = sum(CHAR_PX.get(c, 11) for c in title)
check('R8  Title pixel width ≤550px', px <= TITLE_PX_MAX, f'{px}px')

# Rule 9 — every <img> has alt (decorative may use alt="" + role/aria-hidden)
imgs = re.findall(r'<img\b[^>]*>', HTML)
missing_alt = [i for i in imgs if 'alt=' not in i]
check('R9  Every <img> has alt', len(missing_alt) == 0, f'{len(imgs)} imgs, {len(missing_alt)} missing alt')

# Rule 10 — static canonical to production URL
can_m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', HTML, re.I)
check('R10 Static canonical present', can_m is not None and can_m.group(1).startswith(BASE), can_m.group(1) if can_m else 'none')

# Rule 14 — canonical inside <head>
check('R14 Canonical inside <head>', bool(can_m) and HTML.find('<link rel="canonical"') < HTML.find('</head>'), '')

# Rule 15 — every <img> has width+height
no_dim = [i for i in imgs if 'width=' not in i or 'height=' not in i]
check('R15 Every <img> has width+height', len(no_dim) == 0, f'{len(no_dim)} missing dims')

# Rule 16 — descriptive anchor text
bad_anchors = []
for m in re.finditer(r'<a\b[^>]*>(.*?)</a>', BODY, re.S):
    txt = re.sub(r'<[^>]+>', '', m.group(1)).strip().lower()
    txt = re.sub(r'\s+', ' ', txt)
    if txt in NON_DESC:
        bad_anchors.append(txt)
check('R16 No non-descriptive anchor text', len(bad_anchors) == 0, f'{bad_anchors[:3]}' if bad_anchors else '')

# Rule 17 — non-empty accessible names on anchors
empty_a = 0
for m in re.finditer(r'<a\b([^>]*)>(.*?)</a>', BODY, re.S):
    attrs = m.group(1)
    inner = m.group(2)
    txt = re.sub(r'<[^>]+>', '', inner).strip()
    if txt: continue
    if 'aria-label=' in attrs: continue
    # check for img alt within
    img_alt = re.search(r'<img\b[^>]*\balt="([^"]*)"', inner)
    if img_alt and img_alt.group(1).strip(): continue
    empty_a += 1
check('R17 No empty-name anchors', empty_a == 0, f'{empty_a} empty')

# Rule 18 — <h1> is first heading
first_h = re.search(r'<h([1-6])\b', BODY)
check('R18 <h1> is first heading', first_h is not None and first_h.group(1) == '1', f'first={first_h.group(1) if first_h else None}')

# Rule 19 — alt ≤100 chars
long_alts = []
for i in imgs:
    am = re.search(r'\balt="([^"]*)"', i)
    if am and len(am.group(1)) > ALT_TEXT_MAX:
        long_alts.append(len(am.group(1)))
check('R19 alt ≤100 chars', len(long_alts) == 0, f'longest={max(long_alts) if long_alts else 0}')

# Rule 20 — CSP + Referrer-Policy meta
has_csp = 'Content-Security-Policy' in HEAD
has_ref = re.search(r'<meta\s+name="referrer"', HEAD, re.I) is not None
check('R20 CSP + Referrer-Policy meta', has_csp and has_ref, f'csp={has_csp} ref={has_ref}')

# Rule 21 — every image in /images/ ≤200KB
big_imgs = []
for f in os.listdir(os.path.join(ROOT, 'images')):
    p = os.path.join(ROOT, 'images', f)
    if os.path.isfile(p) and os.path.getsize(p) > IMAGE_MAX_BYTES:
        big_imgs.append(f)
check('R21 Images ≤200KB', len(big_imgs) == 0, f'{len(big_imgs)} oversized')

# Rule 22 — _headers present with required headers
hdr_path = os.path.join(ROOT, '_headers')
headers_ok = False
if os.path.exists(hdr_path):
    hdr = open(hdr_path).read()
    headers_ok = all(h in hdr for h in ('X-Frame-Options','X-Content-Type-Options','Referrer-Policy','Strict-Transport-Security'))
check('R22 _headers with required directives', headers_ok, '')

# Rule 23 — _redirects exists
check('R23 _redirects file present', os.path.exists(os.path.join(ROOT, '_redirects')), '')

# Rule 24 — no URL parameters in internal anchors
param_links = [h for h in hrefs if '?' in h and not h.startswith(('http://','https://','mailto:','tel:'))]
check('R24 No URL parameters in internal anchors', len(param_links) == 0, f'{param_links}')

# Rule 26 — exactly one <h1>
h1_count = len(re.findall(r'<h1\b', HTML))
check('R26 Exactly one <h1>', h1_count == 1, f'{h1_count} h1 tags')

# Rule 27 — no mixed content (no http:// resources)
mixed = re.findall(r'\bhttp://[^\s"\'<>]+', HTML)
# filter known schema URLs like http://schema.org -> not loaded, but be strict
mixed_real = [x for x in mixed if not x.startswith('http://schema.org')]
check('R27 No mixed content', len(mixed_real) == 0, f'{mixed_real[:3]}')

# Rule 28 — robots.txt exists & lists sitemap
robots_path = os.path.join(ROOT, 'robots.txt')
robots_ok = False
if os.path.exists(robots_path):
    r = open(robots_path).read()
    robots_ok = 'Sitemap:' in r and 'northstaffordshireremovals.co.uk' in r
check('R28 robots.txt valid', robots_ok, '')

# Rule 29 — ≥4 EEAT signals (NSR-adapted, no BAR)
signals = {
    'brand': 'North Staffordshire Removals' in BODY,
    'longevity (2010 / 15 yrs)': ('since 2010' in BODY) or ('15 years' in BODY) or ('15 yrs' in BODY) or ('fifteen years' in BODY),
    'locality (Stoke / Staffordshire)': ('Stoke-on-Trent' in BODY) or ('Staffordshire' in BODY),
    'phone (01782)': '01782' in BODY,
    'first-person (our team/our crew/we have)': any(s in BODY for s in ('our team','our crew',"we've",'we have','we run','we sell')),
    'insurance/trust signal': any(s in BODY for s in ('insured','insurance','Public Liability','Goods in Transit')),
    'family-run signal': 'family-run' in BODY.lower(),
}
passing = sum(signals.values())
check('R29 ≥4 EEAT signals (no-BAR variant)', passing >= 4, f'{passing}/7 — {signals}')

# Rule 30 — Organization JSON-LD with @id
org_ok = False
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S):
    try:
        data = json.loads(m.group(1))
    except: continue
    items = data if isinstance(data, list) else [data]
    if isinstance(data, dict) and '@graph' in data: items = data['@graph']
    for it in items:
        if isinstance(it, dict) and '@id' in it and 'organization' in it.get('@id',''):
            org_ok = True; break
check('R30 Organization JSON-LD with @id', org_ok, '')

# Rule 31 — all JSON-LD valid
invalid = 0
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S):
    try: json.loads(m.group(1))
    except: invalid += 1
check('R31 All JSON-LD valid', invalid == 0, f'{invalid} invalid')

# Rule 32 — FAQPage schema present if visible FAQs
has_faq_visible = '<details>' in BODY
has_faq_schema = '"@type":"FAQPage"' in HTML or '"@type": "FAQPage"' in HTML
check('R32 FAQPage schema when FAQs visible', (not has_faq_visible) or has_faq_schema, f'visible={has_faq_visible} schema={has_faq_schema}')

# Rule 33 — exactly one <meta name="description">
check('R33 Exactly one meta description', len(descs) == 1, f'{len(descs)} found')

# Rule 34 — no JS-injected canonical (no createElement canonical)
js_canon = 'rel="canonical"' in HTML.split('</head>',1)[1] if '</head>' in HTML else False
check('R34 No JS-injected canonical', not js_canon, '')

# Rule 35 — directory URLs end in /
dir_no_slash = []
for h in hrefs:
    h0 = h.split('#')[0].split('?')[0]
    if h0.startswith(('http://','https://','mailto:','tel:','#','/')): pass
    # check pattern like services or areas-covered without trailing slash
    if re.match(r'^[\w-]+$', h0):  # e.g. "services"
        dir_no_slash.append(h0)
check('R35 Directory URLs have trailing slash', len(dir_no_slash) == 0, f'{dir_no_slash}')

# Rule 38 — no .html/ (trailing slash on .html file)
bad_trail = [h for h in hrefs if re.search(r'\.html/(?:[#?]|$)', h)]
check('R38 No trailing slash on .html URLs', len(bad_trail) == 0, '')

# Rule 41 — no microdata attrs
md = re.search(r'\b(itemscope|itemtype|itemprop)\b', HTML)
check('R41 No HTML microdata attributes', md is None, '')

# Report
print('=' * 64)
print('northstaffordshireremovals.co.uk — home page SEO audit')
print('=' * 64)
fails = 0
for name, ok, detail in results:
    mark = '✓' if ok else '✗'
    line = f'  {mark} {name}'
    if detail: line += f'  ({detail})'
    print(line)
    if not ok: fails += 1
print('=' * 64)
print(f'  {len(results) - fails} / {len(results)} rules pass.')
sys.exit(0 if fails == 0 else 1)
