"""Phase 150: add contextual localized Home links to existing dining/nightlife services.

Wrap only the existing restaurants/beach clubs/nightlife wording on FR/DE/AR Home.
No visible copy, URL, schema, form, tracking, price, policy or sitemap change.
"""
from pathlib import Path

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
MARKER = 'data-ivm150="service"'
STYLE = 'text-decoration:underline;text-underline-offset:.15em'
PAGES = {
    'fr': ('restaurants, beach clubs, nightlife', '/fr/restaurants-nightlife-ibiza/'),
    'de': ('Restaurants, Beach Clubs, Nightlife', '/de/restaurants-nightlife-ibiza/'),
    'ar': ('مطاعم ونوادٍ شاطئية، حياة ليلية', '/ar/restaurants-nightlife-ibiza/'),
}


def linked_phrase(label: str, href: str) -> str:
    return f'<a {MARKER} href="{href}" style="{STYLE}">{label}</a>'


def enhance(root: Path = ROOT) -> None:
    sitemap = (root / 'sitemap.xml').read_bytes()
    pending = {}
    for lang, (label, href) in PAGES.items():
        path = root / lang / 'index.html'
        html = path.read_text(encoding='utf-8')
        target = root / href.strip('/') / 'index.html'
        canonical = (BASE + href).encode()
        after = linked_phrase(label, href)
        if not target.is_file() or canonical not in sitemap:
            raise SystemExit(f'Phase 150: missing canonical destination {href}')
        if MARKER in html:
            if html.count(MARKER) != 1 or html.count(after) != 1:
                raise SystemExit(f'Phase 150: malformed existing dining/nightlife link: {lang}')
            continue
        if html.count(label) != 1:
            raise SystemExit(f'Phase 150: expected one unchanged dining/nightlife phrase: {lang}')
        if f'href="{href}"' in html or f"href='{href}'" in html:
            raise SystemExit(f'Phase 150: destination already linked from Home: {lang}')
        pending[path] = html.replace(label, after, 1)
    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')
    if (root / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 150: unexpected sitemap change')
    print(f'PASS: Phase 150 — {len(pending)} localized Home pages link existing dining/nightlife wording; no visible copy or URL change')


if __name__ == '__main__':
    enhance()
