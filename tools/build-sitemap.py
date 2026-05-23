#!/usr/bin/env python3
"""Rebuild /sitemap.xml from every indexable HTML page."""
from __future__ import annotations
import glob, os, re, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = 'https://www.northstaffordshireremovals.co.uk'

SECTIONS = [
    ('root',      ['*.html'],               '1.0', 'weekly'),
    ('services',  ['services/*.html'],      '0.8', 'monthly'),
    ('areas',     ['areas-covered/*.html'], '0.8', 'monthly'),
    ('resources', ['resources/*.html'],     '0.7', 'monthly'),
    ('blog',      ['blog/*.html'],          '0.6', 'monthly'),
]

def is_indexable(path: str) -> bool:
    try: html = open(path, encoding='utf-8').read(4096)
    except OSError: return False
    if 'http-equiv="refresh"' in html or 'window.location.replace' in html: return False
    m = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', html, re.I)
    if m and 'noindex' in m.group(1).lower(): return False
    return True

def loc_for(path: str) -> str:
    if path == 'index.html': return BASE + '/'
    if path.endswith('/index.html'): return BASE + '/' + path[:-len('index.html')]
    return BASE + '/' + path

def lastmod_for(path: str) -> str:
    return datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc).date().isoformat()

def main() -> int:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    total = 0
    for label, pats, prio, freq in SECTIONS:
        paths = sorted(p for pat in pats for p in glob.glob(pat) if os.path.isfile(p) and is_indexable(p))
        if paths: lines.append(f'  <!-- {label} ({len(paths)} URLs) -->')
        for p in paths:
            lines.extend([
                '  <url>',
                f'    <loc>{loc_for(p)}</loc>',
                f'    <lastmod>{lastmod_for(p)}</lastmod>',
                f'    <changefreq>{freq}</changefreq>',
                f'    <priority>{prio}</priority>',
                '  </url>',
            ])
            total += 1
    lines.append('</urlset>')
    open('sitemap.xml','w',encoding='utf-8').write('\n'.join(lines)+'\n')
    print(f'sitemap.xml written with {total} URLs')
    return 0

if __name__ == '__main__': sys.exit(main())
