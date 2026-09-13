"""Restore one evidence-backed legacy private-jet URL as a direct alias to the current aviation canonical.

The owner-provided Search Console export shows Google still knows the historical
/services/private-jets URL. The current static build already keeps equivalent
legacy service aliases as noindex redirect stubs, but this path is absent.

GitHub Pages does not expose per-path server redirect rules in this repository,
so this uses the site's existing client-side fallback pattern and points directly
to the final canonical destination. The alias is intentionally excluded from the
XML sitemap and carries no standalone indexable content.
"""
from pathlib import Path

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
LEGACY = ROOT / 'services' / 'private-jets' / 'index.html'
TARGET = BASE + '/private-aviation-ibiza/'

HTML = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ibiza VIP Move</title><meta name="robots" content="noindex,follow"><link rel="canonical" href="{TARGET}"><meta http-equiv="refresh" content="0;url={TARGET}"><script>location.replace('{TARGET}');</script><link rel="stylesheet" href="/assets/phase35.css?v=35"></head><body><a class="ivm-skip-link" href="#main-content">Skip to content</a><main id="main-content"><p>This page has moved to <a href="{TARGET}">{TARGET}</a>.</p></main></body></html>'''


def enhance():
    canonical = ROOT / 'private-aviation-ibiza' / 'index.html'
    sitemap = ROOT / 'sitemap.xml'
    if not canonical.is_file():
        raise SystemExit('Phase 127 canonical private-aviation page missing')
    if not sitemap.is_file():
        raise SystemExit('Phase 127 sitemap missing')

    canonical_html = canonical.read_text(encoding='utf-8')
    if f'<link rel="canonical" href="{TARGET}">' not in canonical_html:
        raise SystemExit('Phase 127 canonical private-aviation target drift')
    if 'noindex' in canonical_html.lower():
        raise SystemExit('Phase 127 canonical private-aviation page unexpectedly noindex')

    LEGACY.parent.mkdir(parents=True, exist_ok=True)
    LEGACY.write_text(HTML, encoding='utf-8')
    print('PASS: Phase 127 restored /services/private-jets/ as a noindex direct legacy alias to /private-aviation-ibiza/ without adding a duplicate sitemap URL')


if __name__ == '__main__':
    enhance()
