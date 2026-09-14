"""Phase 153: strengthen French bespoke-concierge discovery from the French Home page.

The French bespoke concierge page is a real existing service URL that GSC currently reports as
Discovered - currently not indexed, while EN/DE/AR equivalents are indexed. Wrap only the
existing French Home words "demandes sur mesure" with a same-language link to that page.
No visible copy, URL, schema, form, tracking, price, policy or sitemap change.
"""
from pathlib import Path
import re

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
SOURCE = 'fr'
DEST = '/fr/conciergerie-sur-mesure-ibiza/'
LABEL = 'demandes sur mesure'
MARKER = 'data-ivm153="bespoke"'
STYLE = 'text-decoration:underline;text-underline-offset:.15em'


def enhance(root: Path = ROOT) -> None:
    sitemap = (root / 'sitemap.xml').read_bytes()
    source = root / SOURCE / 'index.html'
    target = root / DEST.strip('/') / 'index.html'
    if not source.is_file() or not target.is_file() or (BASE + DEST).encode() not in sitemap:
        raise SystemExit('Phase 153: missing reviewed French source or destination')

    html = source.read_text(encoding='utf-8')
    linked = f'<a {MARKER} href="{DEST}" style="{STYLE}">{LABEL}</a>'
    if MARKER in html:
        if html.count(MARKER) != 1 or html.count(linked) != 1:
            raise SystemExit('Phase 153: malformed existing French bespoke link')
        return
    if re.search(r'href=[\"\']' + re.escape(DEST) + r'[\"\']', html):
        raise SystemExit('Phase 153: French bespoke destination already linked from Home')
    if html.count(LABEL) != 1:
        raise SystemExit(f'Phase 153: expected one existing French bespoke phrase, found {html.count(LABEL)}')

    updated = html.replace(LABEL, linked, 1)
    source.write_text(updated, encoding='utf-8')
    if (root / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 153: sitemap changed unexpectedly')
    print('PASS: Phase 153 — French Home links existing “demandes sur mesure” wording to the existing bespoke concierge page; no visible copy or URL change')


if __name__ == '__main__':
    enhance()
