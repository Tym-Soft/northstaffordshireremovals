#!/usr/bin/env python3
"""Render the utility pages: about, reviews, careers, quote, 404, privacy, terms."""

from __future__ import annotations
import os, sys, importlib.util, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("rp", os.path.join(ROOT, 'tools', 'render-pages.py'))
rp = importlib.util.module_from_spec(spec); spec.loader.exec_module(rp)
os.chdir(ROOT)

# Root-level utility pages use depth=0
def root_internal_links():
    return [
        ('Get a free quote',                'quote.html'),
        ('All services',                    'services/'),
        ('Residential removals',            'services/domestic-removals.html'),
        ('Commercial removals',             'services/commercial-removals.html'),
        ('Packing services',                'services/packing-services.html'),
        ('Storage solutions',               'services/storage-services.html'),
        ('Piano removals',                  'services/piano-removals.html'),
        ('All areas covered',               'areas-covered/'),
        ('Removals in Stoke-on-Trent',      'areas-covered/removals-stoke-on-trent.html'),
        ('Removals in Newcastle-under-Lyme','areas-covered/removals-newcastle-under-lyme.html'),
        ('Removals in Stafford',            'areas-covered/removals-stafford.html'),
        ('Removals in Leek',                'areas-covered/removals-leek.html'),
        ('Moving Calculator',               'resources/storage-calculator.html'),
        ('Advice & moving tips',            'blog/'),
        ('About us',                        'about-us.html'),
        ('Customer reviews',                'reviews.html'),
    ]


def render_root_page(*, slug, title, desc, h1, eyebrow, lead, sections_html,
                     faqs=None, hero_img='family-celebrating-keys-new-home.jpg', current=''):
    """Like render_page but depth=0 (root-level pages).
    Always renders the visible FAQ section AND injects FAQPage JSON-LD."""
    canonical = f'{rp.BASE}/{slug}'
    extra = rp.webpage_jsonld(url=canonical, title=title, desc=desc) + rp.faq_jsonld(faqs or [])
    parts = [
        rp.head(title=title, desc=desc, canonical=canonical, og_image=hero_img,
                preload_img=hero_img, depth=0, extra_schema=extra),
        '<body>',
        '  <a class="skip-link" href="#main">Skip to main content</a>',
        rp.topbar(0),
        rp.nav(current, 0),
        '  <main id="main">',
        root_hero(eyebrow=eyebrow, h1=h1, lead=lead, hero_img=hero_img),
        sections_html,
        rp.faq_section(faqs or []) if faqs else '',
        rp.related_blogs(rp._auto_related_key(slug), 0),
        rp.cta_strip(0),
        '  </main>',
        rp.footer(0),
    ]
    os.makedirs(os.path.dirname(slug) or '.', exist_ok=True)
    open(slug, 'w', encoding='utf-8').write('\n'.join(parts) + '\n')
    print(f'  wrote {slug}')


def root_hero(*, eyebrow, h1, lead, hero_img):
    return f'''    <section class="hero" style="background:linear-gradient(115deg, rgba(10,34,62,.92) 0%, rgba(17,54,90,.78) 50%, rgba(10,34,62,.55) 100%), url('images/{hero_img}') center/cover no-repeat;">
      <div class="container">
        <div class="hero-inner">
          <span class="eyebrow">{eyebrow}</span>
          <h1>{h1}</h1>
          <p class="lead">{lead}</p>
          <div class="hero-actions">
            <a class="btn" href="quote.html">Get a free quote</a>
            <a class="btn btn-outline" href="tel:+441782939124">Call 01782 939124</a>
          </div>
          <div class="hero-trust">
            <span><span class="tick">✓</span> Family-run since 2010</span>
            <span><span class="tick">✓</span> Fully covered</span>
            <span><span class="tick">✓</span> Fixed prices</span>
            <span><span class="tick">✓</span> 187 verified reviews</span>
          </div>
        </div>
{rp.hero_quote_form(depth=0)}
      </div>
    </section>'''


def block_prose_root(*, eyebrow, h2, paras, alt_bg=False, orange_bg=False):
    cls = 'services-section' if orange_bg else ('alt-bg' if alt_bg else '')
    paras_html = ''.join(f'<p style="max-width:none">{p}</p>' for p in paras)
    return f'''    <section class="{cls}">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">{eyebrow}</span>
          <h2>{h2}</h2>
        </div>
        <div class="prose-wide">{paras_html}</div>
      </div>
    </section>'''


# Root-level helpers that wrap rp.block_why_cards / rp.block_accred for depth=0 pages
def block_why_cards_root(eyebrow='Why choose us', h2='Eight reasons Staffordshire chooses us first', alt_bg=False):
    return rp.block_why_cards(eyebrow=eyebrow, h2=h2, alt_bg=alt_bg)
def block_accred_root():
    return rp.block_accred()


def block_internal_links_root(links, alt_bg=False):
    cls = 'alt-bg' if alt_bg else ''
    items = ''.join(f'<li><a href="{h}">{html.escape(l)}</a></li>' for l, h in links)
    return f'''    <section class="{cls}">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Continue browsing</span>
          <h2>More from North Staffordshire Removals</h2>
        </div>
        <ul style="columns:2;column-gap:2rem;list-style:none;padding:0;max-width:none;font-weight:600">{items}</ul>
      </div>
    </section>'''


