#!/usr/bin/env python3
"""Render resources/storage-calculator.html — full MRM-clone calculator wrapped
in NSR branding. Pulls the rebranded widget HTML from resources/_calc-widget.html
and inventory data from resources/_bed-inventory.html."""
from __future__ import annotations
import os, sys, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("rp", os.path.join(ROOT, 'tools', 'render-pages.py'))
rp = importlib.util.module_from_spec(spec); spec.loader.exec_module(rp)
os.chdir(ROOT)


def how_it_works_block():
    paras = [
        "The calculator gives an indicative price band in seconds. Pick what you're moving, the home size, the round-trip distance and storage days — the figure updates live as you type, and the room-by-room inventory lets you refine to the exact cubic-foot total when you want a sharper number.",
        "Our 2026 pricing reflects fifteen years of running residential and commercial moves across Staffordshire. The fee covers labour, vehicle, fuel, full Goods in Transit cover, £10 million Public Liability, parking permits where needed, blankets and wardrobe boxes on the day, and removal of empty cartons at the end. We don't bill by the hour and we don't add fuel surcharges on the day.",
        "<strong>Volumes</strong> are estimates based on average UK household contents at each property size. A sparsely furnished 3-bed costs less than a content-dense 3-bed. The free survey resolves that.",
        "<strong>Distance</strong> uses simple round-trip mileage — depot → your old home → new home → depot. Long-distance moves are quoted on a fixed-price basis per move, not per mile.",
        "<strong>Storage</strong> is charged by the day per palletised unit. Nett rates shown; VAT added at booking. <a href='../services/storage-services.html'>Storage detail</a>.",
    ]
    return rp.block_prose(eyebrow='How the calculator works', h2='How the calculator works', paras=paras, alt_bg=True)


def follow_up_block():
    paras = [
        "<strong>Want a fixed-price written quote?</strong> The calculator's estimate becomes a binding written number after a free home or video survey. Most customers find the written quote lands within 5-10% of the calculator's mid-band.",
        "<strong>Want to talk it through first?</strong> The office line is <a href='tel:+441782939124'><strong>01782 939124</strong></a> Monday to Friday 8am to 6pm, Saturday 9am to 2pm.",
        "<strong>Not sure which service you need?</strong> See <a href='../services/'>all services</a> for a breakdown of residential, commercial, packing, storage and piano-removal options.",
        "<strong>How the calculator was built.</strong> The price bands reflect our actual 2026 rates across hundreds of completed Staffordshire moves. The volume figures per property size are based on an average loaded over the year; the storage estimate uses an average palletised-unit rate.",
        "<strong>What it doesn't capture.</strong> Access factors at both ends (top-floor flats, narrow village lanes, long carries), specialist items (pianos, antiques, fine art) and out-of-hours commercial requirements are not modelled in the calculator. The free survey captures all of these.",
        "<strong>Why we publish a calculator at all.</strong> Most removers don't. We've taken the opposite view — being upfront about realistic price bands respects your time, helps you budget, and reduces the chance of an unpleasant surprise after the survey.",
    ]
    return rp.block_prose(eyebrow='Next step', h2='Convert the estimate into a fixed-price quote', paras=paras)


CALC_FAQS = [
    ("How accurate is the calculator?",
     "Most written quotes land within 5-10% of the calculator's mid-band figure. The calculator uses average volumes per property size; the survey confirms the actual volume and access factors."),
    ("What's included in the calculator's price?",
     "Labour, vehicle, fuel, Goods in Transit cover, Public Liability and parking permits where needed. Same as every NSR quote."),
    ("Why is my actual quote different from the calculator?",
     "Actual content volume (sparser vs denser homes) and access factors (top-floor flats, narrow streets, tight stairs). The free survey reconciles both."),
    ("Can I trust the storage figures?",
     "The storage estimate uses live per-unit nett day rates. Most 2-3 bed houses fit into 3-5 units. Exact storage pricing is confirmed at survey."),
    ("How long does the indicative price hold?",
     "The calculator reflects current 2026 pricing and is updated whenever rates change. The written fixed-price quote following a survey is valid 60 days."),
    ("Can I use the calculator for office or commercial moves?",
     "Yes — the office options give an indicative figure. Commercial moves are usually phased and benefit from a proper site visit; the calculator is a planning tool, the survey is the binding quote."),
]


def calc_widget_html():
    """Pull rebranded widget HTML from the extract file."""
    p = os.path.join(ROOT, 'tools', 'calc-extracts', 'widget.html')
    return open(p, encoding='utf-8').read()


