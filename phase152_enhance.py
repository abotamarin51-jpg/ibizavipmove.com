"""Phase 152: reuse the existing modern Private Office hero on priority localized Media & Partners pages.

FR/DE/AR Media & Partners currently preload and render the 727 KB JPEG even though the
same 3024x4032 hero already has a 358 KB WebP used elsewhere on the site. Prefer that
existing WebP through <picture> and preload it, while preserving the JPEG fallback.
No visible copy, URL, schema, form, tracking, price, policy, sitemap or navigation change.
"""
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path('_site')
PAGES = ('fr/media-partners', 'de/media-partners', 'ar/media-partners')
JPEG = '/assets/images/private-office.jpg'
WEBP = '/assets/images/private-office-hero.webp'
MARKER = 'data-ivm152="media-partner-hero"'
OLD_PRELOAD = f'<link rel="preload" as="image" href="{JPEG}">'
NEW_PRELOAD = f'<link rel="preload" as="image" href="{WEBP}" type="image/webp">'
OPEN = f'<picture {MARKER}><source type="image/webp" srcset="{WEBP}">'


class Tags(HTMLParser):
    def __init__(self, text: str):
        super().__init__(); self.tags=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def enhance(root: Path = ROOT) -> None:
    sitemap = (root / 'sitemap.xml').read_bytes()
    jpeg = root / JPEG.lstrip('/')
    webp = root / WEBP.lstrip('/')
    if not jpeg.is_file() or not webp.is_file():
        raise SystemExit('Phase 152: expected existing Private Office JPEG/WebP assets')
    jpeg_size, webp_size = jpeg.stat().st_size, webp.stat().st_size
    if not (0 < webp_size < jpeg_size * .60):
        raise SystemExit(f'Phase 152: existing WebP no longer meets reviewed size budget ({jpeg_size}->{webp_size})')

    pending = {}
    for slug in PAGES:
        path = root / slug / 'index.html'
        html = path.read_text(encoding='utf-8')
        if MARKER in html:
            if html.count(MARKER) != 1 or html.count(WEBP) < 2:
                raise SystemExit(f'Phase 152: malformed existing picture/preload on {slug}')
            if html.count(NEW_PRELOAD) != 1 or OLD_PRELOAD in html:
                raise SystemExit(f'Phase 152: malformed existing WebP preload on {slug}')
            continue

        candidates = []
        for match in re.finditer(r'<img\b[^>]*>', html, re.I):
            tags = Tags(match.group()).tags
            if not tags:
                continue
            attrs = tags[0][1]
            if attrs.get('src') == JPEG and attrs.get('fetchpriority') == 'high':
                candidates.append(match)
        if len(candidates) != 1:
            raise SystemExit(f'Phase 152: expected one priority Private Office hero on {slug}, found {len(candidates)}')
        if html.count(OLD_PRELOAD) != 1 or NEW_PRELOAD in html:
            raise SystemExit(f'Phase 152: unexpected preload baseline on {slug}')
        image_tag = candidates[0].group()
        updated = html[:candidates[0].start()] + OPEN + image_tag + '</picture>' + html[candidates[0].end():]
        updated = updated.replace(OLD_PRELOAD, NEW_PRELOAD, 1)
        pending[path] = updated

    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')
    if (root / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 152: sitemap changed unexpectedly')
    print(f'PASS: Phase 152 — {len(pending)} FR/DE/AR Media & Partners heroes prefer existing WebP with JPEG fallback; {jpeg_size}->{webp_size} bytes')


if __name__ == '__main__':
    enhance()
