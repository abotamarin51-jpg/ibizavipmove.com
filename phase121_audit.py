"""Read-only gate for verified sitemap lastmod freshness signals."""
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


def run():
    tree = ET.parse(ROOT / 'sitemap.xml')
    values = {}
    for url in tree.getroot().findall(f'{{{NS}}}url'):
        loc = url.findtext(f'{{{NS}}}loc')
        if not loc:
            continue
        values[loc.rstrip('/') + '/'] = url.findtext(f'{{{NS}}}lastmod')
    for path, expected_lastmod in VERIFIED.items():
        canonical = BASE + path
        if canonical not in values:
            raise SystemExit(f'Phase 121 sitemap URL missing: {path}')
        if values[canonical] != expected_lastmod:
            raise SystemExit(f'Phase 121 inaccurate lastmod: {path} -> {values[canonical]!r}, expected {expected_lastmod}')
    if len(values) != 156:
        raise SystemExit(f'Phase 121 sitemap inventory drift: {len(values)} URLs')
    print(f'PASS: Phase 121 audit — {len(VERIFIED)} verified page changes expose accurate lastmod values; sitemap inventory remains {len(values)} canonical URLs')


if __name__ == '__main__':
    run()
