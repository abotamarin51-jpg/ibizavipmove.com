"""Read-only gate for verified sitemap lastmod freshness signals."""
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


def run():
    tree = ET.parse(ROOT / 'sitemap.xml')
    values = {}
    for url in tree.getroot().findall(f'{{{NS}}}url'):
        loc = url.findtext(f'{{{NS}}}loc')
        if not loc:
            continue
        values[loc.rstrip('/') + '/'] = url.findtext(f'{{{NS}}}lastmod')
    for path in VERIFIED:
        canonical = BASE + path
        if canonical not in values:
            raise SystemExit(f'Phase 121 sitemap URL missing: {path}')
        if values[canonical] != LASTMOD:
            raise SystemExit(f'Phase 121 inaccurate lastmod: {path} -> {values[canonical]!r}')
    if len(values) != 156:
        raise SystemExit(f'Phase 121 sitemap inventory drift: {len(values)} URLs')
    print(f'PASS: Phase 121 audit — {len(VERIFIED)} verified 12 September page changes expose lastmod={LASTMOD}; sitemap inventory remains {len(values)} canonical URLs')


if __name__ == '__main__':
    run()