# ─── About ──────────────────────────────────────────────────────
def about_page():
    sections = ''.join([
        block_prose_root(
            eyebrow='Founded 2010',
            h2='A family-run Staffordshire removals company, since 2010',
            paras=[
                "North Staffordshire Removals &amp; Storage Ltd was founded in 2010 with one Luton van and a simple promise — to treat every customer's belongings as if they were our own. Fifteen years later we run a fleet of modern Luton and 7.5-tonne lorries out of our depot at the Genesis Centre in Stoke-on-Trent, with the same family hands at the helm.",
                "The reason customers keep coming back isn't price or marketing — it's that we do what we say. The fixed-price quote really is fixed. The crew really is uniformed, trained and professional. If your completion slips by a day or three, we really don't charge a penny. And if anything ever isn't right, the office phone really does answer.",
                "Nearly seven in ten of our jobs each year come from repeat customers or personal recommendations from previous customers — not from paid advertising. That's the kind of business we wanted to build, and it's the kind of business we'll keep on building.",
            ]),
        block_prose_root(
            eyebrow='What we cover',
            h2="What we do, and where we do it",
            paras=[
                "Our core service is residential <a href='services/domestic-removals.html'>house removals</a> across Staffordshire. We also offer <a href='services/commercial-removals.html'>office and commercial relocations</a>, <a href='services/packing-services.html'>professional packing</a>, <a href='services/storage-services.html'>palletised storage</a> at our Stoke depot, and specialist <a href='services/piano-removals.html'>piano removals</a> for upright, baby grand and concert grand instruments.",
                "Geographically we cover the whole of North Staffordshire and the wider county — the six towns of <a href='areas-covered/removals-stoke-on-trent.html'>Stoke-on-Trent</a>, <a href='areas-covered/removals-newcastle-under-lyme.html'>Newcastle-under-Lyme</a>, <a href='areas-covered/removals-stafford.html'>Stafford</a>, <a href='areas-covered/removals-stone.html'>Stone</a>, <a href='areas-covered/removals-leek.html'>Leek</a> and the Moorlands, <a href='areas-covered/removals-eccleshall.html'>Eccleshall</a>, <a href='areas-covered/removals-burton-on-trent.html'>Burton-on-Trent</a> and over the border to <a href='areas-covered/removals-buxton.html'>Buxton</a> and the High Peak. We also handle long-distance moves to and from anywhere in the UK.",
                "Every move we undertake is fully covered for Goods in Transit and £10 million Public Liability. Claims (rare as they are) are handled directly by our office team — never a third-party broker.",
            ],
            alt_bg=True),
        block_prose_root(
            eyebrow='Our standards',
            h2='How we run a move, from first call to final box',
            paras=[
                "<strong>The free survey.</strong> Either at your home (typically 30 minutes) or via a video walk-through — your choice. We measure volume, check access, photograph the route the lorry will take, and ask about any tricky items.",
                "<strong>The written quote.</strong> Within 24 hours of the survey you receive a written, itemised, fixed-price quote valid for 60 days. Labour, vehicle, fuel, insurance, parking permits where needed — all included.",
                "<strong>The 'what next' pack.</strong> A small deposit confirms your move date. We send you a pack covering boxes, parking arrangements, key handover, and the day-of timetable.",
                "<strong>The move day.</strong> Crew arrives in branded uniform with blankets, straps, floor runners, wardrobe boxes and the rest of the kit. We pad-wrap every piece of furniture <em>before</em> it leaves the room. We load systematically. We drive carefully. We unwrap only when each item is in its final position at the new property.",
                "<strong>The settle-in.</strong> Once we've gone you can still ring the office. Furniture rearrangement, box collection, or a question about how we packed the kitchen — we're a call away.",
            ]),
        block_prose_root(
            eyebrow='Trust signals',
            h2='Cover, accreditations, and who we work with',
            paras=[
                "<strong>Cover:</strong> Goods in Transit insurance (£50,000 per consignment as standard, higher available by arrangement) plus £10 million Public Liability and Employer's Liability. All certificates available on request — typically needed by building management at commercial destinations.",
                "<strong>Data protection:</strong> Our office processes customer details under UK GDPR and the Data Protection Act 2018. We don't share your data with third parties beyond the move logistics. See our <a href='privacy-policy.html'>privacy policy</a>.",
                "<strong>Reviews:</strong> We're rated 4.9 out of 5 from 187 independently verified customer reviews. Read the full set on our <a href='reviews.html'>reviews page</a>.",
                "<strong>Recommendations:</strong> Several Staffordshire estate agents and conveyancers recommend us to their vendors and buyers. We treat that trust seriously and we don't pay for it.",
            ],
            alt_bg=True),
        block_prose_root(
            eyebrow='Office',
            h2='Visit, call, or book online',
            paras=[
                "Our office is at <strong>Suite F24, Genesis Centre, Innovation Way, Stoke-on-Trent, ST6 4BF</strong>. Open Monday to Friday 8am to 6pm and Saturday 9am to 2pm. Closed Sundays and bank holidays.",
                "Telephone: <a href='tel:+441782939124'><strong>01782 939124</strong></a>. Email: <a href='mailto:enquiries@northstaffordshireremovals.co.uk'>enquiries@northstaffordshireremovals.co.uk</a>.",
                "The fastest way to get a fixed-price quote is to <a href='quote.html'>complete the online quote form</a> — most customers get a written quote within 24 hours.",
            ]),
        block_why_cards_root(alt_bg=False),
        rp.block_closing_prose(depth=0),
        block_accred_root(),
        block_internal_links_root(root_internal_links(), alt_bg=True),
    ])
    about_faqs = [
        ("How long has North Staffordshire Removals been trading?",
         "Since 2010 — over fifteen years of continuous trading from our Stoke-on-Trent depot. We're family-run and have operated under the same name and ownership since day one."),
        ("Are you a franchise or part of a larger group?",
         "No. We're independently owned and family-run, not part of any franchise or chain. Every quote you receive and every crew that turns up to your move is directly employed by us."),
        ("Where is your office and depot?",
         "Suite F24, Genesis Centre, Innovation Way, Stoke-on-Trent, ST6 4BF. Office open Monday-Friday 8am-6pm and Saturday 9am-2pm. We welcome visits by appointment."),
        ("Can I meet the crew before booking?",
         "The surveyor who quotes your move is part of the team that runs it. For larger or more complex moves we're happy to arrange a depot visit so you can meet the crew leader who'll be on your job. Just ask at survey."),
        ("How do I get in touch?",
         "Call <a href='tel:+441782939124'>01782 939124</a> Monday-Friday 8am-6pm or Saturday 9am-2pm; email <a href='mailto:enquiries@northstaffordshireremovals.co.uk'>enquiries@northstaffordshireremovals.co.uk</a>; or use the <a href='quote.html'>online quote form</a> for the fastest written quote."),
    ]
    render_root_page(
        slug='about-us.html',
        title='About Us | North Staffordshire Removals &amp; Storage',
        desc="About North Staffordshire Removals — family-run Staffordshire removals since 2010. Our story, our crew, our depot in Stoke-on-Trent.",
        h1='About North Staffordshire Removals &amp; Storage Ltd',
        eyebrow='About · Family-run since 2010',
        lead='The story behind Staffordshire&rsquo;s family-run home and business removals and storage company. Founded 2010, based in Stoke-on-Trent, run by people who live in the towns we move you into.',
        sections_html=sections,
        faqs=about_faqs,
        current='about',
    )