def bed_inventory_script():
    """Pull BED_INVENTORY <script> tag from the extract."""
    p = os.path.join(ROOT, 'tools', 'calc-extracts', 'bed-inventory.html')
    return open(p, encoding='utf-8').read()


def plain_hero():
    """MRM-style plain-background hero for the calculator page —
    H1 + eyebrow + lead + 2 CTAs on the left, hero image on the right.
    No dark gradient banner — matches MRM exactly."""
    return '''    <section style="background:#fff;padding:clamp(2rem,4vw,3.25rem) 0;">
      <div class="container">
        <div class="split">
          <div class="split-content">
            <span class="eyebrow">Free tool · Staffordshire removers since 2010</span>
            <h1>Removals Cost &amp; Volume Calculator</h1>
            <p class="lead" style="font-size:clamp(1.05rem,1.5vw,1.2rem);color:var(--ink-soft);max-width:60ch;">Tick the items in your home, set the move distance and the calculator returns cubic feet, vehicle size, weight and an itemised cost estimate &mdash; the same numbers our crews use to plan a Staffordshire job.</p>
            <div class="hero-actions" style="margin-top:1.25rem">
              <a class="btn" href="../quote.html">Get a free quote</a>
              <a class="btn btn-ghost" href="tel:+441782939124">Call 01782 939124</a>
            </div>
          </div>
          <div class="split-img">
            <img src="../images/loading-cardboard-removal-boxes.jpg" alt="North Staffordshire Removals crew loading a Stoke-on-Trent move" width="1066" height="1600" fetchpriority="high">
          </div>
        </div>
      </div>
    </section>'''


def render():
    sections = ('' + calc_widget_html()
                + '\n' + how_it_works_block()
                + '\n' + follow_up_block()
                + '\n' + rp.block_why_cards(alt_bg=True)
                + '\n' + rp.block_accred()
                + '\n' + rp.faq_section(CALC_FAQS)
                + '\n' + rp.block_internal_links(rp.COMMON_LINKS, alt_bg=True))

    canonical = f'{rp.BASE}/resources/storage-calculator.html'
    extra = rp.webpage_jsonld(url=canonical,
                               title='Moving &amp; Storage Calculator | NSR',
                               desc='Estimate your removals and storage cost in seconds. Indicative 2026 pricing for Staffordshire moves.')
    extra += rp.faq_jsonld(CALC_FAQS)
    # WebApplication schema (mirrors MRM's calculator page schema)
    extra += '''
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"WebApplication","name":"North Staffordshire Removals Storage Calculator","applicationCategory":"UtilityApplication","operatingSystem":"All","description":"Free volume and weight calculator for Staffordshire removals and storage.","url":"''' + canonical + '''","publisher":{"@type":"Organization","@id":"''' + rp.BASE + '''/#organization"},"offers":{"@type":"Offer","price":"0","priceCurrency":"GBP"}}</script>'''

    parts = [
        rp.head(title='Moving &amp; Storage Calculator | NSR Removals',
                desc="Estimate your removals and storage cost in seconds. Indicative 2026 pricing for Staffordshire homes and offices.",
                canonical=canonical, og_image='family-celebrating-keys-new-home.jpg',
                preload_img='family-celebrating-keys-new-home.jpg', depth=1, extra_schema=extra),
    ]
    # Inject calculator.css link
    parts[0] = parts[0].replace('</head>',
        '  <link rel="stylesheet" href="../css/calculator.css?v=' + rp.CSS_V + '">\n</head>')
    parts += [
        '<body>',
        '  <a class="skip-link" href="#main">Skip to main content</a>',
        rp.topbar(1),
        rp.nav('calc', 1),
        '  <main id="main">',
        plain_hero(),
        sections,
        rp.related_blogs('resources-storage-calculator', 1),
        rp.cta_strip(1),
        '  </main>',
        rp.footer(1).replace('mobile-nav.js?v=' + rp.CSS_V + '"></script>',
                              'mobile-nav.js?v=' + rp.CSS_V + '"></script>\n  ' +
                              bed_inventory_script() + '\n  ' +
                              '<script defer src="../js/storage-calculator.js?v=' + rp.CSS_V + '"></script>'),
    ]
    open('resources/storage-calculator.html', 'w', encoding='utf-8').write('\n'.join(parts) + '\n')
    print('  wrote resources/storage-calculator.html')


if __name__ == '__main__':
    render()
