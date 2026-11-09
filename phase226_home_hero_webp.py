"""Serve lighter WebP variants for the five Home hero images without changing copy or layout."""
from html.parser import HTMLParser
from io import BytesIO
from pathlib import Path
import re
from PIL import Image, ImageChops, ImageStat, features

ROOT = Path('_site')
PAGES = ('', 'fr', 'de', 'ar', 'es')
DESKTOP_JPG = '/assets/images/hero-desktop.jpg'
MOBILE_JPG = '/assets/images/hero-mobile.jpg'
DESKTOP_WEBP = '/assets/images/hero-desktop.webp'
MOBILE_WEBP = '/assets/images/hero-mobile.webp'
MARKER = 'data-ivm226="home-hero-webp"'
PICTURE_OPEN = '<picture class="ivm-ref-hero-picture">'
OLD_MOBILE = '<source media="(max-width:700px)" srcset="/assets/images/hero-mobile.jpg">'
NEW_SOURCES = (
    '<source ' + MARKER + ' media="(max-width:700px)" type="image/webp" srcset="' + MOBILE_WEBP + '">'
    + OLD_MOBILE
    + '<source type="image/webp" srcset="' + DESKTOP_WEBP + '">'
)
PRELOAD = (
    '<link rel="preload" as="image" href="' + DESKTOP_WEBP + '" type="image/webp" '
    'imagesrcset="' + MOBILE_WEBP + ' 900w, ' + DESKTOP_WEBP + ' 2000w" '
    'imagesizes="100vw" fetchpriority="high">'
)

class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

def mae(original, encoded):
    with Image.open(BytesIO(encoded)) as decoded:
        if decoded.size != original.size:
            raise SystemExit('Phase 226: encoded Home hero dimensions changed')
        diff = ImageChops.difference(original, decoded.convert('RGB'))
        return sum(ImageStat.Stat(diff).mean) / 3

def encode(path, expected_size):
    with Image.open(path) as opened:
        if opened.format != 'JPEG' or opened.size != expected_size:
            raise SystemExit(f'Phase 226: unexpected Home hero source {path.name}: {opened.format} {opened.size}')
        original = opened.convert('RGB')
    out = BytesIO()
    original.save(out, format='WEBP', quality=80, method=6)
    data = out.getvalue()
    if not 0 < len(data) < path.stat().st_size * .60:
        raise SystemExit(f'Phase 226: {path.name} WebP does not meet the reviewed size budget')
    score = mae(original, data)
    if score > 3.0:
        raise SystemExit(f'Phase 226: {path.name} WebP quality outside reviewed bound ({score:.3f})')
    return data, score

def image_preloads(html):
    tags = re.findall(r'<link\b[^>]*>', html, flags=re.I | re.S)
    return [tag for tag in tags if 'rel="preload"' in tag and 'as="image"' in tag]

def enhance():
    if not features.check('webp'):
        raise SystemExit('Phase 226: Pillow build must support WebP')

    desktop_path = ROOT / DESKTOP_JPG.lstrip('/')
    mobile_path = ROOT / MOBILE_JPG.lstrip('/')
    desktop, desktop_mae = encode(desktop_path, (2000, 1273))
    mobile, mobile_mae = encode(mobile_path, (900, 1250))

    pending = {}
    for slug in PAGES:
        path = ROOT / slug / 'index.html' if slug else ROOT / 'index.html'
        html = path.read_text(encoding='utf-8')
        before_head = html.split('</head>', 1)[0]
        before_h1 = html.count('<h1')

        if MARKER in html:
            if (html.count(MARKER) != 1 or html.count(DESKTOP_WEBP) < 2
                    or html.count(MOBILE_WEBP) < 2 or html.count(PRELOAD) != 1):
                raise SystemExit(f'Phase 226: malformed existing Home WebP markup on {slug or "en"}')
            continue

        target = PICTURE_OPEN + OLD_MOBILE
        if html.count(target) != 1:
            raise SystemExit(f'Phase 226: expected one responsive Home hero on {slug or "en"}')
        html = html.replace(target, PICTURE_OPEN + NEW_SOURCES, 1)

        preloads = image_preloads(html)
        if len(preloads) != 1:
            raise SystemExit(f'Phase 226: expected one Home image preload on {slug or "en"}, found {len(preloads)}')
        html = html.replace(preloads[0], PRELOAD, 1)

        after_head = html.split('</head>', 1)[0]
        def strip_preload(text):
            return re.sub(r'<link\b[^>]*rel="preload"[^>]*as="image"[^>]*>', '', text, count=1, flags=re.I | re.S)
        if strip_preload(before_head) != strip_preload(after_head):
            raise SystemExit(f'Phase 226: unexpected Home head drift on {slug or "en"}')
        if html.count('<h1') != before_h1 or html.count('<link rel="canonical"') != 1:
            raise SystemExit(f'Phase 226: Home SEO identity changed on {slug or "en"}')
        pending[path] = html

    (ROOT / DESKTOP_WEBP.lstrip('/')).write_bytes(desktop)
    (ROOT / MOBILE_WEBP.lstrip('/')).write_bytes(mobile)
    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')

    for slug in PAGES:
        path = ROOT / slug / 'index.html' if slug else ROOT / 'index.html'
        html = path.read_text(encoding='utf-8')
        if (html.count(MARKER) != 1 or html.count(PRELOAD) != 1
                or DESKTOP_JPG not in html or MOBILE_JPG not in html):
            raise SystemExit(f'Phase 226 audit: responsive WebP/JPEG fallback missing on {slug or "en"}')

    print(
        'PASS: Phase 226 — five Home heroes prefer responsive WebP with JPEG fallback; '
        f'desktop {desktop_path.stat().st_size}->{len(desktop)} bytes, '
        f'mobile {mobile_path.stat().st_size}->{len(mobile)} bytes; '
        f'MAE {desktop_mae:.3f}/{mobile_mae:.3f}'
    )

if __name__ == '__main__':
    enhance()