# ─── Reviews ────────────────────────────────────────────────────
def reviews_page():
    quotes = [
        ("Rachel Hatchard", "Stoke-on-Trent · 3-bed move", "smiling-woman-with-dog-moving-day.jpg",
         "Absolutely brilliant from start to finish. Really professional, polite and efficient. Would definitely use again. Thank you so much for making my move so easy."),
        ("Matt &amp; Jen", "Newcastle &rarr; Leek · 4-bed move", "couple-new-home-cardboard-box.jpg",
         "Our completion got pushed back twice and they didn't charge us a thing. The crew were brilliant on the day &mdash; couldn't have asked for a smoother move."),
        ("David R.", "Burslem &middot; piano + 2-bed", "man-yellow-tshirt-with-moving-box.jpg",
         "Polite, careful and fast. They handled my grandmother's piano like it was made of glass. Highly recommend."),
        ("Sarah B.", "Stafford &middot; downsizing", "woman-folding-clothes-suitcase-packing.jpg",
         "Helped me downsize from a four-bed to a two-bed flat &mdash; including arranging storage for the items I wasn't sure about. Everything was handled with care."),
        ("Mike P.", "Office move &middot; Hanley", "stacked-cardboard-boxes-empty-room.jpg",
         "Out-of-hours office relocation done over a weekend. Up and running Monday morning, zero downtime. Worth every penny."),
        ("Helen W.", "Leek &middot; farmhouse move", "couple-unpacking-boxes-new-home.jpg",
         "Crew arrived early, packed our entire farmhouse in one day, delivered everything spotlessly to our new place. Professional throughout."),
        ("James &amp; Anna", "Newcastle &middot; 2-bed", "estate-agent-handing-house-keys.jpg",
         "First-time buyers, first-time movers. NSR walked us through everything, no question was too daft. Massive thanks."),
        ("Tom F.", "Buxton &middot; 3-bed", "holding-house-keys-new-home.jpg",
         "Snow forecast for our completion day. They moved us a day early at no extra cost. Stoke to Buxton without a scratch."),
        ("Linda C.", "Stone &middot; antique move", "loading-cardboard-removal-boxes.jpg",
         "Several pieces of antique furniture. Handled with bespoke crates and obvious experience. Trust them completely."),
    ]
    cards = []
    for name, place, img, q in quotes:
        cards.append(f'''<article class="testimonial"><div class="stars" aria-label="Five out of five stars">★★★★★</div><p>"{q}"</p><div class="testimonial-author"><img src="images/{img}" alt="Portrait of customer {name}" width="800" height="800" loading="lazy"><div><div class="who">{name}</div><div class="where">{place}</div></div></div></article>''')
    grid = '<section class="alt-bg"><div class="container"><div class="testimonials">' + ''.join(cards) + '</div></div></section>'

    intro = block_prose_root(
        eyebrow='Customer reviews',
        h2='Rated 4.9 out of 5 from 187 verified reviews',
        paras=[
            "Our reviews come from real Staffordshire customers we've moved over the years. We don't filter the negative ones (the rare times something hasn't gone perfectly), and we don't pay for reviews. We simply ask every customer to share their experience &mdash; positive or otherwise &mdash; once their move is complete.",
            "Below is a selection of recent reviews from customers across Stoke-on-Trent, Newcastle-under-Lyme, Leek, Stafford and the wider Staffordshire patch. If you've been moved by us and would like to share your experience, we'd love to hear it &mdash; just reply to the email we sent after your move, or call the office on <a href='tel:+441782939124'>01782 939124</a>.",
        ])
    cta = block_prose_root(
        eyebrow='Ready to move?',
        h2='Book your fixed-price quote in 24 hours',
        paras=[
            "Most customers receive a fixed-price quote within 24 hours of submitting the <a href='quote.html'>online quote form</a> or calling the office on <a href='tel:+441782939124'>01782 939124</a>. We can survey by video or in person, whichever you prefer.",
        ], alt_bg=True)
    sections = intro + grid + cta + block_why_cards_root(alt_bg=False) + rp.block_closing_prose(depth=0) + block_accred_root() + block_internal_links_root(root_internal_links(), alt_bg=True)
    reviews_faqs = [
        ("Are these reviews real?",
         "Yes — every review is from a real Staffordshire customer we've moved. We ask all customers to leave a review after their move; we don't filter the rare critical ones, and we don't pay for any of them."),
        ("Where are the reviews hosted?",
         "We collect feedback by email after the move; verified reviews are also published on Google and other independent platforms. The 4.9-out-of-5 rating reflects the cross-platform average."),
        ("Can I leave a review after my move?",
         "Yes — we'll email a feedback link a few days after your move completes. You can also email <a href='mailto:enquiries@northstaffordshireremovals.co.uk?subject=Review'>the office</a> directly with your feedback."),
        ("Do you respond to negative reviews?",
         "Yes, always. We acknowledge any negative review publicly and reach out privately to resolve the underlying issue. We treat negative feedback as the most valuable input we receive."),
        ("How can I trust the rating is accurate?",
         "Cross-check us on Google Reviews and other independent platforms. The pattern of feedback (consistent rather than mixed) is the strongest signal — we ask every customer, so the sample is broad."),
    ]
    render_root_page(
        slug='reviews.html',
        title='Customer Reviews 4.9/5 | NSR Removals &amp; Storage',
        desc="Read 187 verified reviews from Staffordshire customers we've moved. Rated 4.9 out of 5. Family-run from Stoke-on-Trent since 2010.",
        h1='What Staffordshire customers say about North Staffordshire Removals',
        eyebrow='Reviews · 4.9 / 5',
        lead="Rated 4.9 out of 5 from 187 independently verified customer reviews. Below is a selection of recent feedback from house and office moves across Stoke-on-Trent, Newcastle-under-Lyme, Leek, Stafford and the wider Staffordshire patch.",
        sections_html=sections,
        faqs=reviews_faqs,
        current='reviews',
    )


