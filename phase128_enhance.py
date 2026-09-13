"""Strengthen the existing English services hub with user-centred links to existing concierge models.

The current production services hub already links four specialist intent pages, but
its visible bridge is framed around how clients search and omits the existing
Personal Concierge and Luxury Travel Concierge routes. This phase keeps the same
canonical URL and replaces only that bridge with contextual, descriptive links
covering all six existing service-model pages.
"""
from pathlib import Path
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
PAGE = ROOT / 'services' / 'index.html'
SITEMAP = ROOT / 'sitemap.xml'
URL = BASE + '/services/'
LASTMOD = '2026-09-13'

NEW_SECTION = '''<section class="partners-strip ivm-intent-cluster"><div><div class="kicker dark">Choose the right service model</div><h2>Start with the support that matches the brief.</h2><p>For direct personal assistance and day-to-day requests, use <a class="text-link" href="/personal-concierge-ibiza/">Personal Concierge</a>. For pre-arrival trip planning connected to local execution, use <a class="text-link" href="/luxury-travel-concierge-ibiza/">Luxury Travel Concierge</a>.</p><p>For ongoing stay coordination, see <a class="text-link" href="/luxury-lifestyle-management-ibiza/">Lifestyle Management</a>. For hospitality and access requests, see <a class="text-link" href="/vip-services-ibiza/">VIP Services</a>. Principals and representatives can use <a class="text-link" href="/private-client-services-ibiza/">Private Client Services</a>; professional travel partners can use <a class="text-link" href="/destination-management-ibiza/">Luxury DMC &amp; Destination Management</a>.</p></div><a class="btn dark" href="/contact/">Private brief</a></section>'''


def enhance():
    if not PAGE.is_file():
        raise SystemExit('Phase 128 services page missing')
    html = PAGE.read_text(encoding='utf-8')
    if html.count('class="partners-strip ivm-intent-cluster"') != 1:
        raise SystemExit('Phase 128 services intent-cluster cardinality drift')
    match = re.search(r'<section class="partners-strip ivm-intent-cluster">.*?</section>', html, re.S)
    if not match:
        raise SystemExit('Phase 128 services intent cluster not found')
    old = match.group(0)
    if 'More ways clients search for this support' not in old:
        raise SystemExit('Phase 128 expected pre-change search-facing kicker missing')
    html = html[:match.start()] + NEW_SECTION + html[match.end():]
    PAGE.write_text(html, encoding='utf-8')

    if not SITEMAP.is_file():
        raise SystemExit('Phase 128 sitemap missing')
    xml = SITEMAP.read_text(encoding='utf-8')
    loc = f'<loc>{URL}</loc>'
    if xml.count(loc) != 1:
        raise SystemExit(f'Phase 128 services sitemap URL cardinality drift: {xml.count(loc)}')
    pat = re.compile(rf'(<url><loc>{re.escape(URL)}</loc>)(?:<lastmod>[^<]+</lastmod>)?')
    xml2, count = pat.subn(rf'\1<lastmod>{LASTMOD}</lastmod>', xml, count=1)
    if count != 1:
        raise SystemExit('Phase 128 could not update services lastmod')
    SITEMAP.write_text(xml2, encoding='utf-8')
    print('PASS: Phase 128 added contextual links to all six existing concierge service models from /services/ and refreshed only that page lastmod')


if __name__ == '__main__':
    enhance()
