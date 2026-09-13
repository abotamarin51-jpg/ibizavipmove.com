"""Regression checks for the evidence-backed /services/private-jets legacy alias."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
LEGACY_URL = BASE + '/services/private-jets/'
TARGET = BASE + '/private-aviation-ibiza/'
LEGACY = ROOT / 'services' / 'private-jets' / 'index.html'
CANONICAL = ROOT / 'private-aviation-ibiza' / 'index.html'
SITEMAP = ROOT / 'sitemap.xml'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'


def run():
    if not LEGACY.is_file():
        raise SystemExit('Phase 127 legacy private-jets alias missing')
    html = LEGACY.read_text(encoding='utf-8')

    required = [
        '<meta name="robots" content="noindex,follow">',
        f'<link rel="canonical" href="{TARGET}">',
        f'<meta http-equiv="refresh" content="0;url={TARGET}">',
        f"location.replace('{TARGET}')",
        f'<a href="{TARGET}">{TARGET}</a>',
        'id="main-content"',
        'class="ivm-skip-link"',
    ]
    for marker in required:
        if marker not in html:
            raise SystemExit(f'Phase 127 legacy alias marker missing: {marker}')
    if len(re.findall(r'<link\s+rel="canonical"', html, re.I)) != 1:
        raise SystemExit('Phase 127 legacy alias canonical cardinality drift')

    if not CANONICAL.is_file():
        raise SystemExit('Phase 127 canonical private-aviation page missing')
    canonical_html = CANONICAL.read_text(encoding='utf-8')
    if f'<link rel="canonical" href="{TARGET}">' not in canonical_html:
        raise SystemExit('Phase 127 target canonical drift')
    if 'noindex' in canonical_html.lower():
        raise SystemExit('Phase 127 target unexpectedly noindex')

    tree = ET.parse(SITEMAP)
    locs = [
        node.text for node in tree.getroot().findall(f'{{{NS}}}url/{{{NS}}}loc')
        if node.text
    ]
    if len(locs) != 156 or len(set(locs)) != 156:
        raise SystemExit(f'Phase 127 sitemap inventory drift: total={len(locs)} unique={len(set(locs))}')
    if TARGET not in locs:
        raise SystemExit('Phase 127 canonical private-aviation URL missing from sitemap')
    if LEGACY_URL in locs or (BASE + '/services/private-jets') in locs:
        raise SystemExit('Phase 127 legacy redirect URL must not enter sitemap')

    print('PASS: Phase 127 audit — legacy /services/private-jets/ resolves through a noindex direct alias to the indexable aviation canonical; sitemap stays at 156 canonical URLs')


if __name__ == '__main__':
    run()