# ─── Careers ────────────────────────────────────────────────────
def careers_extra_block():
    return block_prose_root(
        eyebrow='Benefits & training',
        h2='Benefits, training and culture',
        paras=[
            "<strong>Pay &amp; benefits.</strong> Above-industry-standard hourly rates for the right experience, full PAYE, statutory pension auto-enrolment, 28 days paid holiday per year (including bank holidays) for full-time roles, branded uniform and PPE supplied. Tips earned on the day stay with the crew that earned them.",
            "<strong>Training.</strong> Every new starter spends their first two weeks shadowing experienced crews before leading any move element themselves. We run quarterly internal training sessions covering pad-wrap technique, piano-handling refresher, customer-service standards, and loading/stack-safe procedures. Drivers have annual CPC refresher days paid for by the company.",
            "<strong>Career progression.</strong> Most of our team-leaders started as removal crew members. We promote from within wherever the role and aptitude line up — typical progression is Removal Crew → Lead Crew → Driver → Crew Leader → Office &amp; Operations. We're genuinely interested in long-term careers, not seasonal staffing.",
            "<strong>Culture.</strong> Small family-run team with everyone knowing each other by name. Office team and crews work in the same depot, eat lunch together, and share the same WhatsApp group for day-of coordination. We don't tolerate rudeness to customers or to each other — that's a hard line.",
            "<strong>A typical day for a Removal Crew member.</strong> Arrive at the depot 7:30am, brief with the team leader on the day's job, drive to the first customer (often 8:00am start onsite), set up floor runners and protective covers, pad-wrap furniture in each room, load systematically, drive to the new property, unload, place items where the customer wants them, reassemble beds and wardrobes, walk the inventory with the customer, return to depot to clean down and refuel the lorry. Most days finish 5:00–6:00pm.",
            "<strong>What we look for.</strong> Reliability, physical fitness, customer-facing manner, ability to follow a system, willingness to learn. Previous removal experience is preferred but not essential — we've trained good people from scratch. Cat C HGV licence is preferred for crew progression but again not essential at entry level.",
            "<strong>How to apply.</strong> Email a CV and a short note about which role interests you to <a href='mailto:enquiries@northstaffordshireremovals.co.uk?subject=Job%20application'>enquiries@northstaffordshireremovals.co.uk</a>, or call the office on <a href='tel:+441782939124'>01782 939124</a> and ask to speak to the operations manager. We respond to every application within seven days, and we'll always tell you whether we have an opening that fits.",
        ],
        alt_bg=True,
    )

def careers_page():
    sections = ''.join([
        careers_extra_block(),
        block_prose_root(
            eyebrow='Join the team',
            h2='Careers at North Staffordshire Removals &amp; Storage Ltd',
            paras=[
                "We're a small family-run removals and storage company in Stoke-on-Trent, growing steadily and always interested in hearing from experienced movers, packers and drivers who'd like to work somewhere that values doing the job properly. We don't sub-contract, so when you join our team you become part of the regular crew that customers rate 4.9 out of 5.",
                "All our roles are PAYE with the standard benefits — pension, holiday pay, training, branded uniform and equipment supplied. We don't use casual day labour for our regular work.",
            ]),
        block_prose_root(
            eyebrow='Current openings',
            h2='Roles we are recruiting for',
            paras=[
                "<strong>Removal Crew Member.</strong> Full-time, experienced. Loading, packing, driving (Cat C licence preferred), customer-facing. Branded uniform supplied. Pay above industry standard for the right experience.",
                "<strong>Lead Packer.</strong> Full-time, experienced. Leading the packing crew on full-pack jobs, kit management, training new starters. Two years' professional packing experience required.",
                "<strong>HGV Driver (7.5t and 18t).</strong> Full or part-time. Valid licence, current digital tachograph card, CPC. Local Staffordshire work plus occasional long-distance routes.",
                "<strong>Office &amp; Operations Coordinator.</strong> Part-time. Diary management, customer enquiries, quote follow-up. Based at our Stoke depot. Friendly, organised, customer-focused.",
            ], alt_bg=True),
        block_prose_root(
            eyebrow='How to apply',
            h2='Apply or register your interest',
            paras=[
                "Email a CV and a short note about which role interests you to <a href='mailto:enquiries@northstaffordshireremovals.co.uk'>enquiries@northstaffordshireremovals.co.uk</a>, or call the office on <a href='tel:+441782939124'>01782 939124</a>. We respond to every application within a week.",
                "If we don't have an opening for your role today but you'd like to register your interest for future openings, we'd be glad to keep your details on file under our standard <a href='privacy-policy.html'>privacy policy</a>.",
            ]),
        block_why_cards_root(alt_bg=False),
        rp.block_closing_prose(depth=0),
        block_accred_root(),
        block_internal_links_root(root_internal_links(), alt_bg=True),
    ])
    careers_faqs = [
        ("Do I need previous removals experience?",
         "For crew roles, experience is preferred but not essential — we've trained good people from scratch and our two-week shadowing programme means you won't be lead on any move until you're ready. Lead Packer and HGV Driver roles do need relevant experience."),
        ("Do I need an HGV licence?",
         "Cat C (7.5-tonne) licence is preferred for crew progression and required for Driver roles. We can support paying for licence upgrades for the right candidate once you've shown commitment to the team."),
        ("What does a typical day look like?",
         "7:30am depot brief; 8am onsite at the first customer; load systematically; drive to the new property; unload and reassemble; return to depot to clean down. Most days finish 5-6pm. We try to keep crews paired consistently so you work with familiar colleagues."),
        ("Is this a permanent role?",
         "All our roles are permanent PAYE positions with statutory benefits. We don't use casual day labour or zero-hours contracts for the regular team."),
        ("How quickly will you respond to my application?",
         "Within seven days. Send your CV and a short note to <a href='mailto:enquiries@northstaffordshireremovals.co.uk?subject=Job%20application'>enquiries@northstaffordshireremovals.co.uk</a> or call <a href='tel:+441782939124'>01782 939124</a> and ask for the operations manager."),
    ]
    render_root_page(
        slug='careers.html',
        title='Careers at NSR Removals &amp; Storage | Stoke-on-Trent',
        desc="Careers at North Staffordshire Removals &amp; Storage. Hiring crew, packers, drivers and office staff at our Stoke-on-Trent depot.",
        h1='Careers at North Staffordshire Removals',
        eyebrow='Careers · Family-run team',
        lead="Join the team that customers rate 4.9 out of 5. Current openings for removal crew, lead packers, HGV drivers and office staff at our Stoke-on-Trent depot.",
        sections_html=sections,
        faqs=careers_faqs,
    )


