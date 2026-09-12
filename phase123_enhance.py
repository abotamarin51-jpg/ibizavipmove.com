"""Consolidate duplicate operational-evidence blocks on the English B2B Partners page."""
from pathlib import Path
import re

ROOT = Path('_site')
PARTNERS = ROOT / 'partners' / 'index.html'
SITEMAP = ROOT / 'sitemap.xml'
URL = 'https://ibizavipmove.com/partners/'
LASTMOD = '2026-09-12'


def enhance():
    if not PARTNERS.is_file() or not SITEMAP.is_file():
        raise SystemExit('Phase 123 required production files missing')
    html = PARTNERS.read_text(encoding='utf-8')
    if html.count('ivm-phase104-authority') != 1:
        raise SystemExit(f'Phase 123 expected one legacy authority block, found {html.count("ivm-phase104-authority")}')
    if html.count('ivm-phase105-proof') != 1:
        raise SystemExit(f'Phase 123 expected one retained evidence block, found {html.count("ivm-phase105-proof")}')
    proof = re.search(r'<section class="partners-strip ivm-phase105-proof".*?</section>', html, re.S)
    if not proof:
        raise SystemExit('Phase 123 retained evidence block malformed')
    for href in ('/case-studies/', '/ibiza-luxury-operations-report-2026/', '/founder/'):
        if f'href="{href}"' not in proof.group(0):
            raise SystemExit(f'Phase 123 retained evidence link missing: {href}')
    legacy = re.findall(r'<section class="editorial ivm-phase104-authority">.*?</section>', html, re.S)
    if len(legacy) != 1:
        raise SystemExit(f'Phase 123 legacy block match mismatch: {len(legacy)}')
    updated_html = html.replace(legacy[0], '', 1)

    sitemap = SITEMAP.read_text(encoding='utf-8')
    pattern = r'(<loc>' + re.escape(URL) + r'</loc>\s*<lastmod>)([^<]+)(</lastmod>)'
    match = re.search(pattern, sitemap)
    if not match:
        raise SystemExit('Phase 123 partners lastmod entry missing')
    updated_sitemap = re.sub(pattern, r'\g<1>' + LASTMOD + r'\g<3>', sitemap, count=1)

    PARTNERS.write_text(updated_html, encoding='utf-8')
    SITEMAP.write_text(updated_sitemap, encoding='utf-8')
    print('PASS: Phase 123 — duplicate Partners authority block removed; one operational-evidence section retained with case studies/report/founder links; partners lastmod refreshed truthfully')


if __name__ == '__main__':
    enhance()
