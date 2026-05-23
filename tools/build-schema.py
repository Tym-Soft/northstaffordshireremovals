#!/usr/bin/env python3
"""Inject the canonical NSR Organization JSON-LD into every indexable page.
Idempotent — wraps the block with sentinel comments and rewrites on every run."""
from __future__ import annotations
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = 'https://www.northstaffordshireremovals.co.uk'
ORG_ID = BASE + '/#organization'

ORG = {
  "@context": "https://schema.org",
  "@type": ["LocalBusiness","MovingCompany"],
  "@id": ORG_ID,
  "name": "North Staffordshire Removals & Storage Ltd",
  "alternateName": "North Staffordshire Removals",
  "legalName": "North Staffordshire Removals & Storage Ltd",
  "url": BASE + "/",
  "logo": BASE + "/images/logo-north-staffordshire-removals.png",
  "image": BASE + "/images/family-celebrating-keys-new-home.jpg",
  "telephone": "+441782939124",
  "email": "enquiries@northstaffordshireremovals.co.uk",
  "foundingDate": "2010",
  "priceRange": "££",
  "currenciesAccepted": "GBP",
  "paymentAccepted": "Cash, Credit Card, Bank Transfer",
  "slogan": "Staffordshire's leading home and business removals and storage company",
  "address": {"@type":"PostalAddress","streetAddress":"Suite F24, Genesis Centre, Innovation Way",
              "addressLocality":"Stoke-on-Trent","addressRegion":"Staffordshire",
              "postalCode":"ST6 4BF","addressCountry":"GB"},
  "geo": {"@type":"GeoCoordinates","latitude":53.0566,"longitude":-2.1858},
  "openingHoursSpecification": [
    {"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"18:00"},
    {"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"09:00","closes":"14:00"},
  ],
  "areaServed": [
    {"@type":"AdministrativeArea","name":"Staffordshire"},
    {"@type":"City","name":"Stoke-on-Trent"},
    {"@type":"City","name":"Newcastle-under-Lyme"},
    {"@type":"City","name":"Stafford"},{"@type":"City","name":"Stone"},
    {"@type":"City","name":"Leek"},{"@type":"City","name":"Eccleshall"},
    {"@type":"City","name":"Burton-on-Trent"},{"@type":"City","name":"Buxton"},
  ],
  "knowsAbout": ["Residential removals","Commercial removals","Packing services",
                 "Self storage","Piano moving","Long distance removals"],
}
RATING = {"@type":"AggregateRating","ratingValue":"4.9","reviewCount":"187","bestRating":"5","worstRating":"1"}

RATING_PAGES = {'index.html', 'reviews.html'}
SENTINEL_RE = re.compile(r'<!-- nsr-schema:org:start -->.*?<!-- nsr-schema:org:end -->', re.S)

def is_indexable(path: str) -> bool:
    try: h = open(path, encoding='utf-8').read(4096)
    except OSError: return False
    if 'http-equiv="refresh"' in h: return False
    m = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', h, re.I)
    return not (m and 'noindex' in m.group(1).lower())

def main() -> int:
    paths = (glob.glob('*.html') + glob.glob('services/*.html')
             + glob.glob('areas-covered/*.html') + glob.glob('blog/*.html')
             + glob.glob('resources/*.html'))
    paths = sorted(p for p in paths if os.path.isfile(p) and is_indexable(p))
    n = 0
    for p in paths:
        html = open(p, encoding='utf-8').read()
        org = dict(ORG)
        if p in RATING_PAGES:
            org['aggregateRating'] = RATING
        block = '<!-- nsr-schema:org:start -->\n  <script type="application/ld+json">' + json.dumps(org, separators=(',',':')) + '</script>\n  <!-- nsr-schema:org:end -->'
        if SENTINEL_RE.search(html):
            new_html = SENTINEL_RE.sub(lambda m: block, html)
        else:
            # inject just before </head>
            new_html = html.replace('</head>', '  ' + block + '\n</head>', 1)
        if new_html != html:
            open(p,'w',encoding='utf-8').write(new_html)
            n += 1
    print(f'Schema injected/updated in {n} pages')
    return 0

if __name__ == '__main__': sys.exit(main())