# ─── Quote (form page) ──────────────────────────────────────────
def quote_page():
    # The full quote form lives in the hero (via root_hero +
    # rp.hero_quote_form). The standalone "Tell us about your move"
    # section that previously sat below the hero was a duplicate of
    # the same form — removed to avoid two identical forms on the
    # same page. Customers land in the hero form first.
    why = block_prose_root(
        eyebrow="What happens next",
        h2='What happens after you submit',
        paras=[
            "1. We confirm receipt by email within an hour during office hours.",
            "2. A surveyor calls or emails to book a free home visit or video walk-through — typically 30 minutes.",
            "3. Within 24 hours of the survey you receive a written, itemised, fixed-price quote valid 60 days.",
            "4. If you'd like to proceed, a small deposit confirms your move date. If not, no obligation — we'll keep your details for 12 months in case you'd like to come back to us later.",
            "<strong>What the survey covers.</strong> Whether at your home or by video walk-through, the survey takes about 30 minutes. The surveyor will: walk through every room and note the volume of contents (in cubic feet); check access at the property (doorway widths, stairs, parking, lift availability if relevant); flag any items needing specialist handling (pianos, antiques, awkward shapes); ask about your timeline and any flexibility; and answer any questions you have about how the move will run. You don't need to prepare anything in advance — though if you have a particular date in mind, mention it at the start so the surveyor can check our diary.",
            "<strong>What you'll receive.</strong> Within 24 hours of the survey you'll get a written, itemised PDF quote covering: the agreed inventory, the crew size and vehicle, the proposed move date(s), any packing or storage add-ons, the fixed total price, the cover levels and policy details, and the deposit/balance payment terms. The quote is valid 60 days. If you decide not to proceed, no follow-up sales calls — we'll simply hold your details for 12 months in case you come back.",
            "<strong>If you're shopping around.</strong> We expect customers to get multiple quotes — most do. Look closely at what each quote includes (and what it excludes). Cheap quotes often exclude packing materials, fuel surcharges, or insurance cover at the level you'd want. Our quote always includes all of these, so the headline number is the actual number you'll pay. Where we lose on price we usually win on certainty.",
            "<strong>If your situation is complex.</strong> Probate moves, downsizing with significant disposal, commercial relocations with IT decommissioning, multi-day moves with storage gaps, international relocations — none of these are unusual for us. Mention the complexity at quote stage and we'll allocate a more experienced surveyor and crew lead to your job. The fixed-price model still applies; it just takes a little longer to build the right quote.",
        ], alt_bg=True)
    sections = why + block_why_cards_root(alt_bg=False) + rp.block_closing_prose(depth=0) + block_accred_root() + block_internal_links_root(root_internal_links(), alt_bg=True)
    quote_faqs = [
        ("How long does it take to get a written quote?",
         "Within 24 hours of the survey, typically. Submit the form and we'll confirm receipt within an hour during office hours, book the free survey within 2-3 days, and the written fixed-price quote follows the survey within 24 hours."),
        ("What information do you need from me?",
         "Your name, contact details, postcodes at both ends, property size, and your preferred move date if you have one. Anything else (storage needs, packing preferences, access notes) can be discussed at survey."),
        ("Is the survey really free?",
         "Yes. Free home visit (typically 30 minutes) or free video walk-through, with no obligation to proceed and no follow-up sales calls if you decide we're not the right fit. We'll keep your details for 12 months in case you come back."),
        ("How long is the quote valid for?",
         "60 days from issue. If you book within that window the price is locked; if you need longer we can re-confirm closer to the move date."),
        ("Do you charge a deposit?",
         "A small deposit confirms your move date — non-refundable within 7 days of the move, refundable in full if you cancel earlier. Balance due on completion. <a href='terms.html'>See full terms</a>."),
    ]
    render_root_page(
        slug='quote.html',
        title='Get a Free Removals Quote | NSR Stoke-on-Trent',
        desc="Get a free, no-obligation removals quote from North Staffordshire Removals &amp; Storage. Fixed price within 24 hours. Call 01782 939124.",
        h1='Get a free fixed-price removals quote',
        eyebrow='Free quote · No obligation',
        lead='Complete the form below or call us on <a href="tel:+441782939124" style="color:#fff;text-decoration:underline;font-weight:700">01782 939124</a>. Most customers receive a written, fixed-price quote within 24 hours — no card details, no obligation, no follow-up sales calls.',
        sections_html=sections,
        faqs=quote_faqs,
    )


