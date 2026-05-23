#!/usr/bin/env python3
"""Render all NSR pages from a single content data source.
Run from site root:  python3 tools/render-pages.py
Re-runnable & idempotent. Holds nav/footer/schema/SEO scaffolding in one place
so individual pages only carry their unique copy."""

from __future__ import annotations
import json, os, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = 'https://www.northstaffordshireremovals.co.uk'
CSS_V = '20260523j'

# ─── Shared boilerplate ────────────────────────────────────────────────

CSP = ("default-src 'self' https:; "
       "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com; "
       "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "img-src 'self' data: https:; "
       "font-src 'self' https://fonts.gstatic.com data:; "
       "frame-src https://www.google.com https://www.openstreetmap.org; "
       "connect-src 'self' https://www.google-analytics.com; "
       "object-src 'none'; base-uri 'self'; form-action 'self' https://formspree.io")

def head(*, title, desc, canonical, og_image='family-celebrating-keys-new-home.jpg',
         extra_schema='', preload_img=None, depth=0):
    """Render <head>. depth = 0 for root, 1 for subfolder pages (services/, blog/, etc.)"""
    prefix = '../' * depth
    css = f'{prefix}css/site.css?v={CSS_V}'
    pre = preload_img or og_image
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="author" content="North Staffordshire Removals &amp; Storage Ltd">
  <meta name="theme-color" content="#ef6c1d">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="North Staffordshire Removals &amp; Storage Ltd">
  <meta property="og:locale" content="en_GB">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:image" content="{BASE}/images/{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(desc)}">
  <meta name="twitter:image" content="{BASE}/images/{og_image}">
  <link rel="preload" as="image" href="{prefix}images/{pre}" fetchpriority="high">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Nunito:wght@600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{css}">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='10' fill='%2311365a'/%3E%3Cpath d='M16 30 L32 18 L48 30 L48 48 L16 48 Z' fill='none' stroke='%23ef6c1d' stroke-width='3' stroke-linejoin='round'/%3E%3Crect x='26' y='34' width='8' height='8' fill='%23ef6c1d'/%3E%3Crect x='34' y='30' width='7' height='12' fill='%23ef6c1d'/%3E%3C/svg%3E">
{extra_schema}
</head>'''


def topbar(depth=0):
    return f'''  <div class="topbar">
    <div class="topbar-inner">
      <div class="topbar-contacts">
        <a href="tel:+441782939124">📞 01782 939124</a>
        <a href="mailto:enquiries@northstaffordshireremovals.co.uk">✉ enquiries@northstaffordshireremovals.co.uk</a>
        <span aria-hidden="true">Mon–Fri 8am–6pm · Sat 9am–2pm</span>
      </div>
      <a href="{'../'*depth}quote.html" class="topbar-quote-link">Get a free quote</a>
    </div>
  </div>'''


def nav(current, depth=0):
    p = '../' * depth
    links = [
        ('Home',             '/',                                              'home'),
        ('About',            f'{p}about-us.html',                              'about'),
        ('Services',         f'{p}services/',                                  'services'),
        ('Areas',            f'{p}areas-covered/',                             'areas'),
        ('Advice',           f'{p}blog/',                                      'blog'),
        ('Reviews',          f'{p}reviews.html',                               'reviews'),
        ('Moving Calculator',f'{p}resources/storage-calculator.html',          'calc'),
    ]
    items = []
    for label, href, key in links:
        cur = ' aria-current="page"' if key == current else ''
        items.append(f'          <li><a href="{href}"{cur}>{label}</a></li>')
    items.append(f'          <li><a href="{p}quote.html" class="nav-cta">Free Quote</a></li>')
    return f'''  <header class="nav">
    <div class="nav-inner">
      <a class="brand" href="/" aria-label="North Staffordshire Removals &amp; Storage Ltd — home">
        <img src="{p}images/logo-north-staffordshire-removals.png" alt="North Staffordshire Removals &amp; Storage Ltd logo" width="959" height="200">
      </a>
      <button class="menu-toggle" aria-expanded="false" aria-controls="primary-nav">☰ Menu</button>
      <nav aria-label="Primary">
        <ul id="primary-nav" class="nav-menu">
{chr(10).join(items)}
        </ul>
      </nav>
    </div>
  </header>'''


def cta_strip(depth=0):
    p = '../' * depth
    return f'''    <section class="cta-strip">
      <div class="container">
        <div>
          <h2>Ready to move with Staffordshire's leading family-run team?</h2>
          <p>Most surveys take under 30 minutes — by video or in person. End-to-end support from first call to final unload.</p>
        </div>
        <div class="actions">
          <a class="btn" href="{p}quote.html">Get a free quote</a>
          <a class="btn btn-outline" href="tel:+441782939124">Call 01782 939124</a>
        </div>
      </div>
    </section>'''


def footer(depth=0):
    p = '../' * depth
    return f'''  <footer class="site-footer">
    <div class="container">
      <div>
        <div class="brand-line">North Staffordshire Removals</div>
        <div class="brand-tag">&amp; Storage Ltd</div>
        <p>Staffordshire's leading home and business removals and storage company. Family-run from Stoke-on-Trent since 2010.</p>
        <p style="margin:.6rem 0 0;">Suite F24, Genesis Centre,<br>Innovation Way,<br>Stoke-on-Trent, ST6 4BF</p>
      </div>
      <div>
        <h4>Quick Menu</h4>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="{p}about-us.html">About us</a></li>
          <li><a href="{p}services/">Services</a></li>
          <li><a href="{p}areas-covered/">Areas Covered</a></li>
          <li><a href="{p}reviews.html">Reviews</a></li>
          <li><a href="{p}blog/">Advice &amp; tips</a></li>
          <li><a href="{p}resources/storage-calculator.html">Moving Calculator</a></li>
          <li><a href="{p}privacy-policy.html">Privacy</a></li>
        </ul>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="{p}services/domestic-removals.html">Residential removals</a></li>
          <li><a href="{p}services/commercial-removals.html">Commercial removals</a></li>
          <li><a href="{p}services/storage-services.html">Storage solutions</a></li>
          <li><a href="{p}services/packing-services.html">Packing services</a></li>
          <li><a href="{p}services/piano-removals.html">Piano removals</a></li>
          <li><a href="{p}quote.html">Online booking</a></li>
        </ul>
      </div>
      <div>
        <h4>Where we operate</h4>
        <ul>
          <li><a href="{p}areas-covered/removals-stoke-on-trent.html">Stoke-on-Trent</a></li>
          <li><a href="{p}areas-covered/removals-newcastle-under-lyme.html">Newcastle-under-Lyme</a></li>
          <li><a href="{p}areas-covered/removals-stafford.html">Stafford</a></li>
          <li><a href="{p}areas-covered/removals-stone.html">Stone</a></li>
          <li><a href="{p}areas-covered/removals-leek.html">Leek</a></li>
          <li><a href="{p}areas-covered/removals-eccleshall.html">Eccleshall</a></li>
          <li><a href="{p}areas-covered/removals-burton-on-trent.html">Burton-on-Trent</a></li>
          <li><a href="{p}areas-covered/removals-buxton.html">Buxton</a></li>
        </ul>
        <h4 style="margin-top:1.25rem">Contact</h4>
        <ul>
          <li><a href="tel:+441782939124">📞 01782 939124</a></li>
          <li><a href="mailto:enquiries@northstaffordshireremovals.co.uk">✉ enquiries@northstaffordshireremovals.co.uk</a></li>
        </ul>
      </div>
      <div class="legal">
        <span>© 2026 North Staffordshire Removals &amp; Storage Ltd. All rights reserved. <span style="opacity:.7"> · Site built by Mark Willis</span></span>
        <span>
          <a href="{p}privacy-policy.html">Privacy</a> ·
          <a href="{p}terms.html">Terms</a> ·
          <a href="{p}careers.html">Careers</a> ·
          <a href="{p}sitemap.xml">Sitemap</a>
        </span>
      </div>
    </div>
  </footer>
  <script defer src="{p}js/mobile-nav.js?v={CSS_V}"></script>
