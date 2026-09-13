"""Read-only gate for same-resolution Private Office WebP/fallback integrity."""
from html.parser import HTMLParser
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from PIL import Image, ImageChops, ImageStat
from phase144_audit import run as run_priority_villa_format_audit
from phase145_audit import run as run_local_concierge_metadata_audit

ROOT = Path('_site')
JPEG = '/assets/images/private-office.jpg'
WEBP = '/assets/images/private-office-hero.webp'
PAGES = ('private-office', 'es/private-office', 'fr/private-office', 'de/private-office', 'ar/private-office')


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def require(ok, msg):
    if not ok:
        raise SystemExit('Phase 139 audit: ' + msg)


def run():
    src, dest = (ROOT / p.lstrip('/') for p in (JPEG, WEBP))
    require(src.is_file() and dest.is_file(), 'both source and WebP must exist')
    require(0 < dest.stat().st_size < src.stat().st_size * .65, 'at least 35 percent smaller hero payload')
    with Image.open(src) as original, Image.open(dest) as encoded:
        require(original.format == 'JPEG' and encoded.format == 'WEBP', 'correct fallback/preferred formats')
        require(original.size == encoded.size == (3024, 4032), 'same reviewed resolution and framing')
        mean = sum(ImageStat.Stat(ImageChops.difference(original.convert('RGB'), encoded.convert('RGB'))).mean) / 3
        require(mean < 2.0, f'pixel-difference guard exceeded: {mean}')
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [e.text for e in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ns)]
    require(len(urls) == len(set(urls)) == 156, 'unchanged canonical inventory')
    for slug in PAGES:
        html = (ROOT / slug / 'index.html').read_text(encoding='utf-8')
        tags = Tags(html).tags
        blocks = re.findall(r'<picture data-ivm139="office-hero">(.*?)</picture>', html, re.S)
        require(len(blocks) == 1 and html.count('data-ivm139') == 1, f'one picture {slug}')
        inner = Tags(blocks[0]).tags
        require([t for t, a in inner] == ['source', 'img'], f'progressive source before fallback {slug}')
        require(inner[0][1] == {'type': 'image/webp', 'srcset': WEBP}, f'exact WebP source {slug}')
        img = inner[1][1]
        require(img.get('src') == JPEG and img.get('fetchpriority') == 'high' and img.get('loading') != 'lazy', f'unchanged early-discovered JPEG fallback {slug}')
        require(img.get('alt') and img.get('width') and img.get('height'), f'accessible dimensioned image {slug}')
        require(not any(t == 'link' and a.get('rel') == 'preload' and a.get('as') == 'image' for t, a in tags), f'no duplicate/mismatched image preload {slug}')
        require(sum(t == 'h1' for t, a in tags) == 1, f'one H1 {slug}')
        url = 'https://ibizavipmove.com/' + slug + '/'
        require(url in urls, f'existing canonical in sitemap {slug}')
        require([a.get('href') for t, a in tags if t == 'link' and a.get('rel') == 'canonical'] == [url], f'self canonical {slug}')
        require(not any(t == 'meta' and a.get('name', '').lower() == 'robots' and 'noindex' in a.get('content', '').lower() for t, a in tags), f'indexability {slug}')
        css = [a.get('href', '') for t, a in tags if t == 'link' and a.get('rel') == 'stylesheet' and a.get('href', '').startswith('/assets/')]
        require(len(css) == 1 and css[0].startswith('/assets/bundles/') and (ROOT / css[0].split('?')[0].lstrip('/')).is_file(), f'one existing first-party CSS bundle {slug}')
        require({a.get('hreflang') for t, a in tags if t == 'link' and a.get('rel') == 'alternate'} == {'en','es','fr','de','ar','x-default'}, f'language cluster {slug}')
    run_priority_villa_format_audit()
    run_local_concierge_metadata_audit()
    print(f'PASS: Phase 139 audit — five B2B heroes, WebP/JPEG fallback, resolution, payload, pixel-difference guard ({mean:.3f}/255), SEO and CSS integrity; 156 sitemap canonicals')


if __name__ == '__main__':
    run()
