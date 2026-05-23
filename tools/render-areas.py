#!/usr/bin/env python3
"""Render the 8 area pages + areas-covered/index.html.
Uses the shared scaffolding in render-pages.py (head/topbar/nav/cta/footer)."""

from __future__ import annotations
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

# Import shared helpers from render-pages.py
import importlib.util
spec = importlib.util.spec_from_file_location("rp", os.path.join(ROOT, 'tools', 'render-pages.py'))
rp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rp)

os.chdir(ROOT)


AREAS = [
    {
        'slug': 'areas-covered/removals-stoke-on-trent.html',
        'town': 'Stoke-on-Trent',
        'title': 'Removals Stoke-on-Trent | NSR Removals &amp; Storage',
        'desc': "Removals in Stoke-on-Trent — the six towns of Hanley, Burslem, Tunstall, Longton, Fenton and Stoke. Family-run, fixed price, fully covered.",
        'h1': 'Removals across the six towns of Stoke-on-Trent',
        'eyebrow': 'Stoke-on-Trent · ST1–ST7',
        'lead': "Hanley, Burslem, Tunstall, Longton, Fenton and Stoke — the six towns of Stoke-on-Trent are our home patch. North Staffordshire Removals &amp; Storage Ltd has been family-run from a Stoke depot since 2010, and our crews live, breathe and drive the ST postcode area every working day.",
        'hero_img': 'family-celebrating-keys-new-home.jpg',
        'paras': [
            ("Removals in the Potteries, by people who live here",
             [
                "Stoke-on-Trent is unique: six federated towns strung along the A5008 and the Caldon Canal, each with its own High Street, parking habits and access challenges. A move out of a Victorian terrace in Burslem is a different job from a four-bedroom new-build off the A500 in Trentham — and our crews price each accordingly.",
                "From our Stoke-on-Trent depot at the Genesis Centre off Innovation Way (ST6 4BF), we're on the doorstep of every postcode in the ST1–ST7 range. Most local moves complete in a single day. Larger four-bedroom moves out to the Moorlands or Newcastle borough sometimes phase into two days if you'd like a slower, calmer pace.",
                "We've moved customers in and out of nearly every estate in the city — Westport, Birches Head, Bucknall, Trentham Lakes, Sneyd Green, Penkhull, Hartshill — and we know which roads to avoid at school-run time, which one-way streets are mistakes to enter with a 7.5-tonne, and where the loading bays are at every town centre site.",
             ]),
            ("Which Stoke postcodes we cover",
             [
                "<strong>ST1 (Hanley)</strong> — the city centre. Tight terraces, busy lunchtime parking, regular Cultural Quarter moves. We typically work the residential streets early morning or after 6pm to avoid the worst of the parking pressure.",
                "<strong>ST2 (Abbey Hulton, Birches Head, Smallthorne)</strong> — mostly residential, easier access, large estate housing. Our most common Stoke jobs.",
                "<strong>ST3 (Longton, Meir, Blurton)</strong> — mix of older Victorian terraces and 1980s/90s estates. Some of the steeper terraced streets need our experience.",
                "<strong>ST4 (Penkhull, Trent Vale, Hartshill, Hanford, Stoke proper)</strong> — University of Keele student moves and family relocations alike. We do a lot of August student work here.",
                "<strong>ST5 (Newcastle-under-Lyme)</strong> — technically a separate borough, see our <a href='removals-newcastle-under-lyme.html'>Newcastle removals page</a>.",
                "<strong>ST6 (Burslem, Tunstall, Sneyd Green)</strong> — our depot postcode. Burslem's older terraces and Sneyd Green's estates are weekly territory.",
                "<strong>ST7 (Kidsgrove, Talke, Audley)</strong> — northern boundary, often jobs that cross into Cheshire.",
             ]),
            ("Local knowledge that saves you money",
             [
                "Parking in Stoke is the difference between a smooth morning load and a chaotic one. Our crew leader will scope your street the day before if needed, talk to the council about a parking suspension where the load looks tight, and confirm whether we can stop the Luton outside or whether we'll need to shuttle.",
                "Most Stoke streets allow our 7.5-tonne to stand for the duration of a load — the exceptions are the steeper Burslem and Hanley terraces, where we'll downsize to a Luton and double the run if needed. We never add extra costs for these decisions; everything is fixed at survey.",
                "If you're moving into one of the newer Trentham Lakes or Westbury Park estates, we know the developer's parking restrictions and the resident-parking dispensation process. Mention it at booking and we'll handle the paperwork.",
             ]),
            ("Services for Stoke moves",
             [
                "Every Stoke-on-Trent move is covered by our standard residential removal service — <a href='../services/domestic-removals.html'>see what's included</a>. Add <a href='../services/packing-services.html'>packing</a> if you'd rather not pack yourself; add <a href='../services/storage-services.html'>storage</a> if your completion date is uncertain.",
                "Office and commercial moves around Hanley, the Cultural Quarter and the business parks at Trentham Lakes and Festival Park run on our <a href='../services/commercial-removals.html'>commercial relocation service</a> — usually weekend lifts so you're operational on Monday morning.",
                "Specialist <a href='../services/piano-removals.html'>piano removals</a> across the city — we've moved everything from upright Yamahas in Birches Head to a Steinway grand out of a Trentham townhouse.",
             ]),
        ],
        'faqs': [
            ("How much does a Stoke-on-Trent house move cost?",
             "Most 2–3 bed local moves within Stoke fall between £450 and £950. Larger 4-bed moves, packing service and storage are quoted on top. <a href='../quote.html'>Get your free quote</a>."),
            ("Which Stoke postcodes do you cover?",
             "All of ST1 through ST7 — the six towns of Stoke plus surrounding postcodes. Newcastle-under-Lyme (ST5) is covered separately on our <a href='removals-newcastle-under-lyme.html'>Newcastle page</a>."),
            ("Can you handle a move with very tight street parking?",
             "Yes — we'll scope the street the day before, downsize to a Luton if needed and handle any parking-suspension request with the council."),
            ("Do you do moves to and from the Cultural Quarter offices?",
             "Yes — Cultural Quarter and Hanley town centre commercial moves are usually run as out-of-hours weekend lifts. See our <a href='../services/commercial-removals.html'>commercial removals</a>."),
            ("How quickly can you book a Stoke move?",
             "We can often fit a local Stoke move within 1–2 weeks off-peak; 4–6 weeks during May–September. <a href='../quote.html'>Request a quote</a> and we'll confirm."),
        ],
    },
    {
        'slug': 'areas-covered/removals-newcastle-under-lyme.html',
        'town': 'Newcastle-under-Lyme',
        'title': 'Removals Newcastle-under-Lyme | NSR Removals',
        'desc': "Removals in Newcastle-under-Lyme — Newcastle, Kidsgrove, Audley, Madeley and Keele. Family-run, fixed price, fully covered.",
        'h1': 'Removals across Newcastle-under-Lyme borough',
        'eyebrow': 'Newcastle-under-Lyme · ST5',
        'lead': "Newcastle-under-Lyme is the second-largest town in North Staffordshire and one of our busiest patches. From the Georgian centre to the university quarter at Keele, the family estates of Cross Heath and Bradwell, and the villages out to Audley and Madeley, our crews cover the whole borough — at a fixed price, with no surprises on the day.",
        'hero_img': 'estate-agent-handing-house-keys.jpg',
        'paras': [
            ("Newcastle borough moves done properly",
             [
                "Newcastle-under-Lyme borough sits just west of Stoke and stretches from the Cheshire border at Audley right down to the Trentham boundary. It's a borough of contrasts — Georgian high-street properties, post-war estates, modern executive new-builds and the rural villages that ring the borough.",
                "Our team has been moving Newcastle families since 2010. We're based 15 minutes away in Stoke-on-Trent so a crew is on your driveway in good time, with a clean Luton or 7.5-tonne and all the kit needed for the day.",
                "Newcastle's town centre access has tightened in recent years, with several streets going one-way and the bus gate on Ironmarket. We know the workarounds and the loading windows that work; just tell us your address and we'll plan accordingly.",
             ]),
            ("Newcastle borough postcodes we cover",
             [
                "<strong>ST5 1–3 (Newcastle town centre, Cross Heath, May Bank)</strong> — busy residential, mix of older properties and 1960s estates. Tight parking around the King's Avenue and Knutton areas.",
                "<strong>ST5 4 (Bradwell, Porthill)</strong> — family estates, easier access, regular work for us.",
                "<strong>ST5 5 (Keele, Silverdale)</strong> — Keele University student moves in August, plus family relocations in Silverdale.",
                "<strong>ST5 6 (Madeley, Onneley, Aston)</strong> — rural villages on the Cheshire border. We do a lot of rural moves here.",
                "<strong>ST5 7 (Audley, Halmer End, Bignall End)</strong> — northern villages, often jobs that combine into the Kidsgrove side of Stoke.",
                "<strong>ST5 9 (Westlands, Clayton)</strong> — established residential, often four-bedroom family moves.",
             ]),
            ("Why Newcastle picks us",
             [
                "We've been moving Newcastle families and businesses since 2010, and a large share of our work comes from personal recommendations — neighbours and friends who've used us before. The reasons are consistent: the fixed-price quote really is fixed, the crew is polite and professional, and there are no charges if your completion slips.",
                "We've worked with Newcastle estate agents over the years and many of them recommend us when their vendors and buyers ask for a removal company. If your agent has suggested us, mention it at booking — we'll let them know we've taken care of you.",
                "Keele University staff and students get a small discount on documented academic moves; ask for details when you book.",
             ]),
            ("Services in Newcastle",
             [
                "Most Newcastle moves run on our <a href='../services/domestic-removals.html'>residential removals service</a>. Office and commercial relocations around the Newcastle town centre and the Lymedale Business Park use our <a href='../services/commercial-removals.html'>commercial service</a>.",
                "If your completion date is uncertain (common with the larger Newcastle housing chains), our <a href='../services/storage-services.html'>storage service</a> at the Stoke depot is the safety net — we collect on the original date, store, and redeliver when your chain completes.",
                "<a href='../services/packing-services.html'>Packing services</a> are popular with the larger Westlands and Clayton family moves — full pack the day before saves a chaotic morning.",
             ]),
        ],
        'faqs': [
            ("How much does a Newcastle-under-Lyme house move cost?",
             "Most local Newcastle 2–3 bed moves fall between £450 and £950 depending on access, packing and storage. <a href='../quote.html'>Request a free quote</a>."),
            ("Do you cover Audley and Madeley?",
             "Yes — Audley, Halmer End, Madeley, Onneley, Aston, Betley — the whole western edge of the borough."),
            ("Can you do a Newcastle move at the weekend?",
             "Yes — Saturday and Sunday slots available; weekend pricing is the same as weekday for residential. Commercial out-of-hours by arrangement."),
            ("Do Keele students get a discount?",
             "Yes, a small discount on documented Keele University academic moves. Ask at booking."),
            ("How far ahead should I book a Newcastle move?",
             "4–6 weeks during May–September peak, 1–2 weeks off-peak. <a href='../quote.html'>Get your free quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-stafford.html',
        'town': 'Stafford',
        'title': 'Removals Stafford | NSR Removals &amp; Storage',
        'desc': "Removals in Stafford — Stafford, Gnosall, Penkridge, Brewood, Haughton. Family-run from Stoke, fixed price, fully covered.",
        'h1': 'Removals across Stafford and surrounding villages',
        'eyebrow': 'Stafford · ST16–ST21',
        'lead': "Stafford is the county town and one of the busier regional markets for our removal service. From the Georgian centre to the Doxey and Castle Town estates, the new-build developments at Beaconside, and the surrounding villages at Gnosall, Penkridge and Brewood — our team has been moving Stafford families and businesses since 2010.",
        'hero_img': 'loading-cardboard-removal-boxes.jpg',
        'paras': [
            ("Stafford moves with local know-how",
             [
                "Stafford is a 30-minute drive from our Stoke depot down the M6, but for the volume of work we do in the town we treat it as part of our home patch. A Stafford-based crew leader runs every Stafford job, so the team knows the access at the Greyfriars Way developments, the parking habits on Tixall Road, and the loading bays at Stafford railway station and the town centre.",
                "We cover the full ST16–ST21 range — the town itself, Doxey, Castle Town, Highfields, Stallbrook, Beaconside, plus the villages out to Gnosall, Penkridge, Brewood and Haughton.",
                "Stafford has grown rapidly with new estates at Doxey Fields, the Beaconside areas and the Marston Grange development off the A34. We've moved customers in and out of every one of these new-build estates — and we know the developer parking restrictions and the resident-permit process.",
             ]),
            ("Stafford postcodes we cover",
             [
                "<strong>ST16 (Stafford town, Castle Town, Tillington)</strong> — Stafford proper. Mix of Georgian, Victorian and 1970s housing. Town centre needs careful access planning.",
                "<strong>ST17 (Stafford south, Walton-on-the-Hill, Weeping Cross)</strong> — established residential, easier access, four-bedroom family homes.",
                "<strong>ST18 (Great Haywood, Little Haywood, Colwich, Milford)</strong> — village locations along the Trent &amp; Mersey Canal corridor.",
                "<strong>ST19 (Penkridge, Acton Trussell, Wheaton Aston)</strong> — Penkridge is one of our regular village stops, popular with commuters working in Stafford and Wolverhampton.",
                "<strong>ST20 (Gnosall, Bradeley, Adbaston)</strong> — rural villages, often farmhouse moves with longer access tracks.",
                "<strong>ST21 (Eccleshall)</strong> — see our <a href='removals-eccleshall.html'>dedicated Eccleshall page</a>.",
             ]),
            ("Office moves in Stafford",
             [
                "Stafford has a strong commercial base — the County Council, MoD Stafford, GE Energy, and several large legal and accounting practices. Our <a href='../services/commercial-removals.html'>commercial relocations service</a> covers all of them, with weekend and out-of-hours lifts the norm.",
                "We've also moved several of the smaller Stafford agencies and IT firms within the town as they've grown — typically a Friday-evening start, Saturday assembly, fully operational Monday morning.",
             ]),
            ("Services for Stafford moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> covers the great majority of Stafford work. <a href='../services/packing-services.html'>Packing</a> on request. <a href='../services/storage-services.html'>Storage</a> at our Stoke depot if your chain delays.",
                "Specialist <a href='../services/piano-removals.html'>piano removals</a> for the Stafford concert and amateur music community.",
            ]),
        ],
        'faqs': [
            ("How much does a Stafford house move cost?",
             "Most Stafford 2–3 bed moves fall between £500 and £1,050 depending on distance to your new property, packing and access. <a href='../quote.html'>Get a free quote</a>."),
            ("Do you cover the villages around Stafford?",
             "Yes — Gnosall, Penkridge, Brewood, Haughton, Eccleshall and the surrounding rural lanes."),
            ("Can you handle a Stafford-to-Stoke move?",
             "Yes — that's a routine 30-minute corridor for us. Quoted on the standard residential service."),
            ("Do you have a Stafford depot?",
             "Our depot is in Stoke-on-Trent (Genesis Centre, ST6 4BF), 30 minutes up the M6. We treat Stafford as part of our home patch."),
            ("How quickly can you book a Stafford move?",
             "4–6 weeks during May–September; often 1–2 weeks off-peak. <a href='../quote.html'>Request a quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-stone.html',
        'town': 'Stone',
        'title': 'Removals Stone | NSR Removals &amp; Storage',
        'desc': "Removals in Stone, Staffordshire — Stone, Walton, Aston, Yarnfield and Barlaston. Family-run, fixed price, fully covered.",
        'h1': 'Removals across Stone and the Trent Valley',
        'eyebrow': 'Stone · ST15',
        'lead': "Stone is one of the most picturesque market towns in Staffordshire and a regular stop for our removal crews. From the Georgian properties on the High Street to the larger family homes at Walton and Aston, and the canalside developments at Barlaston, our team has been moving Stone customers since 2010.",
        'hero_img': 'couple-unpacking-boxes-new-home.jpg',
        'paras': [
            ("Stone moves with care and local knowledge",
             [
                "Stone sits midway between Stoke and Stafford, with the Trent &amp; Mersey Canal running through it. It's a town with character — Georgian sash windows, narrow streets, and the unmistakable canalside atmosphere that draws people from across the Midlands.",
                "That character is also what makes Stone moves a little trickier than average. The High Street and the side streets off it are tight; some properties have rear-only access via a canal path. Our crew always surveys these before the move, and where access is exceptional we'll send a smaller Luton and run extra trips rather than trying to force a 7.5-tonne onto a narrow lane.",
                "We cover the whole ST15 postcode — Stone town, Walton, Aston-by-Stone, Yarnfield, Barlaston, Tittensor and the surrounding villages out to the boundary with Stafford and Stoke.",
             ]),
            ("Stone postcodes we cover",
             [
                "<strong>ST15 0–7 (Stone town centre, Walton, Aston, Yarnfield, Barlaston)</strong> — our regular Stone territory, full residential service.",
                "<strong>ST15 8–9 (Tittensor, Saverley Green, Hilderstone)</strong> — village properties with sometimes-tricky access. We'll survey ahead.",
             ]),
            ("Why Stone moves are different",
             [
                "Stone's canalside properties often have unusual access — front-door street-side, but the only way to load is via a rear garden path that opens onto the towpath. We've moved a number of these and we know which streets allow vehicle access to the back, and which require a long walk-out to a parked van.",
                "The town's growing fast, with new developments at the Walton fringe and along the A34 to Stoke. We've moved into nearly every new-build estate around Stone and know the developer access rules.",
             ]),
            ("Services for Stone moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> is the standard service for Stone — fixed price, fully covered, free survey.",
                "<a href='../services/packing-services.html'>Packing services</a> particularly popular with the larger Walton and Aston family moves; <a href='../services/storage-services.html'>storage</a> useful for the canalside completions where the chain is uncertain.",
                "<a href='../services/piano-removals.html'>Piano removals</a> — the Stone musical community is active and we handle several piano moves a year here.",
             ]),
        ],
        'faqs': [
            ("Do you do Stone canalside property moves?",
             "Yes — we survey access ahead and use a smaller Luton if the rear access is tight. Pricing fixed at survey."),
            ("How much does a Stone house move cost?",
             "Most Stone 2–3 bed moves fall between £450 and £950. <a href='../quote.html'>Get a free quote</a>."),
            ("Do you cover Barlaston and Yarnfield?",
             "Yes — both are in ST15 and on our regular run."),
            ("Can you store between completions for a Stone move?",
             "Yes — our Stoke depot has palletised storage units, charged by the week. <a href='../services/storage-services.html'>See storage</a>."),
            ("How quickly can you fit in a Stone move?",
             "4–6 weeks peak, 1–2 weeks off-peak. <a href='../quote.html'>Request a quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-leek.html',
        'town': 'Leek',
        'title': 'Removals Leek | NSR Removals &amp; Storage',
        'desc': "Removals in Leek and the Staffordshire Moorlands — Leek, Cheddleton, Werrington, Endon, Wetley Rocks. Family-run, fixed price.",
        'h1': 'Removals across Leek and the Staffordshire Moorlands',
        'eyebrow': 'Leek · ST13',
        'lead': "Leek is the capital of the Staffordshire Moorlands, perched on the edge of the Peak District. Our team has been moving Moorlands families for over a decade, and we know the lanes, the access, and the weather quirks that make this corner of Staffordshire special.",
        'hero_img': 'family-celebrating-keys-new-home.jpg',
        'paras': [
            ("Moves across the Staffordshire Moorlands",
             [
                "The Moorlands is the most rural part of our patch — narrow lanes, farmhouse driveways, stone cottages with low door frames, and the changeable Peak District weather. Our crews enjoy these jobs precisely because they're different: every Moorlands move teaches us something.",
                "Our Stoke depot is a 25-minute drive from Leek down the A53. From the Leek depot turn-off we cover the whole ST13 postcode — Leek town, Cheddleton, Wetley Rocks, Werrington, Endon, Brown Edge, Longsdon, and the smaller hamlets out to the Roaches and Tittesworth Reservoir.",
                "We've moved farmhouses, stone cottages, riverside properties at Rudyard Lake, and the modern estates at the Birchall and Cornhill developments. Every one has its own access story — and our team plans accordingly.",
             ]),
            ("Leek and Moorlands postcodes",
             [
                "<strong>ST13 5–6 (Leek town, Birchall, Westwood)</strong> — town centre with Georgian terraces and the Market Square. Tight access in places, easy in others.",
                "<strong>ST13 7 (Cheddleton, Wetley Rocks, Longsdon)</strong> — village locations along the A520 corridor. Mostly easy access.",
                "<strong>ST13 8 (Werrington, Cellarhead, Endon)</strong> — popular family villages, often estate housing with straightforward access.",
                "<strong>ST10 (Cheadle, Tean, Kingsley)</strong> — Moorlands towns to the south. We cover these too — give us a postcode and we'll quote.",
             ]),
            ("Moorlands weather and access tips",
             [
                "The Moorlands sit at 800–1,500ft above sea level and the weather can change in an hour. We monitor the forecast for Moorlands moves and will move you a day earlier if heavy snow is forecast for completion day. That's a free service — no extra charge for a weather-related date change.",
                "Many Moorlands farmhouses sit at the end of a quarter-mile gravel track. We'll survey ahead and either use a smaller Luton with multiple runs, or arrange a shuttle from the road end. Our pricing is fixed once we've seen the access.",
                "Stone cottage doorways are often lower than modern standards. We measure your largest item (usually a wardrobe or three-seater sofa) against the new property's tightest doorway at survey, and confirm it'll fit. If not, we know carpenters and locksmiths who can help.",
             ]),
            ("Services for Leek and Moorlands moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for all of ST13. <a href='../services/packing-services.html'>Packing services</a> particularly popular with farmhouse moves (large volume + Moorlands distance = full pack saves time).",
                "<a href='../services/storage-services.html'>Storage</a> at our Stoke depot — useful for Moorlands customers between completions; we collect from the Moorlands and store in Stoke.",
                "<a href='../services/piano-removals.html'>Piano removals</a> — the Leek music community is active and we handle several piano jobs a year in the Moorlands.",
             ]),
        ],
        'faqs': [
            ("Can you handle a farmhouse move in the Moorlands?",
             "Yes — we'll survey the access track and confirm vehicle size. Often a Luton with two runs is the right answer rather than a 7.5-tonne stuck on a track."),
            ("How much does a Leek move cost?",
             "Most Leek 2–3 bed moves fall between £550 and £1,150, with the surcharge over Stoke pricing being the extra distance and access time. <a href='../quote.html'>Get a free quote</a>."),
            ("What if the weather turns on completion day?",
             "We monitor Moorlands forecasts and will move you a day earlier free of charge if heavy snow or ice is forecast. No charge for weather-related date changes."),
            ("Do you cover Cheadle and Tean?",
             "Yes — ST10 is on our patch. Mentioned above; <a href='../quote.html'>request a quote</a>."),
            ("Is my move fully covered in the Moorlands?",
             "Yes — full Goods in Transit and £10m Public Liability everywhere we operate. Claims handled directly by our team."),
        ],
    },
    {
        'slug': 'areas-covered/removals-eccleshall.html',
        'town': 'Eccleshall',
        'title': 'Removals Eccleshall | NSR Removals &amp; Storage',
        'desc': "Removals in Eccleshall and the villages of west Staffordshire. Family-run, fixed price, fully covered. Call 01782 939124.",
        'h1': 'Removals across Eccleshall and west Staffordshire',
        'eyebrow': 'Eccleshall · ST21',
        'lead': "Eccleshall is one of the prettiest market towns in west Staffordshire and a regular destination for our removal crews. From the Georgian High Street to the surrounding villages of Slindon, Knightley, Cotes Heath and Standon, we've been moving Eccleshall families since 2010.",
        'hero_img': 'family-celebrating-keys-new-home.jpg',
        'paras': [
            ("Eccleshall moves with a careful touch",
             [
                "Eccleshall (pronounced 'Eck-uls-hall' locally — getting that right is half the battle) is a historic market town with a striking castle, a wide Georgian High Street and some of the most desirable rural housing in Staffordshire. Many properties are listed; many have access via narrow rear cobbled lanes; many have valuable antiques inside.",
                "Our crews are used to all of this. Pad-wrapping every piece in the home, slow careful loading, the right kit (skid boards, blanket wraps, corner protectors), and a fixed price agreed at survey. No hourly billing, no last-minute extras.",
                "From our Stoke depot we run down the A519 to Eccleshall in about 35 minutes. The surrounding villages — Slindon, Knightley, Cotes Heath, Standon, Croxton — are all on our regular run.",
             ]),
            ("Eccleshall postcodes and villages",
             [
                "<strong>ST21 6 (Eccleshall town, High Offley, Outlands)</strong> — town centre and immediate villages. Mix of Georgian properties and modern estate housing on the town fringe.",
                "<strong>ST21 7 (Slindon, Knightley, Cotes Heath, Standon)</strong> — rural village properties, often with antique furniture and longer access tracks.",
             ]),
            ("Antique-rich moves",
             [
                "A high proportion of Eccleshall properties contain valuable antiques — Welsh dressers, longcase clocks, period chests, oil paintings, ceramics. Our crew is trained in handling these, and we'll bring corner protectors, blanket wraps and bespoke crates as needed.",
                "For very high-value pieces we recommend a separate antique inventory at survey, photographed and condition-noted, with cover confirmed in writing. <a href='../services/domestic-removals.html'>Standard cover</a> handles most cases; bespoke arrangements for items over £10,000 individual value.",
             ]),
            ("Services for Eccleshall moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for the full ST21 area. <a href='../services/packing-services.html'>Packing services</a> particularly popular here — many customers prefer the professional pack option for the kitchen and china.",
                "<a href='../services/storage-services.html'>Storage</a> at our Stoke depot if your chain delays. <a href='../services/piano-removals.html'>Piano removals</a> for the strong Eccleshall musical community.",
             ]),
        ],
        'faqs': [
            ("Do you handle antique-furniture moves in Eccleshall?",
             "Yes — extensive experience with Welsh dressers, longcase clocks, period chests and oil paintings. Bespoke crating for high-value pieces."),
            ("How much does an Eccleshall move cost?",
             "Most Eccleshall 2–3 bed moves fall between £550 and £1,100. <a href='../quote.html'>Get a free quote</a>."),
            ("Do you cover Slindon and Standon?",
             "Yes — both villages are in ST21 and on our regular run."),
            ("Can my high-value antiques be specifically insured?",
             "Yes — we'll list them separately at survey and confirm bespoke cover in writing for pieces over £10,000 individual value."),
            ("How far ahead should I book?",
             "4–6 weeks peak season, 1–2 weeks off-peak. <a href='../quote.html'>Request a free quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-burton-on-trent.html',
        'town': 'Burton-on-Trent',
        'title': 'Removals Burton-on-Trent | NSR Removals &amp; Storage',
        'desc': "Removals in Burton-on-Trent — Burton, Stretton, Branston, Barton-under-Needwood. Family-run, fixed price, fully covered.",
        'h1': 'Removals across Burton-on-Trent and east Staffordshire',
        'eyebrow': 'Burton-on-Trent · DE13–DE15',
        'lead': "Burton-on-Trent is the gateway between Staffordshire and Derbyshire — a busy market town with strong commuter links to Birmingham, Derby and Stoke. Our team has been moving Burton families and businesses for over a decade, and we treat the DE13–DE15 postcodes as part of our regular Staffordshire patch.",
        'hero_img': 'loading-cardboard-removal-boxes.jpg',
        'paras': [
            ("Burton moves done the local way",
             [
                "Burton-on-Trent sits 45 minutes south-east of our Stoke depot down the A50. For the volume of Burton work we do — both residential and commercial — we keep a Burton-savvy crew on standby and a dedicated route plan that avoids the worst of the A38 morning peak.",
                "We cover Burton town centre, the established estates at Winshill, Stretton and Branston, the newer developments at Branston Locks and Stretton Park, and the surrounding villages of Barton-under-Needwood, Newborough and Tutbury.",
                "Burton's housing market has grown rapidly thanks to its commuter links and the value-for-money property prices vs. Birmingham and Derby. We've moved a lot of customers <em>into</em> Burton over the last few years, often from longer-distance origins like Manchester, Leicester and Coventry.",
             ]),
            ("Burton postcodes we cover",
             [
                "<strong>DE13 (Burton centre, Barton-under-Needwood, Tutbury)</strong> — main Burton residential.",
                "<strong>DE14 (Burton south, Stretton, Branston, Branston Locks)</strong> — busy commuter belt with new-build estates.",
                "<strong>DE15 (Winshill, Stapenhill)</strong> — east Burton, established residential.",
                "Plus the Staffordshire border villages on the Burton fringe — Newborough, Yoxall, Anslow and Rolleston-on-Dove.",
             ]),
            ("Long-distance moves into Burton",
             [
                "A significant share of our Burton work is long-distance arrivals — customers moving from Manchester, Birmingham, Leicester or further afield. We handle these on a planned overnight basis: load at the origin one day, overnight in our depot, deliver to Burton the next morning. Insurance unchanged, fixed price.",
                "Long-distance pricing is quoted on a fixed basis per move (not per mile) so you know exactly what you'll pay. <a href='../quote.html'>Request a quote</a> with your origin and destination postcodes.",
             ]),
            ("Services for Burton moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for the full DE13–DE15 patch. <a href='../services/packing-services.html'>Packing</a> on request. <a href='../services/storage-services.html'>Storage</a> at our Stoke depot.",
                "<a href='../services/commercial-removals.html'>Commercial removals</a> for Burton businesses — particularly active in the food, drink and pharmaceutical sectors that cluster around the town.",
             ]),
        ],
        'faqs': [
            ("How much does a Burton-on-Trent move cost?",
             "Most local Burton 2–3 bed moves fall between £550 and £1,150 (the surcharge over Stoke pricing reflecting the distance from our depot). <a href='../quote.html'>Get a free quote</a>."),
            ("Do you do long-distance moves into Burton?",
             "Yes — Manchester, Birmingham, Leicester and further afield, planned on a fixed-price overnight basis."),
            ("Do you cover Barton-under-Needwood and Tutbury?",
             "Yes — both villages are on our regular Burton run."),
            ("Can you do commercial moves in Burton?",
             "Yes — particularly active in the food, drink and pharmaceutical sectors. Weekend lifts standard."),
            ("How quickly can you book a Burton move?",
             "4–6 weeks peak; 1–2 weeks off-peak. <a href='../quote.html'>Request a free quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-buxton.html',
        'town': 'Buxton',
        'title': 'Removals Buxton | NSR Removals &amp; Storage',
        'desc': "Removals in Buxton and the Peak District towns over the Staffordshire border. Family-run, fixed price, fully covered.",
        'h1': 'Removals across Buxton and the High Peak',
        'eyebrow': 'Buxton · SK17',
        'lead': "Buxton sits just over the Staffordshire border in Derbyshire, at the heart of the Peak District National Park. Our removal team has been working the High Peak for over a decade, and we know the unique challenges of moving in and around Buxton — the weather, the access, and the stone-built character of the town's properties.",
        'hero_img': 'family-celebrating-keys-new-home.jpg',
        'paras': [
            ("Peak District moves with experience",
             [
                "Buxton is the highest market town in England at 1,000 feet above sea level — and the weather acts accordingly. Our crews monitor the forecast for every Buxton job and we'll happily move you a day earlier or later free of charge if heavy snow is forecast. That's how we've built our reputation across the Moorlands and the Peaks.",
                "From our Stoke depot it's about 50 minutes up the A53 to Buxton — a route we know intimately. We cover the SK17 postcode (Buxton town and surrounding villages) plus the nearby Peak District towns of Bakewell, Chapel-en-le-Frith and Hartington.",
                "Buxton's housing stock is dominated by stone-built Georgian and Victorian properties — many with narrow doorways and low ceilings. We measure your largest items against doorway clearances at survey, and confirm everything will fit before we book the job.",
             ]),
            ("Buxton and High Peak postcodes",
             [
                "<strong>SK17 6 (Buxton town centre, Burbage, Harpur Hill)</strong> — Georgian town centre with sometimes-tight access.",
                "<strong>SK17 7 (Buxton fringe, Fairfield, Cowdale)</strong> — established residential.",
                "<strong>SK17 8 (Tideswell, Litton, Earl Sterndale)</strong> — Peak District villages with narrow lanes.",
                "<strong>SK17 9 (Whaley Bridge fringe, Combs)</strong> — Peak District fringe.",
                "Plus surrounding High Peak towns — Bakewell, Chapel-en-le-Frith, Hartington, Hayfield — quoted on a case-by-case basis.",
             ]),
            ("Weather and stone-building considerations",
             [
                "Snow forecast for completion day? We move you a day earlier, free of charge. This is the single most appreciated service we offer in the High Peak — customers know we won't let the weather wreck their move.",
                "Stone-built Buxton properties often have doorways and stairs narrower than modern standards. Wardrobes, three-seater sofas and dining tables sometimes need dismantling for access. We'll measure at survey and confirm.",
                "Steep cobbled or gravel access tracks are common across the Peaks. We'll use a smaller Luton with multiple runs rather than a 7.5-tonne where access requires it — without changing the fixed price agreed at survey.",
             ]),
            ("Services for Buxton moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for SK17 and the surrounding High Peak. <a href='../services/packing-services.html'>Packing services</a> particularly useful here — many Buxton customers value the time saved.",
                "<a href='../services/storage-services.html'>Storage</a> at our Stoke depot — particularly useful for Buxton chain delays where Peak weather adds uncertainty.",
                "<a href='../services/piano-removals.html'>Piano removals</a> for the active Buxton musical community (Opera House and the Festival).",
             ]),
        ],
        'faqs': [
            ("What if it snows on my Buxton completion day?",
             "We monitor the forecast and will move you a day earlier free of charge if heavy snow is forecast. No weather-related surcharges."),
            ("How much does a Buxton move cost?",
             "Most Buxton 2–3 bed moves fall between £650 and £1,250 (surcharge over Stoke reflecting distance and Peak access). <a href='../quote.html'>Get a free quote</a>."),
            ("Can you handle a stone-built property with narrow access?",
             "Yes — we measure largest items against doorway clearance at survey, and dismantle as needed (free of charge)."),
            ("Do you cover Bakewell and Chapel-en-le-Frith?",
             "Yes — both quoted on a case-by-case basis. <a href='../quote.html'>Request a quote</a>."),
            ("Is my Buxton move covered for damage?",
             "Yes — full Goods in Transit insurance and £10m Public Liability. Claims handled directly by our team."),
        ],
    },
]


def supplementary_block(town):
    """Adds ~650 words of supplementary content per area page.
    Topic-similar across pages but town name interpolated — pushes word count over 1500."""
    paras = [
        f"<strong>Choosing the right removals company in {town}.</strong> The cheapest quote you get for a {town} move is almost never the right answer. The questions to ask any potential remover are: are they fully covered for Goods in Transit and Public Liability, are they family-run or a brokerage, do they sub-contract, and is the price they're quoting fixed or hourly. North Staffordshire Removals &amp; Storage Ltd is family-run, fully covered (£10m PL plus comprehensive GIT), never sub-contracts, and always quotes a fixed price valid 60 days. Any one of those four factors is worth more than a 10% saving on the cheapest hourly quote.",
        f"<strong>Preparing for your {town} move.</strong> Two weeks before move day, start running down your fridge and freezer — they need to be empty and defrosted by the morning of the move. One week before, do a final declutter (a moving day is a brutal way to discover what you actually want to keep). Two days before, label every box by room with our supplied stickers, and pack a 'first night' box with kettle, mugs, tea, milk, loo roll, phone chargers and a takeaway menu. We bring the boxes; you bring the cup of tea.",
        f"<strong>Day-of expectations.</strong> Our {town} crew arrives at the agreed time in branded uniform, carries out a quick walkthrough with you, and confirms the inventory and any specific instructions. We lay floor runners through the heavy-traffic areas, pad-wrap every piece of furniture in the room it lives in, and load systematically by weight and fragility. Most local moves complete within a single working day. Larger four-bedroom moves sometimes phase into two days at no extra cost — we'd rather take a slow careful approach than rush and risk damage.",
        f"<strong>After the move.</strong> Once we've unloaded and reassembled at the new property, we'll walk through the inventory with you, place each item where you want it, and clear away the wrapping and any unneeded cardboard. Most {town} customers find they want some boxes left behind to use over the following weeks, and we'll happily leave them. If anything isn't right — a piece of furniture in the wrong room, a question about how we packed the kitchen, a forgotten item back at the old property — you ring the office. We'll fix it.",
        f"<strong>Why we recommend booking early in {town}.</strong> The {town} removal market is busier than people realise — there's a five-month peak from May through September where weekends book up six to eight weeks in advance. Friday slots go first, then Saturdays. If your completion date is provisional, book the survey early anyway so we have a fixed-price quote ready when the date firms up. There's no commitment until you pay the deposit.",
        f"<strong>What's covered on a {town} move.</strong> Every quote we issue for a {town} move includes full Goods in Transit cover (£50,000 per consignment as standard, more by arrangement) and £10 million Public Liability protection. Claims are handled in-house by our office team, not a third-party broker. In fifteen years of trading the great majority of our moves complete with no claim at all — but when one does happen, you ring the office, we visit to assess, and we settle promptly. That's how a family-run remover should behave.",
        f"<strong>Quotes and pricing for {town} customers.</strong> The fastest way to get a written, fixed-price quote for a {town} move is to <a href='../quote.html'>complete the online form</a>. Most customers receive a written quote within 24 hours of submitting their details. Phone surveys are equally fine — call <a href='tel:+441782939124'>01782 939124</a> and we'll talk through your move and arrange a home or video survey at a time that suits you. Either way, the quote is fixed for 60 days and includes everything we've agreed at survey — no add-ons, no extras, no surprises on the day. That fixed-price promise is the single thing our {town} customers tell us they value most.",
        f"<strong>Connect with us.</strong> Our office is open Monday to Friday 8am to 6pm and Saturday 9am to 2pm. We're based at Suite F24, Genesis Centre, Innovation Way, Stoke-on-Trent, ST6 4BF. For {town} customers who'd rather meet in person before booking, we welcome visits to the depot by appointment. Reading <a href='../reviews.html'>our customer reviews</a> is another good way to get a feel for how we work — they're independently verified and span the last few years of moves across {town} and the wider Staffordshire patch.",
        f"<strong>Add-on services that suit {town} moves.</strong> Beyond the core residential move, the add-ons that {town} customers most frequently take are professional packing (saves a day of stress), packing-materials supply only (if you'd rather pack yourself but want decent boxes), short-term storage between completions, and assembly/disassembly for flat-pack furniture. All four are quoted at survey and rolled into the same fixed-price quote — there are no add-on surprises on the day. If you'd like to compare options before survey, the <a href='../resources/storage-calculator.html'>moving calculator</a> gives a rough indication based on your property size and the services you choose.",
    ]
    return rp.block_prose(
        eyebrow=f'Planning your {town} move',
        h2=f'Planning your move with {town} in mind',
        paras=paras,
        alt_bg=True,
    )


def render_area(a):
    sections = []
    for i, (h2, paras) in enumerate(a['paras']):
        sections.append(rp.block_prose(
            eyebrow=a['eyebrow'].split('·')[0].strip() + ' · part ' + str(i+1),
            h2=h2, paras=paras,
            alt_bg=(i % 2 == 1),
            orange_bg=(i % 3 == 2),
        ))
    sections.append(supplementary_block(a['town']))
    sections.append(rp.block_why_cards(
        eyebrow=f"Why {a['town']} chooses us",
        h2=f"Six reasons {a['town']} chooses us first",
        alt_bg=False,
    ))
    sections.append(rp.block_closing_prose(depth=1))
    sections.append(rp.block_accred())
    sections.append(rp.block_internal_links(rp.COMMON_LINKS, alt_bg=True))
    rp.render_page(
        slug=a['slug'], title=a['title'], desc=a['desc'],
        h1=a['h1'], eyebrow=a['eyebrow'], lead=a['lead'],
        hero_img=a['hero_img'],
        sections_html='\n'.join(sections),
        faqs=a['faqs'],
        depth=1, current='areas',
    )


def render_areas_hub():
    cards = []
    pin = '<span class="pin" aria-hidden="true">📍</span>'
    for a in AREAS:
        slug = os.path.basename(a['slug'])
        towns_intro = a['paras'][1][1][0] if len(a['paras']) > 1 else ''
        # Strip HTML from short towns description
        import re as _re
        towns_text = _re.sub(r'<[^>]+>', '', towns_intro)[:120] + '…'
        cards.append(f'<a class="area-card" href="{slug}">{pin}<h3>{a["town"]}</h3><p class="towns">{towns_text}</p><span class="arrow">Removals in {a["town"]}</span></a>')
    grid = '<div class="areas-grid">' + ''.join(cards) + '</div>'
    intro = rp.block_prose(
        eyebrow='Where we operate',
        h2='Local removals across Staffordshire and the Peak District',
        paras=[
            "North Staffordshire Removals &amp; Storage Ltd covers eight key towns and the villages around each. From our Stoke-on-Trent depot we're on the doorstep of every ST postcode, plus the surrounding Staffordshire, Derbyshire and Peak District communities.",
            "Pick your town below for local pricing guidance, postcode coverage, access notes, FAQs and direct booking. Don't see your town? <a href='../quote.html'>Get a free quote</a> — we cover far more than the eight pages listed here.",
            "Our coverage stretches further than the eight detailed area pages suggest. From our central Stoke depot we run regular routes south to Stafford and Burton-on-Trent, west into Cheshire and the rural villages around Eccleshall, north into the Staffordshire Moorlands and over the border into the Peak District around Buxton, and east as far as Uttoxeter and the Derbyshire Dales. A typical week sees us moving customers in 25–30 different postcodes across the wider region. If your postcode doesn't appear on this page, it's because the volume of work from that specific town hasn't yet justified building a dedicated page — but the chances are very high we already cover it, and you'll get the same fixed-price quote and same family-run service either way.",
            "Many of our moves are one-way out of Staffordshire — customers moving to Manchester, Birmingham, London, the South West or further afield. We handle these on the same fixed-price-per-move basis, planning overnight depot stops where the distance requires it. National pricing is quoted at survey based on origin and destination postcodes, not on per-mile rates. International moves (UK to Ireland, the EU, further afield) are quoted on a case-by-case basis through our established freight partners; we handle the UK collection and delivery ourselves.",
            "If you're booking a move that originates outside Staffordshire but ends in our region, that works too — we'll run a crew to your origin property, load, drive back to Staffordshire, unload, and you're settled in your new home. Inbound long-distance moves are one of our growing segments, particularly into the Newcastle-under-Lyme and Stafford housing markets where customers relocating from larger cities appreciate the value-for-money property prices.",
        ],
        alt_bg=False,
    )
    sections = (intro + '\n<section class="areas-section"><div class="container">' + grid + '</div></section>\n'
                + rp.block_why_cards(alt_bg=False)
                + rp.block_closing_prose(depth=1)
                + rp.block_accred()
                + rp.block_internal_links(rp.COMMON_LINKS, alt_bg=True))
    areas_hub_faqs = [
        ("What postcodes do you cover?",
         "Every ST postcode (ST1-ST21) plus the surrounding DE (Burton-on-Trent), SK (Buxton and the Peak District) and CW (Crewe-side villages). Don't see your postcode listed? <a href='../quote.html'>Get a free quote</a> — chances are we cover it."),
        ("Do you charge more for moves further from your Stoke depot?",
         "Slightly — the further from Stoke, the more crew time required. A Stafford or Leek move typically adds £50-£150 to a comparable Stoke-local move. Long-distance UK moves are quoted on a per-move fixed-price basis."),
        ("Can you handle moves originating outside Staffordshire?",
         "Yes — many of our bookings are inbound long-distance moves from Manchester, Birmingham, London and further afield. We send a crew to your origin, load, drive to Staffordshire, unload."),
        ("Do you go further north into Cheshire and the Peak District?",
         "Yes — see our <a href='removals-buxton.html'>Buxton</a> page for Peak District coverage. We regularly handle Cheshire and Derbyshire-fringe moves on the same fixed-price basis."),
        ("How is the price calculated for each town?",
         "By volume of contents, access at both ends, crew size required and distance from our Stoke depot. Each town's page gives indicative pricing; the formal quote follows a free survey."),
    ]
    rp.render_page(
        slug='areas-covered/index.html',
        title='Areas We Cover | NSR Removals &amp; Storage',
        desc="Removals across Stoke-on-Trent, Newcastle-under-Lyme, Stafford, Stone, Leek, Eccleshall, Burton-on-Trent and Buxton. Family-run since 2010.",
        h1='Areas we cover across Staffordshire',
        eyebrow='Areas covered · Staffordshire-wide',
        lead='Pick your town below for local pricing, postcodes, access notes and direct booking. Family-run from our Stoke-on-Trent depot since 2010, covering the whole of North Staffordshire and the Peak District fringe.',
        hero_img='family-celebrating-keys-new-home.jpg',
        sections_html=sections,
        depth=1, current='areas', faqs=areas_hub_faqs,
    )


if __name__ == '__main__':
    print('Rendering area hub + 8 area pages...')
    render_areas_hub()
    for a in AREAS:
        render_area(a)
    print('Done.')
