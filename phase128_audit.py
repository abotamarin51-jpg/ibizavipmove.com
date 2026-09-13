"""Regression checks for the Phase 128 services-hub service-model bridge."""
from pathlib import Path
from html import unescape
import re
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
URL = BASE + '/services/'
PAGE = ROOT / 'services' / 'index.html'
SITEMAP = ROOT / 'sitemap.xml'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
LASTMOD = '2026-09-13'
PATHS = {
    '/personal-concierge-ibiza/': 'Personal Concierge',
    '/luxury-travel-concierge-ibiza/': 'Luxury Travel Concierge',
    '/luxury-lifestyle-management-ibiza/': 'Lifestyle Management',
    '/vip-services-ibiza/': 'VIP Services',
    '/private-client-services-ibiza/': 'Private Client Services',
    '/destination-management-ibiza/': 'Luxury DMC &amp; Destination Management',
}


def run():
    if not PAGE.is_file():
        raise SystemExit('Phase 128 services page missing')
    html = PAGE.read_text(encoding='utf-8')
    if html.count('class="partners-strip ivm-intent-cluster"') != 1:
        raise SystemExit('Phase 128 services intent-cluster cardinality drift')
    match = re.search(r'<section class="partners-strip ivm-intent-cluster">.*?</section>', html, re.S)
    if not match:
        raise SystemExit('Phase 128 services intent cluster missing')
    section = match.group(0)
    if 'More ways clients search for this support' in section:
        raise SystemExit('Phase 128 search-facing kicker remains')
    if 'Choose the right service model' not in section or 'Start with the support that matches the brief.' not in section:
        raise SystemExit('Phase 128 user-centred bridge copy missing')
    for href, label in PATHS.items():
        marker = f'href="{href}">{label}</a>'
        if marker not in section:
            raise SystemExit(f'Phase 128 contextual pathway missing: {href}')
        target = ROOT / href.strip('/') / 'index.html'
        if not target.is_file():
            raise SystemExit(f'Phase 128 linked target missing from build: {href}')
        target_html = target.read_text(encoding='utf-8')
        if 'noindex' in target_html.lower():
            raise SystemExit(f'Phase 128 linked target unexpectedly noindex: {href}')
    visible = unescape(re.sub(r'<[^>]+>', ' ', section)).lower()
    for phrase in ('direct personal assistance', 'pre-arrival trip planning', 'ongoing stay coordination', 'professional travel partners'):
        if phrase not in visible:
            raise SystemExit(f'Phase 128 contextual copy missing: {phrase}')
    if f'<link rel="canonical" href="{URL}">' not in html:
        raise SystemExit('Phase 128 services canonical drift')
    if 'noindex' in html.lower():
        raise SystemExit('Phase 128 services page unexpectedly noindex')
    if len(re.findall(r'<h1\b', html, re.I)) != 1:
        raise SystemExit('Phase 128 services H1 cardinality drift')

    tree = ET.parse(SITEMAP)
    root = tree.getroot()
    urls = root.findall(f'{{{NS}}}url')
    locs = []
    target_lastmod = None
    for node in urls:
        loc = node.find(f'{{{NS}}}loc')
        if loc is None or not loc.text:
            continue
        locs.append(loc.text)
        if loc.text == URL:
            lm = node.find(f'{{{NS}}}lastmod')
            target_lastmod = lm.text if lm is not None else None
    if len(locs) != 156 or len(set(locs)) != 156:
        raise SystemExit(f'Phase 128 sitemap inventory drift: total={len(locs)} unique={len(set(locs))}')
    if target_lastmod != LASTMOD:
        raise SystemExit(f'Phase 128 services lastmod mismatch: {target_lastmod}')

    print('PASS: Phase 128 audit — /services/ has one user-centred service-model bridge, six crawlable contextual pathways to existing indexable pages, unchanged canonical/H1, and 156 sitemap URLs')


if __name__ == '__main__':
    run()