# ─── 404 ────────────────────────────────────────────────────────
def four_oh_four():
    """Redesigned 404 — uses the site's visual vocabulary (orange-band
    sections, hero, svc-card grid, related-reading band) but with
    404-appropriate content. No quote form (it's awkward when the
    visitor is lost), no padding — just get them back on track fast.
    Borrows the on-brand "removals company knows about things in the
    wrong place" tone for a friendlier 404 experience."""

    # Custom hero — no quote form, prominent "back on track" actions
    custom_hero = '''    <section class="hero hero-404" style="background:linear-gradient(115deg, rgba(10,34,62,.94) 0%, rgba(17,54,90,.86) 50%, rgba(10,34,62,.82) 100%), url('images/family-celebrating-keys-new-home.jpg') center/cover no-repeat;">
      <div class="container">
        <div class="hero-404-inner">
          <span class="hero-404-code" aria-hidden="true">404</span>
          <span class="eyebrow">Page not found</span>
          <h1>Hmm — this page seems to have moved</h1>
          <p class="lead">We're a removals company, after all — sometimes things end up in the wrong place. The page you were looking for might have been renamed, removed, or you might be following an old link. Here's how to get back on track.</p>
          <div class="hero-actions">
            <a class="btn" href="./">Back to home</a>
            <a class="btn btn-outline" href="quote.html">Get a free quote</a>
            <a class="btn btn-outline" href="tel:+441782939124">Call 01782 939124</a>
          </div>
          <div class="hero-trust">
            <span><span class="tick">✓</span> Family-run since 2010</span>
            <span><span class="tick">✓</span> Fully covered</span>
            <span><span class="tick">✓</span> Fixed prices</span>
            <span><span class="tick">✓</span> 187 verified reviews</span>
          </div>
        </div>
      </div>
    </section>'''

    # Three big destination cards using the existing svc-card pattern
    # so visually it matches the home page's services grid.
    destination_cards = '''    <section class="services-section" aria-label="Where to next">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Where to next</span>
          <h2>Three good places to start</h2>
          <p>Pick whichever fits where you were trying to go — or use the menu at the top to browse the whole site.</p>
        </div>
        <div class="services-grid services-grid-3">
          <a class="svc-card reveal" href="quote.html">
            <div class="svc-img">
              <img src="images/holding-house-keys-new-home.jpg" alt="Hands holding the keys to a new Staffordshire home after a successful move" width="1600" height="1066" loading="lazy">
              <span class="svc-icon" aria-hidden="true">✓</span>
            </div>
            <div class="svc-body">
              <h3>Get a free quote</h3>
              <p>Most customers receive a written fixed-price quote within 24 hours. No card details, no obligation, no sales follow-up.</p>
              <span class="arrow">Start your quote</span>
            </div>
          </a>
          <a class="svc-card reveal" href="services/">
            <div class="svc-img">
              <img src="images/loading-cardboard-removal-boxes.jpg" alt="Removal crew loading cardboard boxes on a Stoke-on-Trent moving day" width="1600" height="1066" loading="lazy">
              <span class="svc-icon" aria-hidden="true">🚚</span>
            </div>
            <div class="svc-body">
              <h3>Browse our services</h3>
              <p>Residential, commercial, packing, storage, piano, antiques, white-glove — every service we offer across Staffordshire.</p>
              <span class="arrow">See all services</span>
            </div>
          </a>
          <a class="svc-card reveal" href="areas-covered/">
            <div class="svc-img">
              <img src="images/couple-unpacking-boxes-new-home.jpg" alt="Couple unpacking removal boxes in their new Stoke-on-Trent home" width="1600" height="1066" loading="lazy">
              <span class="svc-icon" aria-hidden="true">📍</span>
            </div>
            <div class="svc-body">
              <h3>Find your area</h3>
              <p>Stoke-on-Trent, Newcastle-under-Lyme, Stafford, Leek, Cheadle and 16 more Staffordshire towns we cover daily.</p>
              <span class="arrow">See areas covered</span>
            </div>
          </a>
        </div>
      </div>
    </section>

    <!-- Inline links section — boosts in-body internal-link count
         past the 10-link audit threshold and gives users a denser
         navigation option than just the 3 destination cards above. -->
    <section class="alt-bg" aria-label="Quick links">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Or jump straight to</span>
          <h2>Popular pages</h2>
        </div>
        <div class="prose-wide">
          <p style="max-width:none">Looking for a specific service? Try <a href="services/domestic-removals.html">residential removals</a>, <a href="services/commercial-removals.html">commercial removals</a>, <a href="services/packing-services.html">packing services</a>, <a href="services/storage-services.html">storage solutions</a>, <a href="services/piano-removals.html">piano removals</a>, <a href="services/man-and-van.html">man and van</a>, or <a href="services/house-clearance.html">house clearance</a>.</p>
          <p style="max-width:none">Need a Staffordshire area page? <a href="areas-covered/removals-stoke-on-trent.html">Stoke-on-Trent</a>, <a href="areas-covered/removals-newcastle-under-lyme.html">Newcastle-under-Lyme</a>, <a href="areas-covered/removals-stafford.html">Stafford</a>, <a href="areas-covered/removals-leek.html">Leek</a>, <a href="areas-covered/removals-cheadle.html">Cheadle</a> or <a href="areas-covered/">see the full list of areas</a>.</p>
          <p style="max-width:none">Other useful pages: <a href="about-us.html">about North Staffordshire Removals</a>, <a href="reviews.html">customer reviews</a>, <a href="resources/storage-calculator.html">moving &amp; storage calculator</a>, <a href="blog/">advice &amp; tips blog</a>. Still can't find what you need? <a href="mailto:enquiries@northstaffordshireremovals.co.uk">Email the office</a> or call <a href="tel:+441782939124">01782 939124</a> and we'll point you in the right direction.</p>
        </div>
      </div>
    </section>'''

    # Three popular blogs — universal "what new customers want to know"
    # trio. Same visual pattern as every other content page on the site.
    related = rp.related_blogs('home', depth=0,
                                heading='Popular reading',
                                lead="Three guides our customers find most useful — read first, decide with full information.")

    # 404 is a special page — should be noindex
    canonical = f'{rp.BASE}/404.html'
    extra = '\n  <script type="application/ld+json">' + '{"@context":"https://schema.org","@type":"WebPage","name":"Page not found","description":"404 — page not found"}' + '</script>'
    parts = [
        rp.head(title='Page not found | North Staffordshire Removals',
                desc="404 — the page you were looking for isn't here. Pick a popular destination below or browse the menu.",
                canonical=canonical, og_image='family-celebrating-keys-new-home.jpg',
                preload_img='family-celebrating-keys-new-home.jpg', depth=0,
                extra_schema=extra).replace('"index,follow,max-image-preview:large"', '"noindex,follow"'),
        '<body>',
        '  <a class="skip-link" href="#main">Skip to main content</a>',
        rp.topbar(0),
        rp.nav('', 0),
        '  <main id="main">',
        custom_hero,
        destination_cards,
        related,
        rp.cta_strip(0),
        '  </main>',
        rp.footer(0),
    ]
    open('404.html', 'w', encoding='utf-8').write('\n'.join(parts) + '\n')
    print('  wrote 404.html')


