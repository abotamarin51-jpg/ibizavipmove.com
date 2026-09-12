"""Refresh sitemap lastmod only for pages with verified significant changes on 2026-09-12."""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
LASTMOD = '2026-09-12'
VERIFIED = {
    '/contact/', '/es/contacto/', '/fr/contact/', '/de/kontakt/', '/ar/contact/',
    '/fr/partners/', '/de/partners/', '/ar/partners/',
    '/fr/clients-internationaux/', '/de/internationale-kunden/', '/ar/international-clients/',
    '/fr/private-office/', '/de/private-office/', '/ar/private-office/',
}
ET.register_namespace('', NS)


def enhance():
    sitemap = ROOT / 'sitemap.xml'
    if not sitemap.is_file():
        raise SystemExit('Phase 121 sitemap missing')
    tree = ET.parse(sitemap)
    root = tree.getroot()
    seen = set()
    changed = 0
    for url in root.findall(f'{{{NS}}}url'):
        loc = url.find(f'{{{NS}}}loc')
        if loc is None or not loc.text:
            continue
        canonical = loc.text.rstrip('/') + '/'
        path = canonical[len(BASE):] if canonical.startswith(BASE) else None
        if path not in VERIFIED:
            continue
        seen.add(path)
        lastmod = url.find(f'{{{NS}}}lastmod')
        if lastmod is None:
            lastmod = ET.Element(f'{{{NS}}}lastmod')
            url.insert(1, lastmod)
        if lastmod.text != LASTMOD:
            lastmod.text = LASTMOD
            changed += 1
    missing = VERIFIED - seen
    if missing:
        raise SystemExit(f'Phase 121 verified sitemap targets missing: {sorted(missing)}')
    tree.write(sitemap, encoding='utf-8', xml_declaration=True)
    print(f'PASS: Phase 121 sitemap freshness — {len(VERIFIED)} verified significantly changed URLs carry accurate lastmod={LASTMOD}; {changed} metadata value(s) refreshed')


if __name__ == '__main__':
    enhance()
