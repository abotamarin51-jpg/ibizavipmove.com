"""Identify the English service catalogue separately from full-stay concierge.

The catalogue title and description are set in postprocess_site.py. Match its
visible heading to that role and update only its existing sitemap date. Keep
the service inventory, navigation, imagery and contact routes unchanged.
"""
from pathlib import Path
import re

ROOT = Path('_site')
PAGE = ROOT / 'services' / 'index.html'
SITEMAP = ROOT / 'sitemap.xml'
UPDATED = '2026-11-04'
OLD = '<h1>One private ecosystem.<br>Every moving part connected.</h1>'
NEW = '<h1>Private services in Ibiza,<br>connected through one trusted contact.</h1>'


def enhance():
    if not PAGE.is_file():
        raise SystemExit('Phase 132 services page missing')
    html = PAGE.read_text(encoding='utf-8')

    if NEW in html and OLD not in html:
        if html.count(NEW) != 1:
            raise SystemExit(f'Phase 132 enhanced H1 cardinality drift: {html.count(NEW)}')
    elif html.count(OLD) == 1 and NEW not in html:
        html = html.replace(OLD, NEW, 1)
    else:
        raise SystemExit(f'Phase 132 expected one original services H1: {html.count(OLD)}')

    sitemap = SITEMAP.read_text(encoding='utf-8')
    pattern = r'(<url>\s*<loc>https://ibizavipmove\.com/services/</loc>\s*<lastmod>)[^<]+(</lastmod>)'
    sitemap, count = re.subn(pattern, lambda m: m.group(1) + UPDATED + m.group(2), sitemap)
    if count != 1:
        raise SystemExit('Phase 132 expected one existing Services sitemap entry')

    PAGE.write_text(html, encoding='utf-8')
    SITEMAP.write_text(sitemap, encoding='utf-8')
    print('PASS: Phase 132 — private-services catalogue heading and matching sitemap freshness')


if __name__ == '__main__':
    enhance()