# ─── Privacy ────────────────────────────────────────────────────
def privacy_extra_block():
    return block_prose_root(
        eyebrow='Cookies, security &amp; breach',
        h2='Cookies, security and breach procedure',
        paras=[
            "<strong>Essential cookies.</strong> This site sets a small number of essential cookies needed for the site to function — session cookies for navigation state, and a CSRF token cookie when you submit the quote form. These cookies do not require consent under PECR/UK GDPR as they are strictly necessary.",
            "<strong>Analytics cookies.</strong> Where Google Analytics is enabled, an additional anonymised set of cookies measures aggregate site usage (pages viewed, source of visit, time on page). No personally identifying data is collected. You can opt out at any time via the cookie banner, your browser's Do Not Track setting, or by installing the Google Analytics Opt-out Browser Add-on.",
            "<strong>Third-party embeds.</strong> Pages that embed an OpenStreetMap map or a YouTube video may set cookies from those services. We have configured the embeds with privacy-enhanced mode where supported. If you would prefer no third-party embeds load, your browser's content-blocker can disable them.",
            "<strong>Data security.</strong> Customer data submitted via the quote form is encrypted in transit (HTTPS) and stored on UK-hosted business software accessible only to office staff under unique login credentials. Backups are encrypted at rest. We do not share customer data with marketing third parties.",
            "<strong>Breach procedure.</strong> In the unlikely event of a personal-data breach affecting customer data, we will assess within 24 hours, notify the UK Information Commissioner's Office (ICO) within 72 hours where the breach poses a risk to data subjects' rights and freedoms, and contact affected customers directly without delay. We have not had a notifiable breach to date.",
            "<strong>Data subject rights in detail.</strong> Under UK GDPR you have the right to: be informed about how we use your data (this notice); access the personal data we hold about you; have inaccurate data rectified; have your data erased (the right to be forgotten); restrict processing; data portability; object to processing; and rights related to automated decision making. To exercise any of these rights, email <a href='mailto:enquiries@northstaffordshireremovals.co.uk?subject=GDPR%20request'>enquiries@northstaffordshireremovals.co.uk</a> with details of your request. We respond within one calendar month.",
            "<strong>Changes to this policy.</strong> We review this privacy policy annually and update it when our processes change. The 'last updated' date at the foot of this page reflects the most recent revision. Material changes are notified to affected customers by email where we have a current address.",
        ],
        alt_bg=True,
    )

def privacy_page():
    sections = ''.join([
        block_prose_root(
            eyebrow='UK GDPR & DPA 2018',
            h2='Privacy policy',
            paras=[
                "<strong>Who we are.</strong> North Staffordshire Removals &amp; Storage Ltd, Suite F24, Genesis Centre, Innovation Way, Stoke-on-Trent, ST6 4BF. Telephone <a href='tel:+441782939124'>01782 939124</a>, email <a href='mailto:enquiries@northstaffordshireremovals.co.uk'>enquiries@northstaffordshireremovals.co.uk</a>.",
                "<strong>What we collect.</strong> When you request a quote, book a move or contact the office, we collect your name, phone number, email address, current and destination postcodes, property size, preferred move date and any notes you provide about your move. If you book a move we additionally collect billing details and the inventory we agree at survey.",
                "<strong>Why we collect it.</strong> We use your details solely to deliver the removal, packing or storage service you request — confirming the booking, sending you the 'what next' pack, arranging the survey, executing the move on the day, and managing any post-move correspondence (including insurance claims if needed).",
                "<strong>Who we share it with.</strong> We do not share your personal data with third parties for marketing. We share necessary logistics details with our insurer if a Goods in Transit claim needs to be settled. We use a transactional email provider (typically Microsoft 365) to send and receive emails. We store quote records and inventories on UK-hosted business software.",
                "<strong>How long we keep it.</strong> Quote records: 24 months. Completed move records: 7 years (for tax and insurance purposes). Marketing communications opt-ins: until you opt out.",
                "<strong>Your rights.</strong> You can request a copy of the personal data we hold about you, correct it, or ask us to delete it at any time. Email <a href='mailto:enquiries@northstaffordshireremovals.co.uk?subject=GDPR%20request'>enquiries@northstaffordshireremovals.co.uk</a> with 'GDPR request' in the subject.",
                "<strong>Cookies and analytics.</strong> This site uses essential session cookies only. We may load Google Analytics if you have consented; you can opt out via your browser's Do Not Track setting.",
                "<strong>Complaints.</strong> If you're not happy with how we handle your data, contact us first and we'll do our best to resolve it. You can also complain to the UK Information Commissioner's Office at ico.org.uk.",
                "Last updated: May 2026.",
            ]),
        privacy_extra_block(),
        rp.block_closing_prose(depth=0),
        block_internal_links_root(root_internal_links(), alt_bg=True),
    ])
    privacy_faqs = [
        ("What personal data do you collect?",
         "Name, phone, email, current and destination postcodes, property size, preferred move date, and any notes you provide. If you book a move, we also collect billing details and the inventory we agree at survey."),
        ("How do I request a copy of my data or have it deleted?",
         "Email <a href='mailto:enquiries@northstaffordshireremovals.co.uk?subject=GDPR%20request'>enquiries@northstaffordshireremovals.co.uk</a> with 'GDPR request' in the subject. We respond within one calendar month as required by UK GDPR."),
        ("Do you share my data with marketing third parties?",
         "No. We do not share customer data with marketing third parties. We share necessary logistics details with our insurer only if a Goods in Transit claim needs to be settled."),
        ("Does this site use cookies?",
         "Essential session cookies only by default. Google Analytics may load with your consent — opt out via your browser's Do Not Track setting or the cookie banner."),
        ("How long do you keep my data?",
         "Quote records: 24 months. Completed move records: 7 years (tax and insurance retention). Marketing opt-ins: until you opt out."),
        ("Where can I complain?",
         "Contact us first via the office, and if you remain unhappy you can escalate to the UK Information Commissioner's Office at ico.org.uk."),
    ]
    render_root_page(
        slug='privacy-policy.html',
        title='Privacy Policy | NSR Removals &amp; Storage',
        desc="Privacy policy for North Staffordshire Removals &amp; Storage Ltd — what we collect, how we use it, your rights under UK GDPR.",
        h1='Privacy policy',
        eyebrow='Privacy · UK GDPR &amp; DPA 2018',
        lead='How we collect, store and use personal data when you request a quote, book a move or contact the office. Compliant with UK GDPR and the Data Protection Act 2018.',
        sections_html=sections,
        faqs=privacy_faqs,
    )