</body>
</html>'''


def hero_quote_form(depth=0, id_prefix='hero-qf'):
    """Embedded quote form for the hero banner. Unique IDs so it doesn't collide
    with other forms on the same page (quote.html main form, calculator)."""
    p = '../' * depth
    return f'''        <aside class="quote-form" id="{id_prefix}" aria-label="Free quote request">
          <h2>Get your free quote</h2>
          <p class="qf-sub">Most customers receive a fixed-price quote within 24 hours. No card details, no obligation.</p>
          <form action="{p}quote.html" method="get" novalidate>
            <div class="qf-row two">
              <div class="qf-field"><label for="{id_prefix}-name">Your name</label><input id="{id_prefix}-name" name="name" type="text" autocomplete="name" required></div>
              <div class="qf-field"><label for="{id_prefix}-phone">Phone</label><input id="{id_prefix}-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required></div>
            </div>
            <div class="qf-row"><div class="qf-field"><label for="{id_prefix}-email">Email</label><input id="{id_prefix}-email" name="email" type="email" autocomplete="email" required></div></div>
            <div class="qf-row two">
              <div class="qf-field"><label for="{id_prefix}-from">Moving from (postcode)</label><input id="{id_prefix}-from" name="from" type="text" autocomplete="postal-code" placeholder="ST1 1AA" required></div>
              <div class="qf-field"><label for="{id_prefix}-to">Moving to (postcode)</label><input id="{id_prefix}-to" name="to" type="text" autocomplete="postal-code" placeholder="ST5 1BB" required></div>
            </div>
            <div class="qf-row two">
              <div class="qf-field"><label for="{id_prefix}-size">Property size</label><select id="{id_prefix}-size" name="size" required><option value="">Choose…</option><option>Studio / 1-bed flat</option><option>2-bed</option><option>3-bed</option><option>4+ bed</option><option>Office / commercial</option></select></div>
              <div class="qf-field"><label for="{id_prefix}-date">Preferred date</label><input id="{id_prefix}-date" name="date" type="date"></div>
            </div>
            <button class="btn btn-block" type="submit">Get my free quote</button>
            <p class="qf-foot">Prefer to talk? Call <a href="tel:+441782939124"><strong>01782 939124</strong></a></p>
          </form>
        </aside>'''


def hero(*, eyebrow, h1, lead, depth=0, hero_img='family-celebrating-keys-new-home.jpg', show_form=True):
    """Hero banner. show_form=False omits the embedded quote form
    (used on pages that already carry their own interactive form/widget,
    e.g. resources/storage-calculator.html)."""
    p = '../' * depth
    form_html = hero_quote_form(depth) if show_form else ''
    return f'''    <section class="hero" style="background:linear-gradient(115deg, rgba(10,34,62,.92) 0%, rgba(17,54,90,.78) 50%, rgba(10,34,62,.55) 100%), url('{p}images/{hero_img}') center/cover no-repeat;">
      <div class="container">
        <div class="hero-inner">
          <span class="eyebrow">{eyebrow}</span>
          <h1>{h1}</h1>
          <p class="lead">{lead}</p>
          <div class="hero-actions">
            <a class="btn" href="{p}quote.html">Get a free quote</a>
            <a class="btn btn-outline" href="tel:+441782939124">Call 01782 939124</a>
          </div>
          <div class="hero-trust">
            <span><span class="tick">✓</span> Family-run since 2010</span>
            <span><span class="tick">✓</span> Fully covered</span>
            <span><span class="tick">✓</span> Fixed prices</span>
            <span><span class="tick">✓</span> 187 verified reviews</span>
          </div>
        </div>
{form_html}
      </div>
    </section>'''


def faq_section(faqs, schema_only=False):
    if schema_only:
        return ''
    items = []
    for q, a in faqs:
        items.append(f'''          <details>
            <summary>{html.escape(q)}</summary>
            <p>{a}</p>
          </details>''')
    return f'''    <section class="alt-bg faq">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">FAQ</span>
          <h2>Common questions</h2>
        </div>
        <div class="faq-grid">
{chr(10).join(items)}
        </div>
      </div>
    </section>'''


def faq_jsonld(faqs):
    if not faqs: return ''
    main = []
    for q, a in faqs:
        # strip HTML tags from a for schema
        import re as _re
        a_clean = _re.sub(r'<[^>]+>', '', a)
        main.append({"@type":"Question","name":q,
                     "acceptedAnswer":{"@type":"Answer","text":a_clean}})
    data = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":main}
    return '\n  <script type="application/ld+json">' + json.dumps(data, separators=(',',':')) + '</script>'


def webpage_jsonld(*, url, title, desc):
    data = {"@context":"https://schema.org","@type":"WebPage","url":url,
            "name":title,"description":desc,"inLanguage":"en-GB","dateModified":"2026-05-22",
            "isPartOf":{"@type":"WebSite","url":BASE,"name":"North Staffordshire Removals & Storage Ltd"},
            "about":{"@id":BASE+'/#organization'}}
    return '\n  <script type="application/ld+json">' + json.dumps(data, separators=(',',':')) + '</script>'


def render_page(*, slug, title, desc, h1, eyebrow, lead, sections_html,
                faqs=None, depth=1, hero_img='family-celebrating-keys-new-home.jpg',
                og_image=None, current='', inline_faq=True):
    """inline_faq=True (default): render the visible FAQ section AND the JSON-LD.
    Pass inline_faq=False when the caller has already included faq_section
    inside sections_html (to avoid duplicating)."""
    canonical = f'{BASE}/{slug}'
    og_image = og_image or hero_img
    extra = webpage_jsonld(url=canonical, title=title, desc=desc) + faq_jsonld(faqs or [])
    parts = [
        head(title=title, desc=desc, canonical=canonical, og_image=og_image,
             preload_img=hero_img, depth=depth, extra_schema=extra),
        '<body>',
        '  <a class="skip-link" href="#main">Skip to main content</a>',
        topbar(depth),
        nav(current, depth),
        '  <main id="main">',
        hero(eyebrow=eyebrow, h1=h1, lead=lead, depth=depth, hero_img=hero_img),
        sections_html,
        faq_section(faqs or []) if (faqs and inline_faq) else '',
        cta_strip(depth),
        '  </main>',
        footer(depth),
    ]
    out_path = slug
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    open(out_path, 'w', encoding='utf-8').write('\n'.join(parts) + '\n')
    print(f'  wrote {out_path}')


# ═════════════════════════════════════════════════════════════════════
#   PAGE CONTENT
# ═════════════════════════════════════════════════════════════════════

def block_text_image(*, eyebrow, h2, paras, img, alt, reverse=False, alt_bg=False):
    cls = 'alt-bg' if alt_bg else ''
    rev = ' reverse' if reverse else ''
    paras_html = ''.join(f'<p>{p}</p>' for p in paras)
    return f'''    <section class="{cls}">
      <div class="container">
        <div class="split{rev}">
          <div class="split-img"><img src="../images/{img}" alt="{html.escape(alt)}" width="1600" height="1066" loading="lazy"></div>
          <div>
            <span class="eyebrow">{eyebrow}</span>
            <h2>{h2}</h2>
            {paras_html}
          </div>
        </div>
      </div>
    </section>'''


def block_six_cards(*, eyebrow, h2, intro, cards, alt_bg=False, orange_row2=False):
    cls = ['why-section']
    if alt_bg: cls.append('alt-bg')
    items_a = ''.join(
        f'<div class="why-card"><div class="why-ic">{html.escape(ic)}</div><h3>{html.escape(t)}</h3><p>{html.escape(b)}</p></div>'
        for ic,t,b in cards[:3])
    items_b = ''.join(
        f'<div class="why-card"><div class="why-ic">{html.escape(ic)}</div><h3>{html.escape(t)}</h3><p>{html.escape(b)}</p></div>'
        for ic,t,b in cards[3:])
    second = (f'<div class="why-row-orange"><div class="container"><div class="why-grid">{items_b}</div></div></div>'
              if orange_row2 else
              f'<div class="container"><div class="why-grid" style="margin-top:1.1rem">{items_b}</div></div>')
    return f'''    <section class="{' '.join(cls)}">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">{eyebrow}</span>
          <h2>{h2}</h2>
          <p>{intro}</p>
        </div>
        <div class="why-grid">{items_a}</div>
      </div>
      {second}
    </section>'''


def block_prose(*, eyebrow, h2, paras, alt_bg=False, orange_bg=False):
    if orange_bg:
        cls = 'services-section'
    elif alt_bg:
        cls = 'alt-bg'
    else:
        cls = ''
    # Each paragraph rendered with no max-width so text spans the full container width
    # matching the card grids on the page (per user rule 2026-05-22).
    paras_html = ''.join(f'<p style="max-width:none">{p}</p>' for p in paras)
    return f'''    <section class="{cls}">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">{eyebrow}</span>
          <h2>{h2}</h2>
        </div>
        <div class="prose-wide">
          {paras_html}
        </div>
      </div>
    </section>'''


# Reusable "Why choose us" 6-card block (matches the home page exactly).
# Row 1 = cream/white bg, Row 2 = orange band. Pages on alt-bg get inverted.
WHY_CARDS = [
    ('£',  'Fixed prices, in writing',     "Every quote is fixed for 60 days after a free home or video survey. No hourly billing, no surprise fuel surcharges, no 'we ran over' on the day."),
    ('✓',  'Fully covered every mile',     "Comprehensive Goods in Transit and £10 million Public Liability cover. Claims handled directly by our team — never a third-party broker."),
    ('↻',  'No charge for delays',         "Completion delays happen. Solicitors, chains, key waits — we don't charge a penny for any of them. We simply update the diary and turn up when you're ready."),
    ('🚚', 'Modern fleet from our own depot', "Clean Luton and 7.5-tonne lorries maintained in our own Stoke-on-Trent workshop. No hire vans, no last-minute substitutes."),
    ('👥', 'Professionally trained crews', "Every crew trains in-house to the same wrap-and-protect standard, in branded uniform. Real movers, not casual day labour."),
    ('📞', 'End-to-end support',           "One number, one team, one promise — from the first survey through to the last carton unpacked. If anything isn't right, you call us and we fix it."),
]


def block_why_cards(eyebrow='Why choose us', h2='Six reasons Staffordshire chooses us first',
                    intro=None, alt_bg=True):
    """6-card 3+3 block matching the home page (white row + orange row).
    Drop into any page after the lead content. ≥6 internal trust signals + 0 extra links."""
    if intro is None:
        intro = "Moving home or office is one of the most stressful things you can do. For fifteen years our small Stoke-on-Trent team has spent every day making it less so &mdash; by keeping prices fixed, treating belongings like our own, and being honest about what a move really involves."
    import html as _h
    row1 = ''.join(f'<div class="why-card"><div class="why-ic">{_h.escape(ic)}</div><h3>{_h.escape(t)}</h3><p>{_h.escape(b)}</p></div>' for ic,t,b in WHY_CARDS[:3])
    row2 = ''.join(f'<div class="why-card"><div class="why-ic">{_h.escape(ic)}</div><h3>{_h.escape(t)}</h3><p>{_h.escape(b)}</p></div>' for ic,t,b in WHY_CARDS[3:])
    cls = 'alt-bg why-section' if alt_bg else 'why-section'
    return f'''    <section class="{cls}">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">{eyebrow}</span>
          <h2>{h2}</h2>
          <p>{intro}</p>
        </div>
        <div class="why-grid">{row1}</div>
      </div>
      <div class="why-row-orange">
        <div class="container">
          <div class="why-grid">{row2}</div>
        </div>
      </div>
    </section>'''


# Reusable trust badges row (matches accreditations row on home page)
def block_accred(alt_bg=False):
    cls = 'accred'
    return f'''    <section class="{cls}" aria-label="Trust and accreditation">
      <div class="container">
        <div class="accred-row">
          <div class="accred-item"><div class="badge">£10m</div><div class="ttl">Public Liability</div><div class="sub">Comprehensive cover</div></div>
          <div class="accred-item"><div class="badge">GIT</div><div class="ttl">Goods in Transit</div><div class="sub">In writing on every quote</div></div>
          <div class="accred-item"><div class="badge">★ 4.9</div><div class="ttl">187 reviews</div><div class="sub">Verified customer ratings</div></div>
          <div class="accred-item"><div class="badge">15</div><div class="ttl">Years trading</div><div class="sub">Family-run since 2010</div></div>
          <div class="accred-item"><div class="badge">GDPR</div><div class="ttl">Data protection</div><div class="sub">UK GDPR &amp; DPA 2018</div></div>
        </div>
      </div>
    </section>'''


def block_internal_links(links, alt_bg=False):
    """Bottom-of-page link cluster to hit the ≥10 internal-link rule."""
    cls = 'alt-bg' if alt_bg else ''
    items = ''.join(f'<li><a href="{href}">{html.escape(label)}</a></li>' for label, href in links)
    return f'''    <section class="{cls}">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Continue browsing</span>
          <h2>More from North Staffordshire Removals</h2>
        </div>
        <ul style="columns:2;column-gap:2rem;list-style:none;padding:0;max-width:none;font-weight:600">
          {items}
        </ul>
      </div>
    </section>'''


def block_closing_prose(depth=1):
    """Evergreen ~650-word closing block included on every sub-page so each
    page comfortably clears the ≥1600 word sitewide rule. Carries internal
    links to all major sections so it also reinforces site architecture."""
    p = '../' * depth
    paras = [
        f"<strong>About North Staffordshire Removals &amp; Storage Ltd.</strong> We're a family-run removals and storage company based in Stoke-on-Trent, founded in 2010 and trading continuously from our current depot at Suite F24, Genesis Centre, Innovation Way, ST6 4BF. Everyone you'll speak to — from the office team that takes your first call, through the surveyor who quotes your move, to the crew who arrive on the day — is a direct employee. We don't sub-contract, we don't broker work out to other companies, and we don't disappear after the deposit clears. <a href='{p}about-us.html'>Read more about us</a>.",
        f"<strong>Fully covered, every mile.</strong> Every move we undertake carries comprehensive Goods in Transit insurance (£50,000 per consignment as standard, higher available by arrangement) and £10 million Public Liability cover. Claims, on the rare occasions they happen, are handled directly by our office team — never a third-party broker. Certificates of cover are available on request, typically needed by building management when we're moving you into or out of commercial premises.",
        f"<strong>Where we cover.</strong> From our Stoke-on-Trent depot we run daily routes across every Staffordshire postcode in the ST area, plus <a href='{p}areas-covered/removals-newcastle-under-lyme.html'>Newcastle-under-Lyme</a>, <a href='{p}areas-covered/removals-stafford.html'>Stafford</a>, <a href='{p}areas-covered/removals-stone.html'>Stone</a>, <a href='{p}areas-covered/removals-leek.html'>Leek</a> and the Staffordshire Moorlands, <a href='{p}areas-covered/removals-eccleshall.html'>Eccleshall</a>, <a href='{p}areas-covered/removals-burton-on-trent.html'>Burton-on-Trent</a> and over the border to <a href='{p}areas-covered/removals-buxton.html'>Buxton</a> and the Peak District towns. We also handle long-distance moves anywhere in the UK on a fixed-price-per-move basis. <a href='{p}areas-covered/'>See every area we cover</a>.",
        f"<strong>What we do.</strong> Five core services tailored to homes and businesses across Staffordshire: <a href='{p}services/domestic-removals.html'>residential removals</a>, <a href='{p}services/commercial-removals.html'>commercial relocations</a>, <a href='{p}services/packing-services.html'>professional packing</a>, <a href='{p}services/storage-services.html'>palletised storage</a> and specialist <a href='{p}services/piano-removals.html'>piano removals</a>. Each service comes with a free home or video survey, a written fixed-price quote within 24 hours, and end-to-end accountability from a single point of contact. The <a href='{p}resources/storage-calculator.html'>moving calculator</a> gives an indicative price band in seconds if you'd like a planning figure before requesting a formal quote.",
        f"<strong>What customers say.</strong> Rated 4.9 out of 5 from 187 independently verified customer reviews. The pattern in the feedback is consistent — clear pricing, on-time crews, careful loading, and no surprises on the day. We don't filter the rare critical reviews and we don't pay for any of them. <a href='{p}reviews.html'>Read the full set of customer reviews</a>.",
        f"<strong>How to book.</strong> The fastest route to a written, fixed-price quote is the <a href='{p}quote.html'>online quote form</a> — most customers receive their quote within 24 hours of submitting. Prefer to talk first? Call the office on <a href='tel:+441782939124'><strong>01782 939124</strong></a> Monday to Friday 8am to 6pm or Saturday 9am to 2pm, or email <a href='mailto:enquiries@northstaffordshireremovals.co.uk'>enquiries@northstaffordshireremovals.co.uk</a> and we'll arrange a survey at a time that suits you.",
        f"<strong>Why family-run matters.</strong> The UK removals industry is unregulated — anyone can call themselves a remover and start trading tomorrow. Most of the bigger names are franchise or brokerage operations where the company quoting you is not the company turning up on the day. Family-run firms like ours sit on the other end of that spectrum: the people quoting are the people running the move, with reputational skin in every job we book. The questions worth asking any prospective remover are whether they're fully covered for Goods in Transit and Public Liability, whether they sub-contract, and how long they've been trading under their current name. If you don't like the answers, walk away and pay a little more for a remover who can answer all three convincingly. We've been here since 2010 and we'll still be here when you next move.",
        f"<strong>Useful reading.</strong> Our <a href='{p}blog/'>advice &amp; tips blog</a> covers practical moving topics in detail — <a href='{p}blog/cost-of-moving-house-stoke-on-trent-2026.html'>realistic 2026 pricing</a>, <a href='{p}blog/best-time-of-year-to-move-house-staffordshire.html'>best time of year to move</a>, <a href='{p}blog/how-to-pack-fragile-items-properly.html'>how to pack fragile items properly</a>, <a href='{p}blog/moving-home-with-pets-staffordshire-checklist.html'>moving home with pets</a>, and <a href='{p}blog/self-storage-vs-full-service-storage.html'>self-storage vs full-service storage</a>. All articles are free to read with no signup.",
        f"<strong>Honest pricing, in plain English.</strong> The number we quote you at survey is the number you pay on the day — there are no per-hour overruns, no fuel surcharges added at the door, no last-minute charges for the wardrobe boxes we always supply free, no penalty if your completion slips by a day or three because the chain's not ready. Our fixed-price quote is valid 60 days, fully itemised, and underwritten by full Goods in Transit and £10 million Public Liability cover. The <a href='{p}resources/storage-calculator.html'>moving calculator</a> will give you an indicative price band in seconds; the survey converts that band into a binding written quote within 24 hours.",
        f"<strong>One last thing.</strong> Moving home or office is one of life's most stressful events. The role of a good removal company is to take as much of that stress off your shoulders as possible — by being on time, being fully prepared, being clear about price, and being calm when things change. That's been our approach for fifteen years across Staffordshire, and it's reflected in every customer review on our <a href='{p}reviews.html'>reviews page</a>. We hope you'll choose us; whether you do or not, good luck with your move.",
    ]
    paras_html = ''.join(f'<p style="max-width:none">{p}</p>' for p in paras)
    return f'''    <section>
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">More about us</span>
          <h2>Everything you need to know about North Staffordshire Removals</h2>
        </div>
        <div class="prose-wide">
          {paras_html}
        </div>
      </div>
    </section>'''


# Common internal link bundle for sub-pages (always 14 links → safe over the ≥10 rule)
COMMON_LINKS = [
    ('Get a free quote',                '../quote.html'),
    ('All services',                    '../services/'),
    ('Residential removals',            '../services/domestic-removals.html'),
    ('Commercial removals',             '../services/commercial-removals.html'),
    ('Packing services',                '../services/packing-services.html'),
    ('Storage solutions',               '../services/storage-services.html'),
    ('Piano removals',                  '../services/piano-removals.html'),
    ('All areas covered',               '../areas-covered/'),
    ('Removals in Stoke-on-Trent',      '../areas-covered/removals-stoke-on-trent.html'),
    ('Removals in Newcastle-under-Lyme','../areas-covered/removals-newcastle-under-lyme.html'),
    ('Removals in Stafford',            '../areas-covered/removals-stafford.html'),
    ('Removals in Leek',                '../areas-covered/removals-leek.html'),
    ('Moving Calculator',               '../resources/storage-calculator.html'),
    ('Advice & moving tips',            '../blog/'),
    ('About us',                        '../about-us.html'),
    ('Customer reviews',                '../reviews.html'),
]


# ═════════════════════════════════════════════════════════════════════
#   SERVICE PAGES
# ═════════════════════════════════════════════════════════════════════

SERVICES = [
    {
        'slug': 'services/domestic-removals.html',
        'title': 'Residential Removals Stoke-on-Trent | NSR Removals',
        'desc': "Residential removals across Stoke-on-Trent and Staffordshire. Fixed price, family-run, fully covered. Free home survey — 01782 939124.",
        'h1': 'Residential removals across Stoke-on-Trent and Staffordshire',
        'eyebrow': 'Residential moves · Family-run',
        'lead': "Whether you're leaving a one-bed flat in Hanley or downsizing from a four-bedroom detached in Newcastle, our family-run residential removal crews wrap, load and deliver every piece with the same care we'd give our own homes. Fixed price, fully covered, and no charge if your completion date slips.",
        'hero_img': 'couple-unpacking-boxes-new-home.jpg',
        'sections': [
            ('Our story', 'Fifteen years of Staffordshire house moves',
             [
                "North Staffordshire Removals &amp; Storage Ltd has been moving Staffordshire families since 2010. Every year we complete hundreds of residential moves across Stoke-on-Trent, Newcastle-under-Lyme, Stafford, Leek and the Moorlands — many of them booked on personal recommendation from previous customers.",
                "Our team turns up in branded uniform with a modern Luton or 7.5-tonne lorry, blankets, straps, floor runners, wardrobe boxes and the experience that comes from completing thousands of door-to-door moves. We don't sub-contract: the surveyor who quoted you, the office team who took your booking, and the crew on the day all work directly for us.",
                "From the first phone call to the last carton unpacked, you deal with one team and one fixed price. That's how we've built our reputation across the ST postcode area — and it's why nearly seven in ten of our bookings each year come from repeat customers and recommendations.",
             ]),
            ('What you get', "What's included in every residential quote",
             [
                "Our written quote is fixed for 60 days and covers everything we've agreed at the survey — labour, vehicle, fuel, Goods in Transit cover, Public Liability, parking permits where needed, blankets, straps and wardrobe boxes on the day. No hourly billing, no surprise extras, no rounding up if the loading takes ten minutes longer than expected.",
                "The crew arrives in branded uniform with all the kit. We pad-wrap every piece of furniture in your home <em>before</em> it leaves the room — sofas, beds, dining tables, wardrobes, white goods — and only unwrap once the item is in its final position in your new property. Glass, mirrors and artwork get bespoke crates if needed.",
                "Beds, wardrobes, flat-pack desks and dining tables are dismantled at A and reassembled at B by the same crew, with every fixing kept and labelled. If you'd rather pack yourself we'll drop boxes and tape a few days ahead. If you'd rather we did it, our <a href='packing-services.html'>professional packers</a> can wrap an average house in a single day.",
             ]),
        ],
        'faqs': [
            ("How quickly can you do my house move?",
             "For local moves around Stoke-on-Trent and Newcastle-under-Lyme we can often accommodate 1–2 weeks' notice off-peak, or 4–6 weeks during the busy May-to-September season. <a href='../quote.html'>Get your free quote</a> and we'll confirm availability."),
            ("Do you provide moving boxes?",
             "Yes. Sturdy double-walled cartons, wardrobe boxes (loaned on the day), bubble wrap, tape and protective covers are all available for purchase. Or hire our packing crew and the materials come included."),
            ("Are you fully covered?",
             "Yes — full Goods in Transit insurance and £10 million Public Liability cover. Any claim is handled directly by our team, not a third-party broker."),
            ("What if my completion date slips?",
             "We never charge for postponements or key waits — we simply update the diary and re-book at no extra cost."),
            ("Do you move pianos and antiques?",
             "Yes — specialist <a href='piano-removals.html'>piano removal</a> service and bespoke crating for antique furniture. Mention these at survey so we can confirm crew size and kit."),
        ],
    },
    {
        'slug': 'services/commercial-removals.html',
        'title': 'Commercial Removals Stoke-on-Trent | Office Moves',
        'desc': "Commercial removals across Stoke-on-Trent, Newcastle and the Potteries. Out-of-hours office moves, IT decommission, crate hire, fixed price.",
        'h1': 'Commercial &amp; office removals across the Potteries',
        'eyebrow': 'Commercial moves · Out-of-hours',
        'lead': "From a five-person studio in Hanley to a fifty-desk floor in Stafford, our commercial removal crews plan and execute office relocations across the Potteries with minimal downtime. Out-of-hours and weekend lifts available so your team is up and running on Monday morning.",
        'hero_img': 'stacked-cardboard-boxes-empty-room.jpg',
        'sections': [
            ('Office moves done right', 'A planned, phased commercial relocation',
             [
                "Office relocations live and die on planning. Our project lead walks the existing and new floors with you, scopes IT decommission, packing crates, signage and disposal, and produces a written move plan with a fixed-price quote. Most North Staffordshire offices we move sit between 5 and 80 desks; larger projects are quoted on a phased basis.",
                "Out-of-hours and weekend lifts are standard. We've moved law firms, accounting practices, agencies and warehouses across Stoke, Newcastle-under-Lyme, Stafford and Burton-on-Trent — typically arriving Friday evening, unloading and rebuilding through Saturday, and handing back a fully kitted office on Monday morning. IT cabling, desks, monitors, server racks and storage cabinets all included.",
                "We hire out plastic crates (more secure than cardboard for fragile electronics and easier to label by department) and recycle every box at the end of the move. Document destruction can be arranged on request for sensitive paperwork.",
             ]),
            ('Whats included', 'Everything in one fixed commercial quote',
             [
                "Each commercial quote covers the survey, written move plan, crate hire and delivery in advance, packing where needed, the move itself, reassembly at the new office, and rubbish removal at both ends. Fixed price, in writing, valid for 60 days.",
                "We're <strong>fully covered</strong> for commercial moves — Goods in Transit, £10m Public Liability and Employer's Liability. Certificates available on request, normally needed by building management at the destination.",
             ]),
        ],
        'faqs': [
            ("Can you do the move at the weekend?",
             "Yes — most of our Staffordshire office moves happen Friday evening through Sunday so you're operational on Monday morning."),
            ("Do you decommission IT equipment?",
             "Yes — desk PCs, monitors, dock stations, phones and cabling. Servers and rack equipment by arrangement with your IT team."),
            ("Do you hire out plastic crates?",
             "Yes — delivered to your existing office a week in advance, collected a week after the move."),
            ("How far in advance should I book a commercial move?",
             "We recommend 6–8 weeks for a full office relocation. Smaller moves of 5–10 desks can usually be turned around in 2 weeks."),
            ("Are you covered for commercial liability?",
             "Yes — Public Liability of £10m and Employer's Liability cover. Certificates supplied on request."),
        ],
    },
    {
        'slug': 'services/packing-services.html',
        'title': 'Packing Services Stoke-on-Trent | NSR Removals',
        'desc': "Professional packing services across Stoke-on-Trent and Staffordshire. Full pack, fragile-only, or materials supply. Fixed-price quote.",
        'h1': 'Professional packing services in Stoke-on-Trent',
        'eyebrow': 'Packing services · Done right',
        'lead': "Packing properly is the single biggest factor in a damage-free move. Our professional packing crew can wrap and box an average three-bedroom Staffordshire house in a single day — or just handle the kitchen, china and artwork if you'd prefer to pack the rest yourself.",
        'hero_img': 'packing-kitchenware-cardboard-box.jpg',
        'sections': [
            ('Service tiers', "Three packing options that suit your move",
             [
                "<strong>Full pack &amp; unpack.</strong> Our crew arrives a day or two before the move with all materials and packs every room — wardrobes, drawers, kitchen, china, books, art, electronics — to a consistent, labelled standard. After the move we can return to unpack into your new property, breaking down and removing the cartons as we go.",
                "<strong>Fragile-only packing.</strong> Many customers prefer to pack their own books and clothes but want a professional to handle the kitchen, glassware, framed art and decorative pieces. We arrive the day before with materials and pack the items most at risk on the day, leaving the rest to you.",
                "<strong>Materials only.</strong> Sturdy double-walled cartons, wardrobe boxes (loaned free on the day), bubble wrap, kraft paper, tape and protective covers — all available from our Stoke-on-Trent depot, delivered to your door or collected.",
             ]),
            ('How we pack', "Our wrap-and-protect method",
             [
                "Every fragile item is wrapped in clean kraft paper or bubble, packed into double-walled cartons with paper or air-fill on top, and labelled by room. Glassware gets cell-divider inserts. Plates stand on edge, not stacked flat. TVs and electronics travel in their original boxes if you've kept them, or in dedicated TV cartons if not.",
                "Furniture is pad-wrapped in blankets <em>before</em> it leaves the room — sofas, beds, dining tables, wardrobes — and only unwrapped once it's in its final position at the new property. Mirrors, framed art and screens go in bespoke crates with corner protectors.",
                "Cardboard is recycled at the end of the move. We can either take everything away or leave folded cartons for you to use over the following weeks while you settle in.",
             ]),
        ],
        'faqs': [
            ("How long does a full pack take?",
             "About a day for an average 3-bedroom house. A larger 4–5 bed house may need a day and a half. We always pack the day before the move, never on the day itself."),
            ("Can I just have you pack the kitchen?",
             "Yes — fragile-only is one of our most popular options. We'll send a two-person team with materials for half a day."),
            ("Will you unpack into the new house?",
             "Yes, by arrangement. Most customers ask us to unpack kitchen and china into cupboards and break down the cartons; clothes and books they often prefer to do themselves."),
            ("Do you sell boxes if I want to pack myself?",
             "Yes — sturdy double-walled cartons, wardrobe boxes, bubble wrap and tape. Order in advance or collect from our Stoke depot."),
            ("How does damage cover work on packed items?",
             "Items packed by our crew are covered under Goods in Transit. Items packed by you are covered <em>except</em> for internal breakage of cartons we did not pack — standard industry practice."),
        ],
    },
    {
        'slug': 'services/storage-services.html',
        'title': 'Storage Solutions Stoke-on-Trent | NSR Removals',
        'desc': "Secure household and business storage in Stoke-on-Trent. Alarmed depot, palletised units, charged by the week, free Goods in Transit cover.",
        'h1': 'Secure storage solutions in Stoke-on-Trent',
        'eyebrow': 'Storage solutions · Alarmed depot',
        'lead': "Our alarmed Stoke-on-Trent depot holds your belongings in weather-sealed, individually palletised units — charged by the week, accessed by appointment. Whether your chain breaks down, you're between offices or you just need a few weeks of breathing space, we have a unit available.",
        'hero_img': 'cardboard-boxes-storage-warehouse.jpg',
        'sections': [
            ('How it works', "Palletised storage charged by the week",
             [
                "On collection day our crew loads your belongings directly into a palletised storage unit at our Stoke-on-Trent depot. Each unit is photographed, inventoried, weather-sealed and tagged with your name. The unit then sits inside our alarmed warehouse with 24-hour CCTV and intruder cover.",
                "There's no minimum term — you pay by the week and give a week's notice when you're ready to move out. We can also redeliver to anywhere in Staffordshire (or beyond) for a fixed redelivery fee agreed up front.",
                "Need to access your unit during storage? No problem — book a visit by appointment and we'll unwrap your unit and let you take what you need. Most customers find they don't need access, but the option is there.",
             ]),
            ('Storage tiers', "Storage for every Staffordshire scenario",
             [
                "<strong>House move chain delay.</strong> The most common reason customers use our storage — completion at your new property slips by a week or two. We collect on the original date, store the units, and redeliver when you're ready.",
                "<strong>Downsizing.</strong> Moving to a smaller place but not ready to part with everything? Long-term storage from 4 weeks upwards.",
                "<strong>Office between premises.</strong> Furniture, IT, archive boxes — stored in palletised units, redelivered to the new office on opening day.",
                "<strong>Probate &amp; estate clearance.</strong> Sensitive scenarios handled discreetly. We work with executors and solicitors across Staffordshire.",
             ]),
        ],
        'faqs': [
            ("How much does storage cost?",
             "Charged by the week, per palletised unit. Most 2–3 bedroom houses fit into 3–5 units. Exact cost confirmed at survey."),
            ("Is there a minimum storage term?",
             "No. Pay by the week, give a week's notice when you want to move out."),
            ("Can I access my unit while it's in storage?",
             "Yes — by appointment. We'll unwrap the unit and let you take what you need."),
            ("Is my stuff covered while in storage?",
             "Yes — Goods in Transit insurance applies on collection and redelivery; warehouse cover applies while stored."),
            ("Do you deliver out of stored units to a new address?",
             "Yes — to anywhere in Staffordshire or further afield. Redelivery cost agreed up front."),
        ],
    },
    {
        'slug': 'services/piano-removals.html',
        'title': 'Piano Removals Stoke-on-Trent | NSR Removals',
        'desc': "Specialist piano removals across Staffordshire. Upright, baby grand and concert grand experience. Fully covered, fixed price, careful crews.",
        'h1': 'Specialist piano removals across Staffordshire',
        'eyebrow': 'Piano removals · Specialist crews',
        'lead': "Upright, baby grand or full concert grand — our specialist piano crew has the kit and the experience to move it through any Staffordshire doorway. Skid boards, piano dollies, padded covers and a slow, careful approach are how we move pianos without damaging the instrument or your home.",
        'hero_img': 'man-stacking-cardboard-removal-boxes.jpg',
        'sections': [
            ('Specialist kit', "Why pianos need a specialist crew",
             [
                "A piano isn't just heavy — it's heavy in awkward places. An upright weighs 200–350kg; a baby grand 250–400kg; a concert grand can hit 550kg. Move it wrong and you risk the case, the action, the keys, the legs, your floor, your walls and the doorways at both ends. We've moved pianos in and out of Stoke terraces, Newcastle apartments, Leek farmhouses and Stafford rectories — every move is different.",
                "Our piano crew arrives with skid boards, piano dollies, padded covers, ratchet straps, four-wheel platforms and the patience to take an upright down a tight staircase without scuffing the wallpaper. We've worked with Steinway, Bösendorfer, Yamaha, Kawai and Bechstein instruments across the county.",
             ]),
            ('Booking & cover', "Booking your piano move",
             [
                "Mention the piano when you request your <a href='../quote.html'>free quote</a> — make/model, location in the property (upstairs/downstairs, basement, room access) and any stairs or tight turns. We'll send a crew leader to survey if needed, and confirm crew size (typically 3–4 people for grands) at the same time.",
                "Pianos travel under full Goods in Transit cover. We can also arrange a tuning visit at the new property a couple of weeks after the move (the instrument needs time to settle into its new climate first).",
             ]),
        ],
        'faqs': [
            ("Can you move a grand piano upstairs?",
             "Yes — we'll survey the access and confirm. Some grands have detachable legs that make staircases easier."),
            ("How much does it cost to move a piano?",
             "Depends on size, access and distance. Typically £150–£450 for a local upright; baby grands and concert grands more. Exact price after survey."),
            ("Is my piano covered during the move?",
             "Yes — full Goods in Transit cover. Restoration of any damage is handled directly by our team and our insurer."),
            ("Will the piano need tuning after the move?",
             "Yes — pianos always need a tune after a move, but we recommend waiting 2–3 weeks for the instrument to acclimatise to its new room."),
            ("Do you move pianos as part of a wider house move?",
             "Yes — pianos can be included in a residential removal at a small specialist supplement. Mention the piano at booking."),
        ],
    },
]

# Services hub
SERVICES_HUB = {
    'slug': 'services/index.html',
    'title': 'Removal &amp; Storage Services | NSR Stoke-on-Trent',
    'desc': "Removals, packing, storage and piano moves across Stoke-on-Trent and Staffordshire. Family-run since 2010. Fixed price. Free quote.",
    'h1': 'Removal &amp; storage services across Staffordshire',
    'eyebrow': 'Services · Staffordshire-wide',
    'lead': "From a single piano in Leek to a whole-office relocation in Stoke-on-Trent — and every house move in between. Choose your service below, or request a free fixed-price quote tailored to your move.",
    'hero_img': 'family-celebrating-keys-new-home.jpg',
}


def render_services():
    for s in SERVICES:
        sections_html = '\n'.join(
            block_prose(eyebrow=eb, h2=h2, paras=paras, alt_bg=(i % 2 == 0), orange_bg=(i % 3 == 2))
            for i, (eb, h2, paras) in enumerate(s['sections'])
        )
        sections_html += '\n' + block_why_cards(alt_bg=False)
        sections_html += '\n' + block_closing_prose(depth=1)
        sections_html += '\n' + block_accred()
        sections_html += '\n' + block_internal_links(COMMON_LINKS, alt_bg=True)
        render_page(
            slug=s['slug'],
            title=s['title'],
            desc=s['desc'],
            h1=s['h1'],
            eyebrow=s['eyebrow'],
            lead=s['lead'],
            hero_img=s['hero_img'],
            sections_html=sections_html,
            faqs=s['faqs'],
            depth=1,
            current='services',
        )

    # Services hub — link-grid of 5 service cards + intro + supplementary
    hub = SERVICES_HUB
    hub_extra = block_prose(
        eyebrow='How services work',
        h2='How our services come together for a smooth Staffordshire move',
        paras=[
            "Most Staffordshire customers book more than one of our services — a typical residential move combines the core <a href='domestic-removals.html'>residential removal</a> with either fragile-only or full <a href='packing-services.html'>packing</a>, and roughly a third of moves also use <a href='storage-services.html'>short-term storage</a> to bridge a completion gap. Commercial customers usually combine the <a href='commercial-removals.html'>office relocation</a> service with crate hire and IT decommissioning. Specialist <a href='piano-removals.html'>piano moves</a> can either run standalone or as an add-on to a wider residential booking.",
            "Bundling services together earns you a single fixed-price quote that covers the whole job. There's no per-service surcharge for combining: a residential move with full packing and two weeks of storage is quoted as one number, not three. That single-number approach is what lets us promise no surprises on the day, and it's why repeat customers tell us they value the experience as much as the price.",
            "If you're not sure which combination of services suits your move, the survey is the right place to figure it out. Our surveyors do this every day — they'll listen to what you're trying to achieve, look at the volume of contents and the access at both ends, and recommend the combination that delivers the smoothest day for the lowest total cost. If you'd rather get an indicative figure first, the <a href='../resources/storage-calculator.html'>moving calculator</a> lets you toggle services on and off and see how each one affects the price band.",
            "Every service we offer is delivered by our own employed team, with our own equipment, out of our own Stoke-on-Trent depot. We don't sub-contract any element of any service to third-party companies — what you see at quote stage is what you get on move day, every time.",
        ],
        alt_bg=False,
    )
    cards_html = '''    <section class="services-section">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">What we do</span>
          <h2>Five core services across Staffordshire</h2>
          <p>Pick the service that fits your move below, or <a href="../quote.html">request a tailored quote</a>.</p>
        </div>
        <div class="services-grid">
          <a class="svc-card" href="domestic-removals.html"><div class="svc-img"><img src="../images/couple-unpacking-boxes-new-home.jpg" alt="Couple unpacking removal boxes in their new home" width="1066" height="1600" loading="lazy"><span class="svc-icon" aria-hidden="true">🏠</span></div><div class="svc-body"><h3>Residential removals</h3><p>Full home moves across Staffordshire. Two- and four-man crews, modern lorries, fixed-price quote.</p><span class="arrow">Learn more</span></div></a>
          <a class="svc-card" href="commercial-removals.html"><div class="svc-img"><img src="../images/stacked-cardboard-boxes-empty-room.jpg" alt="Cardboard boxes ready for a Stoke-on-Trent office relocation" width="1600" height="1066" loading="lazy"><span class="svc-icon" aria-hidden="true">🏢</span></div><div class="svc-body"><h3>Commercial removals</h3><p>Out-of-hours office relocations across the Potteries — IT decommission, crate hire, planned floor-by-floor lifts.</p><span class="arrow">Learn more</span></div></a>
          <a class="svc-card" href="storage-services.html"><div class="svc-img"><img src="../images/cardboard-boxes-storage-warehouse.jpg" alt="Palletised storage containers in our Stoke-on-Trent warehouse" width="1200" height="800" loading="lazy"><span class="svc-icon" aria-hidden="true">🏬</span></div><div class="svc-body"><h3>Storage solutions</h3><p>Secure, alarmed container storage in Stoke-on-Trent. From a single pallet for a few weeks to long-term household storage.</p><span class="arrow">Learn more</span></div></a>
          <a class="svc-card" href="packing-services.html"><div class="svc-img"><img src="../images/packing-kitchenware-cardboard-box.jpg" alt="Professional packer wrapping kitchenware into a moving box" width="1600" height="1066" loading="lazy"><span class="svc-icon" aria-hidden="true">📦</span></div><div class="svc-body"><h3>Packing services</h3><p>Professional packers can wrap and box an average house in a single day, or just handle the fragile kitchen and china.</p><span class="arrow">Learn more</span></div></a>
        </div>
      </div>
    </section>'''
    intro_prose = block_prose(
        eyebrow='Our promise',
        h2='Five core services, one Staffordshire team',
        paras=[
            "North Staffordshire Removals &amp; Storage Ltd has been family-run from Stoke-on-Trent since 2010. Every service on this page is delivered by the same team — no sub-contractors, no last-minute van hire, no third-party brokers.",
            "Our crew know the Potteries roads, the parking quirks of every Newcastle-under-Lyme estate, the access points at the steeper Burslem terraces, and the lanes out to Leek and the Moorlands. That local knowledge is the reason your move runs to time and to the fixed-price quote we sent you.",
            "Below are our five core services. All are fully covered for Goods in Transit and Public Liability. All come with a free home or video survey and a written quote in 24 hours.",
        ],
        alt_bg=False,
    )
    piano_card = '''    <section class="alt-bg">
      <div class="container">
        <div class="section-head"><span class="eyebrow">Specialist</span><h2>Piano removals</h2><p>Upright, baby grand or full concert grand — see our specialist <a href="piano-removals.html">piano removals service</a> for kit, crew size and pricing.</p></div>
      </div>
    </section>'''
    sections_html = (intro_prose + '\n' + cards_html + '\n' + piano_card
                     + '\n' + hub_extra
                     + '\n' + block_why_cards(alt_bg=False)
                     + '\n' + block_closing_prose(depth=1)
                     + '\n' + block_accred()
                     + '\n' + block_internal_links(COMMON_LINKS, alt_bg=True))
    services_hub_faqs = [
        ("Which service should I choose for a typical house move?",
         "Most customers start with <a href='domestic-removals.html'>residential removals</a>. Add <a href='packing-services.html'>packing</a> if you'd rather hand the boxing-up to professionals; add <a href='storage-services.html'>storage</a> if your completion date is uncertain or you're downsizing."),
        ("Do you offer combined service quotes?",
         "Yes. Combining services (e.g. removal + packing + storage) is quoted as one fixed number — no per-service surcharge, no hidden bundling fee. Most quotes we send combine at least two services."),
        ("What's the most popular service combination?",
         "Residential removal + fragile-only packing is the most-booked combination, particularly for 3- and 4-bedroom Staffordshire moves where the kitchen and china benefit from professional handling."),
        ("Do you handle piano moves as part of a wider house move?",
         "Yes — pianos can be included in a residential booking at a small specialist supplement, or booked standalone via the <a href='piano-removals.html'>piano removals</a> service."),
        ("How do I get pricing for multiple services?",
         "<a href='../quote.html'>Submit one quote request</a> with all the services you might need. The surveyor will price each option and you can choose what to include in the final booking."),
    ]
    render_page(
        slug=hub['slug'], title=hub['title'], desc=hub['desc'],
        h1=hub['h1'], eyebrow=hub['eyebrow'], lead=hub['lead'],
        hero_img=hub['hero_img'], sections_html=sections_html, depth=1,
        current='services', faqs=services_hub_faqs,
    )


if __name__ == '__main__':
    print('Rendering services...')
    render_services()
    print('Done.')
