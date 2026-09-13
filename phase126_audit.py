"""Regression checks for Phase 126 Search Console-led luxury-car intent alignment."""
from pathlib import Path
from html import unescape
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
URL = BASE + '/luxury-car-rental-ibiza/'
PAGE = ROOT / 'luxury-car-rental-ibiza' / 'index.html'
SITEMAP = ROOT / 'sitemap.xml'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
LASTMOD = '2026-09-13'
TITLE = 'Luxury Car Hire & Rental Ibiza | Supercars | Ibiza VIP Move'
DESCRIPTION = (
    'Luxury car hire and rental in Ibiza, including executive cars, luxury SUVs, '
    'sports cars and supercars, with delivery coordinated to villas, hotels or marinas.'
)


def meta(html, attr, key):
    match = re.search(rf'<meta\s+{attr}="{re.escape(key)}"\s+content="([^"]*)"', html, re.I)
    return unescape(match.group(1)) if match else None


def parse_jsonld(html):
    values = []
    for match in re.finditer(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', html, re.I | re.S):
        try:
            values.append(json.loads(match.group(1).strip()))
        except json.JSONDecodeError as exc:
            raise SystemExit(f'Phase 126 invalid JSON-LD: {exc}')
    return values


def run():
    if not PAGE.is_file():
        raise SystemExit('Phase 126 luxury car page missing')
    html = PAGE.read_text(encoding='utf-8')

    title_match = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
    rendered_title = unescape(title_match.group(1)).strip() if title_match else None
    if rendered_title != TITLE:
        raise SystemExit(f'Phase 126 title mismatch: {rendered_title!r}')
    if meta(html, 'name', 'description') != DESCRIPTION:
        raise SystemExit('Phase 126 description mismatch')
    if meta(html, 'property', 'og:title') != TITLE or meta(html, 'property', 'og:description') != DESCRIPTION:
        raise SystemExit('Phase 126 Open Graph mismatch')
    if meta(html, 'name', 'twitter:title') != TITLE or meta(html, 'name', 'twitter:description') != DESCRIPTION:
        raise SystemExit('Phase 126 Twitter metadata mismatch')
    if f'<link rel="canonical" href="{URL}">' not in html:
        raise SystemExit('Phase 126 canonical changed')
    if len(re.findall(r'<h1\b', html, re.I)) != 1:
        raise SystemExit('Phase 126 H1 cardinality drift')
    if 'Luxury Car Hire &amp; Rental' not in html and 'Luxury Car Hire & Rental' not in html:
        raise SystemExit('Phase 126 H1 wording missing')

    visible = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', html, flags=re.I | re.S)
    visible = unescape(re.sub(r'<[^>]+>', ' ', visible))
    visible = re.sub(r'\s+', ' ', visible).lower()
    for phrase in ('luxury car hire', 'luxury car rental', 'sports cars', 'supercars'):
        if phrase not in visible:
            raise SystemExit(f'Phase 126 visible intent missing: {phrase}')

    objects = parse_jsonld(html)
    webpage = [o for o in objects if isinstance(o, dict) and o.get('@type') == 'WebPage' and o.get('@id') == URL + '#webpage']
    service = [o for o in objects if isinstance(o, dict) and o.get('@type') == 'Service' and o.get('@id') == URL + '#service']
    if len(webpage) != 1 or len(service) != 1:
        raise SystemExit(f'Phase 126 JSON-LD cardinality mismatch: WebPage={len(webpage)} Service={len(service)}')
    if webpage[0].get('name') != 'Luxury Car Hire & Rental Ibiza' or webpage[0].get('description') != DESCRIPTION:
        raise SystemExit('Phase 126 WebPage schema mismatch')
    if service[0].get('name') != 'Luxury Car Hire & Rental':
        raise SystemExit('Phase 126 Service schema name mismatch')
    if service[0].get('serviceType') != 'Luxury car hire and rental coordination in Ibiza':
        raise SystemExit('Phase 126 Service schema type mismatch')
    if service[0].get('description') != DESCRIPTION:
        raise SystemExit('Phase 126 Service schema description mismatch')

    if not SITEMAP.is_file():
        raise SystemExit('Phase 126 sitemap missing')
    tree = ET.parse(SITEMAP)
    root = tree.getroot()
    urls = root.findall(f'{{{NS}}}url')
    locs = []
    target_lastmod = None
    for url in urls:
        loc = url.find(f'{{{NS}}}loc')
        if loc is None or not loc.text:
            continue
        locs.append(loc.text)
        if loc.text == URL:
            lm = url.find(f'{{{NS}}}lastmod')
            target_lastmod = lm.text if lm is not None else None
    if len(locs) != 156 or len(set(locs)) != 156:
        raise SystemExit(f'Phase 126 sitemap inventory drift: total={len(locs)} unique={len(set(locs))}')
    if target_lastmod != LASTMOD:
        raise SystemExit(f'Phase 126 sitemap lastmod mismatch: {target_lastmod}')

    print('PASS: Phase 126 audit — one existing luxury-car canonical covers verified hire/rental wording, aligned metadata/schema, truthful lastmod, and the 156-URL sitemap inventory is unchanged')


if __name__ == '__main__':
    run()