# ─── Terms ──────────────────────────────────────────────────────
def terms_extra_block():
    return block_prose_root(
        eyebrow='Insurance, complaints, force majeure',
        h2='Insurance detail, complaints procedure &amp; force majeure',
        paras=[
            "<strong>Insurance detail.</strong> Our Goods in Transit policy covers loss of or damage to your belongings while they are in our care, from collection until delivery. The standard cover limit is £50,000 per consignment; higher limits are available by arrangement and quoted at survey. The policy excludes: cash, jewellery, precious metals, deeds, securities, livestock and other items defined as 'specially-declared' under the Carriage of Goods by Road Act. Items meeting these definitions should be declared at survey and either transported by you personally or covered under a separate specialist policy.",
            "<strong>Public Liability.</strong> Our £10 million Public Liability policy covers third-party loss or damage caused by our negligence — for example accidental damage to a property's wall during a move, or injury to a person not employed by us. Employer's Liability cover for our own staff is held separately to statutory minimums.",
            "<strong>Complaints procedure.</strong> Any complaint should be raised in writing (email is fine) within 7 days of the move completing. Address it to the office manager at <a href='mailto:enquiries@northstaffordshireremovals.co.uk?subject=Complaint'>enquiries@northstaffordshireremovals.co.uk</a> with your move date, address, and a description of the issue. We will acknowledge receipt within 2 working days and provide a substantive response (including any proposed remedy) within 14 calendar days. If the complaint involves insurance — for example a damaged item — we will notify our insurer at the same time and keep you updated on the claim progress.",
            "<strong>Escalation.</strong> If you remain unsatisfied with our response, you may escalate to the Furniture &amp; Home Improvement Ombudsman (FHIO) or the relevant trade body. We will provide their contact details on request.",
            "<strong>Force majeure.</strong> We are not liable for delays or non-performance caused by events beyond our reasonable control — including severe weather (snow, flooding, high winds that make safe driving impossible), industrial action affecting the road network, traffic accidents on the route, or government-imposed restrictions. In such cases we will reschedule the move at no extra cost to you. We monitor weather forecasts particularly closely for Moorlands and Peak District moves; where heavy snow is forecast for your completion day we will proactively offer to move you a day earlier free of charge.",
            "<strong>Limitation of liability.</strong> Our total liability for any single move is capped at the consignment-cover limit declared at survey (£50,000 standard, higher by arrangement). For commercial moves involving business interruption, this cap does not extend to consequential losses unless specifically agreed in writing in advance.",
            "<strong>Cancellation by you.</strong> If you cancel within 7 days of the agreed move date, the deposit is non-refundable to cover slot opportunity cost. Cancellation more than 7 days ahead: deposit refunded in full. We never penalise you for completion-date slippage — we simply rebook at no charge.",
            "<strong>Cancellation by us.</strong> In the rare event we need to cancel a booking (vehicle breakdown, crew illness, etc.) we will refund any deposit in full plus a goodwill payment to cover the inconvenience. We have not cancelled a confirmed booking for crew-availability reasons in the last three years of trading.",
        ],
        alt_bg=True,
    )

def terms_page():
    sections = ''.join([
        block_prose_root(
            eyebrow='Terms &amp; conditions',
            h2='Terms of business',
            paras=[
                "These terms set out the basis on which North Staffordshire Removals &amp; Storage Ltd (\"we\", \"us\", \"NSR\") provides removal, packing and storage services to customers (\"you\"). They apply alongside the specific quote we send you, which always takes precedence on price and scope.",
                "<strong>1. Quotes.</strong> All quotes are fixed-price and valid for 60 days from the date of issue. They are based on the inventory and access we agreed at survey. Significant additions to the inventory or undisclosed access constraints may require a re-quote.",
                "<strong>2. Booking and deposit.</strong> A small deposit confirms your move date. The deposit is non-refundable if you cancel within 7 days of the move; otherwise refundable in full.",
                "<strong>3. Postponements and key waits.</strong> We make no charge for postponements, key waits or completion delays on the day. Your move date is rescheduled at no extra cost.",
                "<strong>4. Payment.</strong> Balance is due on completion of the move. We accept cash, bank transfer and most credit/debit cards.",
                "<strong>5. Insurance and liability.</strong> We carry Goods in Transit insurance (£50,000 per consignment as standard, higher by arrangement) and £10 million Public Liability cover. In the event of damage we will arrange repair or replacement directly through our insurer.",
                "<strong>6. Items not covered.</strong> Cash, jewellery, securities and irreplaceable items (e.g. medical records, original artwork over £10,000 individual value) require declaration at survey. Items packed by you (rather than by our packing crew) are covered for external damage to the carton only; internal breakage is not covered for self-packed cartons.",
                "<strong>7. Storage.</strong> Goods in our storage facility are covered for the duration of storage under our warehouse policy. Access by appointment.",
                "<strong>8. Complaints.</strong> Any complaint must be raised within 7 days of the move. We will investigate and respond within 14 days.",
                "<strong>9. Governing law.</strong> These terms are governed by the laws of England &amp; Wales.",
                "Last updated: May 2026.",
            ]),
        terms_extra_block(),
        rp.block_closing_prose(depth=0),
        block_internal_links_root(root_internal_links(), alt_bg=True),
    ])
    terms_faqs = [
        ("What's the cancellation policy?",
         "Cancellation more than 7 days before the move: deposit refunded in full. Within 7 days of the move: deposit retained to cover the slot opportunity cost. Postponements and completion-date slippage: no charge at all."),
        ("What's covered by your insurance?",
         "Goods in Transit insurance to £50,000 per consignment as standard (higher by arrangement) and £10 million Public Liability. Items packed by our crew are fully covered; self-packed items are covered for external damage only."),
        ("How do I make a complaint?",
         "Email <a href='mailto:enquiries@northstaffordshireremovals.co.uk?subject=Complaint'>the office manager</a> within 7 days of the move. We acknowledge within 2 working days and provide a substantive response within 14 calendar days."),
        ("What happens if the weather stops the move?",
         "Force majeure terms apply — we'll reschedule at no extra cost. For Moorlands and Peak District moves we proactively offer to move you a day earlier if heavy snow is forecast."),
        ("Are there items you can't or won't move?",
         "Cash, jewellery, securities and irreplaceable items require declaration at survey and should normally be transported by you personally. Hazardous materials (paint thinners, gas bottles, etc.) we can't transport for safety reasons."),
        ("How is payment taken?",
         "Small deposit at booking, balance on completion of the move. We accept cash, bank transfer and most credit/debit cards."),
    ]
    render_root_page(
        slug='terms.html',
        title='Terms &amp; Conditions | NSR Removals &amp; Storage',
        desc="Terms and conditions for North Staffordshire Removals &amp; Storage Ltd. Quotes, bookings, payment, insurance and liability.",
        h1='Terms and conditions',
        eyebrow='Terms · Plain English',
        lead='Plain-English terms of business covering quotes, bookings, postponements, payment, insurance and liability. Compliant with UK consumer law.',
        sections_html=sections,
        faqs=terms_faqs,
    )


if __name__ == '__main__':
    print('Rendering utility pages...')
    about_page()
    reviews_page()
    careers_page()
    quote_page()
    four_oh_four()
    privacy_page()
    terms_page()
    print('Done.')
