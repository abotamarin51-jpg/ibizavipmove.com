"""Read-only gate for Phase 143 Partners hero format optimization."""
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path('_site')
PAGES = ('partners', 'fr/partners', 'de/partners', 'ar/partners', 'es/partners')
JPEG = '/assets/images/private-office.jpg'
WEBP = '/assets/images/private-office-hero.webp'


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
        raise SystemExit('Phase 143 audit: ' + msg)


def run():
    jpeg = ROOT / JPEG.lstrip('/')
    webp = ROOT / WEBP.lstrip('/')
    require(jpeg.is_file() and webp.is_file(), 'reviewed assets missing')
    require(webp.stat().st_size < jpeg.stat().st_size * .65, 'WebP no longer meets reviewed size budget')

    ns = {'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [e.text for e in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ns)]
    require(len(urls) == len(set(urls)) == 156, 'canonical inventory changed')

    for slug in PAGES:
        path = ROOT / slug / 'index.html'
        require(path.is_file(), f'missing target {slug}')
        text = path.read_text(encoding='utf-8')
        parsed = Tags(text)
        matches = []
        for pic in parsed.pictures:
            if pic['attrs'].get('data-ivm143') != 'partners-hero':
                continue
            sources = [a for a in pic['sources'] if a.get('type') == 'image/webp' and a.get('srcset') == WEBP]
            imgs = [a for a in pic['imgs'] if a.get('src') == JPEG and a.get('fetchpriority') == 'high']
            if sources and imgs:
                matches.append((pic, sources, imgs))
        require(len(matches) == 1, f'{slug}: expected exactly one reviewed Partners picture')
        require(sum(t == 'h1' for t, a in parsed.tags) == 1, f'{slug}: expected one H1')
        url = 'https://ibizavipmove.com/' + slug + '/'
        require([a.get('href') for t, a in parsed.tags if t == 'link' and a.get('rel') == 'canonical'] == [url], f'{slug}: self canonical')
        require(url in urls, f'{slug}: canonical remains in sitemap')

        if slug == 'partners':
            preloads = [a for t, a in parsed.tags if t == 'link' and a.get('rel') == 'preload' and a.get('as') == 'image']
            require(any(a.get('href') == WEBP and a.get('type') == 'image/webp' for a in preloads), 'English Partners WebP preload missing')
            require(not any(a.get('href') == JPEG for a in preloads), 'English Partners still preloads JPEG')

    print(f'PASS: Phase 143 audit — five Partners pages prefer existing lighter WebP ({jpeg.stat().st_size} -> {webp.stat().st_size} bytes) with JPEG fallback; H1/canonicals and 156-URL sitemap preserved')


if __name__ == '__main__':
    run()
