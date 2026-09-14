"""Read-only gate for Phase 152 localized Media & Partners modern hero delivery."""
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET
from phase152_enhance import JPEG, WEBP, MARKER, NEW_PRELOAD, OLD_PRELOAD, PAGES

ROOT = Path('_site')
BASE = 'https://ibizavipmove.com'
LANGS = {'en', 'es', 'fr', 'de', 'ar', 'x-default'}


class Tags(HTMLParser):
    def __init__(self, text: str):
        super().__init__(); self.tags=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit('Phase 152 audit: ' + message)


def run(root: Path = ROOT) -> None:
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [e.text for e in ET.parse(root / 'sitemap.xml').findall('s:url/s:loc', ns)]
    require(len(urls) == len(set(urls)) == 156, 'canonical inventory changed')
    jpeg = root / JPEG.lstrip('/')
    webp = root / WEBP.lstrip('/')
    require(jpeg.is_file() and webp.is_file(), 'expected JPEG/WebP assets')
    require(0 < webp.stat().st_size < jpeg.stat().st_size * .60, 'WebP size budget')

    for slug in PAGES:
        path = root / slug / 'index.html'
        html = path.read_text(encoding='utf-8')
        tags = Tags(html).tags
        require(html.count(MARKER) == 1, f'one picture marker: {slug}')
        require(html.count(NEW_PRELOAD) == 1 and OLD_PRELOAD not in html, f'WebP preload: {slug}')
        require(html.count(WEBP) == 2, f'WebP source + preload: {slug}')
        pictures = [a for t,a in tags if t == 'picture' and a.get('data-ivm152') == 'media-partner-hero']
        require(len(pictures) == 1, f'one tagged picture: {slug}')
        sources = [a for t,a in tags if t == 'source' and a.get('type') == 'image/webp' and a.get('srcset') == WEBP]
        require(len(sources) >= 1, f'WebP picture source: {slug}')
        imgs = [a for t,a in tags if t == 'img' and a.get('src') == JPEG and a.get('fetchpriority') == 'high']
        require(len(imgs) == 1, f'priority JPEG fallback: {slug}')
        canonical = BASE + '/' + slug + '/'
        require(canonical in urls, f'sitemap membership: {slug}')
        require([a.get('href') for t,a in tags if t == 'link' and a.get('rel') == 'canonical'] == [canonical], f'self canonical: {slug}')
        require(sum(t == 'h1' for t,a in tags) == 1, f'one H1: {slug}')
        require(not any(t == 'meta' and a.get('name','').lower() in {'robots','googlebot'} and 'noindex' in a.get('content','').lower() for t,a in tags), f'indexable: {slug}')
        require({a.get('hreflang') for t,a in tags if t == 'link' and a.get('rel') == 'alternate'} == LANGS, f'hreflang: {slug}')
        html_tag = next(a for t,a in tags if t == 'html')
        lang = slug.split('/',1)[0]
        require(html_tag.get('lang') == lang, f'language: {slug}')
        if lang == 'ar':
            require(html_tag.get('dir') == 'rtl', 'Arabic RTL preserved')
    print('PASS: Phase 152 audit — FR/DE/AR Media & Partners priority heroes use the existing WebP with JPEG fallback; canonicals/hreflang/indexability and 156-URL sitemap preserved')


if __name__ == '__main__':
    run()
