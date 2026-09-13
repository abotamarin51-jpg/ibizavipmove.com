"""Read-only gate for Phase 142 localized-home responsive hero markup."""
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET
from phase143_audit import run as run_partners_hero_webp_audit

ROOT = Path('_site')
PAGES = ('fr', 'de', 'ar', 'es')
DESKTOP = '/assets/images/hero-desktop.jpg'
MOBILE = '/assets/images/hero-mobile.jpg'


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.stack=[]; self.pictures=[]; self.tags=[]
        self.feed(text)
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
        raise SystemExit('Phase 142 audit: ' + msg)


def run():
    desktop = ROOT / 'assets/images/hero-desktop.jpg'
    mobile = ROOT / 'assets/images/hero-mobile.jpg'
    require(desktop.exists() and mobile.exists(), 'hero assets missing')
    require(mobile.stat().st_size < desktop.stat().st_size, 'mobile hero must be lighter than desktop hero')

    for slug in PAGES:
        path = ROOT / slug / 'index.html'
        text = path.read_text(encoding='utf-8')
        parsed = Tags(text)
        matches = []
        for pic in parsed.pictures:
            imgs = [a for a in pic['imgs'] if a.get('src') == DESKTOP and a.get('fetchpriority') == 'high']
            sources = [a for a in pic['sources'] if a.get('srcset') == MOBILE and a.get('media') == '(max-width:700px)']
            if imgs and sources:
                matches.append((pic, imgs, sources))
        require(len(matches) == 1, f'{slug}: expected exactly one responsive priority hero picture')
        require(text.count('<h1') == 1, f'{slug}: expected one H1')
        require(text.count('rel="canonical"') == 1, f'{slug}: expected one canonical')

    sitemap = ET.parse(ROOT / 'sitemap.xml').getroot()
    ns = {'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = sitemap.findall('s:url', ns)
    require(len(urls) == 156, f'sitemap changed: {len(urls)} URLs')
    run_partners_hero_webp_audit()
    print('PASS: Phase 142 — localized home mobile hero gate')


if __name__ == '__main__':
    run()
