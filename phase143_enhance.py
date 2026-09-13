"""Phase 143: reuse the validated Private Office WebP on existing Partners pages.

This is a post-build, markup-only performance change. It creates no new asset or URL and
retains the existing JPEG as the img fallback.
"""
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path('_site')
PAGES = ('partners', 'fr/partners', 'de/partners', 'ar/partners', 'es/partners')
JPEG = '/assets/images/private-office.jpg'
WEBP = '/assets/images/private-office-hero.webp'
MARKER = 'data-ivm143="partners-hero"'
OPEN = f'<picture {MARKER}><source type="image/webp" srcset="{WEBP}">'


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def enhance():
    jpeg = ROOT / JPEG.lstrip('/')
    webp = ROOT / WEBP.lstrip('/')
    if not jpeg.is_file() or not webp.is_file():
        raise SystemExit('Phase 143: reviewed source assets missing')
    if not 0 < webp.stat().st_size < jpeg.stat().st_size * .65:
        raise SystemExit('Phase 143: existing WebP no longer meets reviewed size budget')

    sitemap = (ROOT / 'sitemap.xml').read_bytes()
    changed = 0
    for slug in PAGES:
        path = ROOT / slug / 'index.html'
        html = path.read_text(encoding='utf-8')
        if MARKER in html:
            if html.count(MARKER) != 1:
                raise SystemExit(f'Phase 143: malformed existing picture on {slug}')
            continue

        candidates = []
        for match in re.finditer(r'<img\b[^>]*>', html, re.I):
            attrs = Tags(match.group()).tags[0][1]
            if attrs.get('src') == JPEG and attrs.get('fetchpriority') == 'high':
                candidates.append(match)
        if len(candidates) != 1:
            raise SystemExit(f'Phase 143: expected one priority Partners hero on {slug}')

        image_tag = candidates[0].group()
        wrapped = OPEN + image_tag + '</picture>'
        html = html[:candidates[0].start()] + wrapped + html[candidates[0].end():]

        if slug == 'partners':
            preload = f'<link rel="preload" as="image" href="{JPEG}">'
            replacement = f'<link rel="preload" as="image" href="{WEBP}" type="image/webp">'
            if html.count(preload) != 1:
                raise SystemExit('Phase 143: expected one English Partners image preload')
            html = html.replace(preload, replacement, 1)

        path.write_text(html, encoding='utf-8')
        changed += 1

    if (ROOT / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 143: sitemap changed unexpectedly')
    print(f'PASS: Phase 143 — Partners heroes updated on {changed} pages; existing WebP preferred with JPEG fallback retained')


if __name__ == '__main__':
    enhance()
