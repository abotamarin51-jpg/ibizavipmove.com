from pathlib import Path
from urllib.parse import urljoin, urlparse
import json
import math
import re
import struct
import zlib
import xml.etree.ElementTree as ET

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
ENTITY_ID = BASE + '/#organization'
INSTAGRAM = 'https://www.instagram.com/ibizavipmove/'
STYLE = '/assets/phase30.css?v=30'
TODAY = '2026-09-03'
BRAND_MARK = BASE + '/assets/brand-mark.svg'
HOME_IMAGE = BASE + '/assets/images/hero-desktop.jpg'
LANGUAGES = ['English', 'Spanish', 'French', 'German', 'Arabic']

assets = ROOT / 'assets'
assets.mkdir(parents=True, exist_ok=True)
(assets / 'phase30.css').write_text(Path('phase30.css').read_text(encoding='utf-8'), encoding='utf-8')

# ---------------------------------------------------------------------------
# Search-result favicon: Google Search's current favicon documentation favours
# a stable square raster asset. Generate one from the brand's four-petal motif
# using only the Python standard library so CI stays dependency-free.
# ---------------------------------------------------------------------------
def png_chunk(kind, data):
    return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)


def draw_line(buf, size, x0, y0, x1, y1, colour, thickness):
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy), 1)
    radius = max(1, thickness // 2)
    for i in range(steps + 1):
        x = round(x0 + dx * i / steps)
        y = round(y0 + dy * i / steps)
        for oy in range(-radius, radius + 1):
            for ox in range(-radius, radius + 1):
                if ox * ox + oy * oy > radius * radius:
                    continue
                xx, yy = x + ox, y + oy
                if 0 <= xx < size and 0 <= yy < size:
                    p = (yy * size + xx) * 3
                    buf[p:p+3] = bytes(colour)


def make_favicon(size, target):
    bg = (9, 14, 19)
    gold = (185, 145, 88)
    buf = bytearray(bg * (size * size))
    c = (size - 1) / 2
    # Four nested rose curves echo the official brand-mark geometry.
    for scale in (0.88, 0.69, 0.50, 0.31):
        pts = []
        for i in range(721):
            t = 2 * math.pi * i / 720
            r = size * 0.39 * scale * math.cos(2 * t)
            x = c + r * math.cos(t)
            y = c + r * math.sin(t)
            pts.append((round(x), round(y)))
        thick = max(2, round(size / 80))
        for a, b in zip(pts, pts[1:]):
            draw_line(buf, size, a[0], a[1], b[0], b[1], gold, thick)
    raw = bytearray()
    row = size * 3
    for y in range(size):
        raw.append(0)
        raw.extend(buf[y*row:(y+1)*row])
    png = b'\x89PNG\r\n\x1a\n'
    png += png_chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
    png += png_chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += png_chunk(b'IEND', b'')
    target.write_bytes(png)


make_favicon(192, assets / 'favicon-192.png')
make_favicon(512, assets / 'favicon-512.png')

manifest = {
    'name': 'Ibiza VIP Move',
    'short_name': 'Ibiza VIP Move',
    'start_url': '/',
    'display': 'standalone',
    'background_color': '#090e13',
    'theme_color': '#090e13',
    'icons': [
        {'src': '/assets/favicon-192.png', 'sizes': '192x192', 'type': 'image/png'},
        {'src': '/assets/favicon-512.png', 'sizes': '512x512', 'type': 'image/png'},
    ],
}
(ROOT / 'site.webmanifest').write_text(json.dumps(manifest, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')

# ---------------------------------------------------------------------------
# Entity authority, social identity and preferred-image metadata.
# ---------------------------------------------------------------------------
JSONLD_RE = re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>', re.I | re.S)
CANONICAL_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.I)
OG_IMAGE_RE = re.compile(r'<meta\s+property="og:image"\s+content="([^"]+)"', re.I)
NOINDEX_RE = re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex', re.I)


def set_meta(text, selector, value):
    pattern = rf'(<meta\s+{selector}\s+content=")[^"]*(")'
    if re.search(pattern, text, flags=re.I):
        return re.sub(pattern, lambda m: m.group(1) + value + m.group(2), text, count=1, flags=re.I)
    return text


def enhance_schema(raw, canonical, preferred):
    try:
        data = json.loads(raw)
    except Exception:
        return raw
    if not isinstance(data, dict):
        return raw

    typ = data.get('@type')
    types = set(typ if isinstance(typ, list) else [typ])
    is_entity = data.get('@id') == ENTITY_ID or (
        data.get('name') == 'Ibiza VIP Move' and bool(types & {'Organization', 'LocalBusiness', 'ProfessionalService'})
    )

    if is_entity:
        data['@id'] = ENTITY_ID
        data['name'] = 'Ibiza VIP Move'
        data['alternateName'] = 'Ibiza VIP Move Concierge'
        data['url'] = BASE + '/'
        data['sameAs'] = [INSTAGRAM]
        data['slogan'] = 'Discretion. Access. Excellence.'
        data['logo'] = {
            '@type': 'ImageObject',
            'url': BRAND_MARK,
            'contentUrl': BRAND_MARK,
            'width': 220,
            'height': 220,
        }
        data['image'] = HOME_IMAGE
        data['areaServed'] = {'@type': 'Place', 'name': 'Ibiza, Balearic Islands, Spain'}
        data['knowsLanguage'] = LANGUAGES
        cp = data.get('contactPoint') if isinstance(data.get('contactPoint'), dict) else {}
        cp.update({
            '@type': 'ContactPoint',
            'telephone': '+34 600 703 303',
            'email': 'partnership@ibizavipmove.com',
            'contactType': 'customer service',
            'url': BASE + '/contact/',
            'availableLanguage': LANGUAGES,
        })
        data['contactPoint'] = cp

    if typ == 'WebSite':
        data['publisher'] = {'@id': ENTITY_ID}

    if typ in ('WebPage', 'AboutPage', 'ContactPage', 'CollectionPage', 'ProfilePage'):
        data['about'] = {'@id': ENTITY_ID}
        data['publisher'] = {'@id': ENTITY_ID}
        if preferred:
            data['primaryImageOfPage'] = {'@type': 'ImageObject', 'url': preferred, 'contentUrl': preferred}

    if typ == 'Service':
        data['provider'] = {'@id': ENTITY_ID}
        data['areaServed'] = {'@type': 'Place', 'name': 'Ibiza, Balearic Islands, Spain'}
        if canonical:
            data['url'] = canonical
        if preferred:
            data['image'] = preferred

    return json.dumps(data, ensure_ascii=False)


indexable_pages = 0
footer_links = 0
for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    noindex = bool(NOINDEX_RE.search(text))
    cm = CANONICAL_RE.search(text)
    canonical = cm.group(1).strip() if cm else ''
    is_home = canonical.rstrip('/') == BASE

    if not noindex and '</head>' in text:
        indexable_pages += 1
        if STYLE not in text:
            text = text.replace('</head>', f'<link rel="stylesheet" href="{STYLE}"></head>', 1)
        if 'rel="manifest"' not in text:
            text = text.replace('</head>', '<link rel="manifest" href="/site.webmanifest"></head>', 1)
        if '/assets/favicon-192.png' not in text:
            fav = '<link rel="icon" type="image/png" sizes="192x192" href="/assets/favicon-192.png"><link rel="apple-touch-icon" sizes="192x192" href="/assets/favicon-192.png">'
            text = text.replace('</head>', fav + '</head>', 1)
        if f'rel="me" href="{INSTAGRAM}"' not in text:
            text = text.replace('</head>', f'<link rel="me" href="{INSTAGRAM}"></head>', 1)
        if 'name="author"' not in text:
            text = text.replace('</head>', '<meta name="author" content="Ibiza VIP Move"></head>', 1)

    if is_home:
        text = set_meta(text, 'property="og:image"', HOME_IMAGE)
        text = set_meta(text, 'property="og:image:secure_url"', HOME_IMAGE)
        text = set_meta(text, 'name="twitter:image"', HOME_IMAGE)
        text = set_meta(text, 'property="og:image:alt"', 'Ibiza VIP Move · Private Concierge in Ibiza')
        if 'property="og:image:type"' not in text:
            text = text.replace('</head>', '<meta property="og:image:type" content="image/jpeg"></head>', 1)

    # Determine the final preferred image after the home update.
    og = OG_IMAGE_RE.search(text)
    preferred = og.group(1).strip() if og else ''
    if preferred.startswith('/'):
        preferred = BASE + preferred

    text = JSONLD_RE.sub(
        lambda m: '<script type="application/ld+json">' + enhance_schema(m.group(1), canonical, preferred) + '</script>',
        text,
    )

    if not noindex and '<footer' in text and 'class="ivm-official"' not in text:
        official = (
            '<div class="ivm-official">'
            '<span>Official Ibiza VIP Move<span class="ivm-official-dot"></span>Ibiza, Spain</span>'
            '<div class="ivm-official-links">'
            f'<a href="{INSTAGRAM}" rel="me external" aria-label="Ibiza VIP Move on Instagram">Instagram @ibizavipmove</a>'
            '<a href="/about/">Official brand information</a>'
            '</div></div>'
        )
        text = text.replace('</footer>', official + '</footer>', 1)
        footer_links += 1

    path.write_text(text, encoding='utf-8')

# ---------------------------------------------------------------------------
# Final-pass image sitemap. This intentionally runs after Phase 28/29 so the
# sitemap reflects the exact final layout and hero imagery users actually see.
# ---------------------------------------------------------------------------
IMG_RE = re.compile(r'<img\b[^>]*\bsrc="([^"]+)"', re.I)
SOURCE_RE = re.compile(r'<source\b[^>]*\bsrcset="([^"]+)"', re.I)
IMAGE_NS = 'http://www.google.com/schemas/sitemap-image/1.1'
SITEMAP_NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'


def abs_url(value):
    value = (value or '').strip()
    if not value or value.startswith(('data:', 'javascript:')):
        return None
    return urljoin(BASE + '/', value)


def local_content_image(url):
    if not url:
        return False
    parsed = urlparse(url)
    if parsed.netloc and parsed.netloc != urlparse(BASE).netloc:
        return False
    p = parsed.path.lower()
    return '/assets/images/' in p and p.endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif'))


entries = []
unique_images = set()
for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    if NOINDEX_RE.search(text):
        continue
    cm = CANONICAL_RE.search(text)
    if not cm:
        continue
    canonical = cm.group(1).strip()
    if not canonical.startswith(BASE):
        continue
    found = []
    og = OG_IMAGE_RE.search(text)
    if og:
        u = abs_url(og.group(1))
        if local_content_image(u):
            found.append(u)
    for src in IMG_RE.findall(text):
        u = abs_url(src)
        if local_content_image(u):
            found.append(u)
    for srcset in SOURCE_RE.findall(text):
        for item in srcset.split(','):
            candidate = item.strip().split()[0] if item.strip() else ''
            u = abs_url(candidate)
            if local_content_image(u):
                found.append(u)
    dedup = []
    seen = set()
    for u in found:
        if u not in seen:
            seen.add(u)
            dedup.append(u)
            unique_images.add(u)
    if dedup:
        entries.append((canonical, dedup))

ET.register_namespace('', SITEMAP_NS)
ET.register_namespace('image', IMAGE_NS)
image_root = ET.Element(f'{{{SITEMAP_NS}}}urlset')
for canonical, images in entries:
    url_el = ET.SubElement(image_root, f'{{{SITEMAP_NS}}}url')
    ET.SubElement(url_el, f'{{{SITEMAP_NS}}}loc').text = canonical
    for image in images:
        image_el = ET.SubElement(url_el, f'{{{IMAGE_NS}}}image')
        ET.SubElement(image_el, f'{{{IMAGE_NS}}}loc').text = image
ET.ElementTree(image_root).write(ROOT / 'image-sitemap.xml', encoding='utf-8', xml_declaration=True)

# Fresh lastmod on the canonical sitemap for this release.
sitemap = ROOT / 'sitemap.xml'
ET.register_namespace('', SITEMAP_NS)
sm_tree = ET.parse(sitemap)
sm_root = sm_tree.getroot()
for url in sm_root.findall(f'{{{SITEMAP_NS}}}url'):
    lastmod = url.find(f'{{{SITEMAP_NS}}}lastmod')
    if lastmod is None:
        lastmod = ET.SubElement(url, f'{{{SITEMAP_NS}}}lastmod')
    lastmod.text = TODAY
sm_tree.write(sitemap, encoding='utf-8', xml_declaration=True)

robots = ROOT / 'robots.txt'
rt = robots.read_text(encoding='utf-8') if robots.exists() else 'User-agent: *\nAllow: /\n'
lines = [line for line in rt.splitlines() if not line.lower().startswith('sitemap:')]
lines.extend([f'Sitemap: {BASE}/sitemap.xml', f'Sitemap: {BASE}/image-sitemap.xml'])
robots.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')

# Strengthen the already-existing machine-readable brand summary without
# implying that llms.txt is a search-ranking requirement.
llms = ROOT / 'llms.txt'
if llms.exists():
    llm_text = llms.read_text(encoding='utf-8')
    llm_text = re.sub(r'> Last updated: .*?\.', f'> Last updated: {TODAY}.', llm_text, count=1)
    if 'Official Instagram:' not in llm_text:
        needle = f'Official website: {BASE}/\n'
        llm_text = llm_text.replace(needle, needle + f'Official Instagram: {INSTAGRAM}\n', 1)
    if 'Primary geographic entity:' not in llm_text:
        llm_text += '\n## Entity summary\nPrimary geographic entity: Ibiza, Balearic Islands, Spain.\nOfficial brand name: Ibiza VIP Move.\nOfficial Instagram: ' + INSTAGRAM + '\n'
    llms.write_text(llm_text, encoding='utf-8')

# Validation.
assert (assets / 'favicon-192.png').stat().st_size > 1000
assert (assets / 'favicon-512.png').stat().st_size > 3000
assert (ROOT / 'site.webmanifest').is_file()
assert indexable_pages >= 35, f'Unexpectedly low indexable page count: {indexable_pages}'
assert footer_links >= 30, f'Official social footer added to too few pages: {footer_links}'
assert entries and len(unique_images) >= 8, 'Final image sitemap lacks sufficient imagery'
final_home = (ROOT / 'index.html').read_text(encoding='utf-8')
assert HOME_IMAGE in final_home
assert INSTAGRAM in final_home
assert 'sameAs' in final_home and 'Ibiza VIP Move Concierge' in final_home
assert '/assets/favicon-192.png' in final_home
assert STYLE in final_home
assert f'Sitemap: {BASE}/image-sitemap.xml' in robots.read_text(encoding='utf-8')
assert f'> Last updated: {TODAY}.' in llms.read_text(encoding='utf-8')
print(f'PASS: Phase 30 authority — {indexable_pages} indexable pages, {footer_links} official social footers, {len(unique_images)} final local images')
