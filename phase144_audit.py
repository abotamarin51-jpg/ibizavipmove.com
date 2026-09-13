"""Read-only gate for Phase 144 priority villa modern-format delivery."""
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image, features

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


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.stack=[]; self.pictures=[]; self.tags=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs); self.tags.append((tag, attrs))
        if tag == 'picture':
            self.stack.append({'attrs': attrs, 'sources': [], 'imgs': []})
        elif tag == 'source' and self.stack:
            self.stack[-1]['sources'].append(attrs)
        elif tag == 'img' and self.stack:
            self.stack[-1]['imgs'].append(attrs)
    def handle_endtag(self, tag):
        if tag == 'picture' and self.stack:
            self.pictures.append(self.stack.pop())


def require(ok, msg):
    if not ok:
        raise SystemExit('Phase 144 audit: ' + msg)


def slug_for(path):
    rel = path.relative_to(ROOT)
    return str(rel.parent).replace('\\', '/') if rel.name == 'index.html' else None


def run():
    require(features.check('avif') and features.check('webp'), 'Pillow modern-format support missing')
    jpeg = ROOT / JPEG.lstrip('/'); avif = ROOT / AVIF.lstrip('/'); webp = ROOT / WEBP.lstrip('/')
    require(jpeg.is_file() and avif.is_file() and webp.is_file(), 'villa assets missing')
    require(avif.stat().st_size < jpeg.stat().st_size * .58, 'AVIF no longer meets reviewed size budget')
    require(webp.stat().st_size < jpeg.stat().st_size * .78, 'WebP no longer meets reviewed size budget')
    with Image.open(jpeg) as j, Image.open(avif) as a, Image.open(webp) as w:
        require(j.size == a.size == w.size == (2000, 1334), 'villa dimensions changed')

    ns = {'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [e.text for e in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ns)]
    require(len(urls) == len(set(urls)) == 156, 'canonical inventory changed')

    observed = set()
    for path in ROOT.rglob('index.html'):
        parsed = Tags(path.read_text(encoding='utf-8'))
        if any(t == 'img' and a.get('src') == JPEG and a.get('fetchpriority') == 'high' for t, a in parsed.tags):
            observed.add(slug_for(path))
    require(observed == set(PAGES), f'unreviewed priority villa inventory: {sorted(observed ^ set(PAGES))}')

    for slug in PAGES:
        path = ROOT / slug / 'index.html'; require(path.is_file(), f'missing target {slug}')
        text = path.read_text(encoding='utf-8'); parsed = Tags(text)
        matches = []
        for pic in parsed.pictures:
            if pic['attrs'].get('data-ivm144') != 'villa-priority':
                continue
            avif_sources = [a for a in pic['sources'] if a.get('type') == 'image/avif' and a.get('srcset') == AVIF]
            webp_sources = [a for a in pic['sources'] if a.get('type') == 'image/webp' and a.get('srcset') == WEBP]
            imgs = [a for a in pic['imgs'] if a.get('src') == JPEG and a.get('fetchpriority') == 'high']
            if avif_sources and webp_sources and imgs:
                matches.append(pic)
        require(len(matches) == 1, f'{slug}: expected one reviewed villa picture')
        require(sum(t == 'h1' for t, a in parsed.tags) == 1, f'{slug}: expected one H1')
        url = 'https://ibizavipmove.com/' + slug + '/'
        require([a.get('href') for t, a in parsed.tags if t == 'link' and a.get('rel') == 'canonical'] == [url], f'{slug}: self canonical')
        require(url in urls, f'{slug}: canonical remains in sitemap')

        preloads = [a for t, a in parsed.tags if t == 'link' and a.get('rel') == 'preload' and a.get('as') == 'image']
        require(not any(a.get('href') == JPEG for a in preloads), f'{slug}: JPEG preload would duplicate modern-format selection')
        if slug in PRELOAD_PAGES:
            require(any(a.get('href') == AVIF and a.get('type') == 'image/avif' for a in preloads), f'{slug}: AVIF preload missing')
        else:
            require(not any(a.get('href') == AVIF for a in preloads), f'{slug}: unexpected new preload')

    print(
        f'PASS: Phase 144 audit — {len(PAGES)} priority villa pages prefer AVIF/WebP with JPEG fallback; '
        f'{jpeg.stat().st_size} -> {avif.stat().st_size}/{webp.stat().st_size} bytes; 156-URL sitemap preserved'
    )


if __name__ == '__main__':
    run()
