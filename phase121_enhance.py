"""Refresh sitemap lastmod only for pages with verified significant changes."""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
VERIFIED = {
    '/contact/': '2026-09-12', '/es/contacto/': '2026-09-12', '/fr/contact/': '2026-09-12',
    '/de/kontakt/': '2026-09-12', '/ar/contact/': '2026-09-12',
    '/fr/partners/': '2026-09-12', '/de/partners/': '2026-09-12', '/ar/partners/': '2026-09-12',
    '/fr/clients-internationaux/': '2026-09-12', '/de/internationale-kunden/': '2026-09-12',
    '/ar/international-clients/': '2026-09-12',
    '/private-office/': '2026-10-21',
    '/fr/private-office/': '2026-09-12', '/de/private-office/': '2026-09-12', '/ar/private-office/': '2026-09-12',
    '/destination-management-ibiza/': '2026-10-18',
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
        target_lastmod = VERIFIED.get(path)
        if target_lastmod is None:
            continue
        seen.add(path)
        lastmod = url.find(f'{{{NS}}}lastmod')
        if lastmod is None:
            lastmod = ET.Element(f'{{{NS}}}lastmod')
            url.insert(1, lastmod)
        if lastmod.text != target_lastmod:
            lastmod.text = target_lastmod
            changed += 1
    missing = set(VERIFIED) - seen
    if missing:
        raise SystemExit(f'Phase 121 verified sitemap targets missing: {sorted(missing)}')
    tree.write(sitemap, encoding='utf-8', xml_declaration=True)
    print(f'PASS: Phase 121 sitemap freshness — {len(VERIFIED)} verified significantly changed URLs carry accurate lastmod values; {changed} metadata value(s) refreshed')


if __name__ == '__main__':
    enhance()
