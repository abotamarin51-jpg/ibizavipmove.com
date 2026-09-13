"""Phase 144: serve modern formats for the shared priority villa hero.

Generate AVIF and WebP alternatives from the existing build-produced villa JPEG, wrap only
reviewed fetchpriority=high uses, and retain the original JPEG as the img fallback.
"""
from html.parser import HTMLParser
from io import BytesIO
from pathlib import Path
import re
from PIL import Image, ImageChops, ImageStat, features

ROOT = Path('_site')
PAGES = (
    'luxury-villas-ibiza',
    'fr/villas-luxe-ibiza', 'de/luxusvillen-ibiza', 'ar/luxury-villas-ibiza', 'es/villas-lujo-ibiza',
    'fr/conciergerie-privee-ibiza', 'de/privater-concierge-ibiza', 'ar/private-concierge-ibiza', 'es/concierge-privado-ibiza',
    'ibiza-intelligence/villa-arrival-planning',
    'fr/ibiza-intelligence/villa-arrival-planning', 'de/ibiza-intelligence/villa-arrival-planning',
    'ar/ibiza-intelligence/villa-arrival-planning', 'es/ibiza-intelligence/villa-arrival-planning',
)
PRELOAD_PAGES = {
    'luxury-villas-ibiza',
    'fr/conciergerie-privee-ibiza', 'de/privater-concierge-ibiza', 'ar/private-concierge-ibiza', 'es/concierge-privado-ibiza',
    'fr/ibiza-intelligence/villa-arrival-planning', 'de/ibiza-intelligence/villa-arrival-planning',
    'ar/ibiza-intelligence/villa-arrival-planning', 'es/ibiza-intelligence/villa-arrival-planning',
}
JPEG = '/assets/images/villa.jpg'
AVIF = '/assets/images/villa-priority.avif'
WEBP = '/assets/images/villa-priority.webp'
MARKER = 'data-ivm144="villa-priority"'
OPEN = f'<picture {MARKER}><source type="image/avif" srcset="{AVIF}"><source type="image/webp" srcset="{WEBP}">'
OLD_PRELOAD = f'<link rel="preload" as="image" href="{JPEG}">'
NEW_PRELOAD = f'<link rel="preload" as="image" href="{AVIF}" type="image/avif">'


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def mae(original, encoded_bytes):
    with Image.open(BytesIO(encoded_bytes)) as decoded:
        if decoded.size != original.size:
            raise SystemExit('Phase 144: encoded villa dimensions changed')
        diff = ImageChops.difference(original, decoded.convert('RGB'))
        return sum(ImageStat.Stat(diff).mean) / 3


def enhance():
    if not features.check('avif') or not features.check('webp'):
        raise SystemExit('Phase 144: Pillow build must support AVIF and WebP')

    source = ROOT / JPEG.lstrip('/')
    with Image.open(source) as opened:
        if opened.format != 'JPEG' or opened.size != (2000, 1334):
            raise SystemExit('Phase 144: review changed villa source before encoding')
        original = opened.convert('RGB')

    avif_out = BytesIO(); original.save(avif_out, format='AVIF', quality=60)
    webp_out = BytesIO(); original.save(webp_out, format='WEBP', quality=80, method=6)
    avif = avif_out.getvalue(); webp = webp_out.getvalue()
    jpeg_size = source.stat().st_size
    if not 0 < len(avif) < jpeg_size * .58:
        raise SystemExit('Phase 144: AVIF does not meet reviewed size budget')
    if not 0 < len(webp) < jpeg_size * .78:
        raise SystemExit('Phase 144: WebP does not meet reviewed size budget')
    avif_mae = mae(original, avif); webp_mae = mae(original, webp)
    if avif_mae > 5.0 or webp_mae > 4.0:
        raise SystemExit(f'Phase 144: encoded quality outside reviewed bound ({avif_mae:.3f}, {webp_mae:.3f})')

    sitemap = (ROOT / 'sitemap.xml').read_bytes()
    pending = {}
    changed = 0
    for slug in PAGES:
        path = ROOT / slug / 'index.html'
        html = path.read_text(encoding='utf-8')

        if MARKER in html:
            if html.count(MARKER) != 1 or AVIF not in html or WEBP not in html:
                raise SystemExit(f'Phase 144: malformed existing villa picture on {slug}')
            if slug in PRELOAD_PAGES and (html.count(NEW_PRELOAD) != 1 or OLD_PRELOAD in html):
                raise SystemExit(f'Phase 144: malformed existing AVIF preload on {slug}')
            continue

        candidates = []
        for match in re.finditer(r'<img\b[^>]*>', html, re.I):
            attrs = Tags(match.group()).tags[0][1]
            if attrs.get('src') == JPEG and attrs.get('fetchpriority') == 'high':
                candidates.append(match)
        if len(candidates) != 1:
            raise SystemExit(f'Phase 144: expected one reviewed priority villa image on {slug}, found {len(candidates)}')

        image_tag = candidates[0].group()
        wrapped = OPEN + image_tag + '</picture>'
        html = html[:candidates[0].start()] + wrapped + html[candidates[0].end():]

        old_count = html.count(OLD_PRELOAD)
        if slug in PRELOAD_PAGES:
            if old_count != 1:
                raise SystemExit(f'Phase 144: expected one villa JPEG preload on {slug}, found {old_count}')
            html = html.replace(OLD_PRELOAD, NEW_PRELOAD, 1)
        elif old_count:
            raise SystemExit(f'Phase 144: unexpected villa preload on {slug}')

        pending[path] = html
        changed += 1

    # Write only after every target has validated. Original JPEG and sitemap remain untouched.
    (ROOT / AVIF.lstrip('/')).write_bytes(avif)
    (ROOT / WEBP.lstrip('/')).write_bytes(webp)
    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')

    if (ROOT / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 144: sitemap changed unexpectedly')
    print(
        f'PASS: Phase 144 — {changed} priority villa heroes prefer AVIF/WebP with JPEG fallback; '
        f'{jpeg_size} -> AVIF {len(avif)} bytes / WebP {len(webp)} bytes; '
        f'MAE {avif_mae:.3f}/{webp_mae:.3f}'
    )


if __name__ == '__main__':
    enhance()
