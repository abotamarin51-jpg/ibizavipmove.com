"""Offer a lighter, same-resolution B2B hero while retaining the original JPEG."""
from html.parser import HTMLParser
from io import BytesIO
from pathlib import Path
import re
from PIL import Image

ROOT = Path('_site')
PAGES = ('private-office', 'es/private-office', 'fr/private-office', 'de/private-office', 'ar/private-office')
JPEG = '/assets/images/private-office.jpg'
WEBP = '/assets/images/private-office-hero.webp'
OPEN = '<picture data-ivm139="office-hero"><source type="image/webp" srcset="' + WEBP + '">'


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def enhance():
    source = ROOT / JPEG.lstrip('/')
    with Image.open(source) as image:
        if image.format != 'JPEG' or image.size != (3024, 4032):
            raise SystemExit('Phase 139: review changed Private Office source before encoding')
        output = BytesIO()
        image.convert('RGB').save(output, format='WEBP', quality=85, method=6)
    content = output.getvalue()
    if not 0 < len(content) < source.stat().st_size * .65:
        raise SystemExit('Phase 139: WebP does not meet the reviewed size budget')
    pending = {}
    for slug in PAGES:
        path = ROOT / slug / 'index.html'
        html = path.read_text(encoding='utf-8')
        tags = Tags(html).tags
        if any(tag == 'link' and a.get('rel') == 'preload' and a.get('as') == 'image' for tag, a in tags):
            raise SystemExit(f'Phase 139: review unexpected hero preload on {slug}')
        candidates = []
        for match in re.finditer(r'<img\b[^>]*>', html, re.I):
            attrs = Tags(match.group()).tags[0][1]
            if attrs.get('src') == JPEG and attrs.get('fetchpriority') == 'high':
                candidates.append(match)
        if len(candidates) != 1:
            raise SystemExit(f'Phase 139: expected exactly one original priority hero on {slug}')
        image_tag = candidates[0].group()
        wrapped = OPEN + image_tag + '</picture>'
        if 'data-ivm139' in html:
            if html.count(wrapped) != 1:
                raise SystemExit(f'Phase 139: malformed existing picture on {slug}')
        else:
            html = html[:candidates[0].start()] + wrapped + html[candidates[0].end():]
        pending[path] = html
    # Validate every target before writing. No original asset or sitemap rewrite.
    (ROOT / WEBP.lstrip('/')).write_bytes(content)
    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')
    print(f'PASS: Phase 139 — five Private Office heroes gain WebP with unchanged JPEG fallback; {source.stat().st_size} -> {len(content)} bytes, same 3024x4032 image')


if __name__ == '__main__':
    enhance()
