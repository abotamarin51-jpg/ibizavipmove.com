"""Read-only gate for FR/DE/AR Services contact routing."""
from pathlib import Path
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

ROOT = Path('_site')
TARGETS = {
    'fr/services': ('/fr/contact/', 'https://ibizavipmove.com/fr/services/'),
    'de/services': ('/de/kontakt/', 'https://ibizavipmove.com/de/services/'),
    'ar/services': ('/ar/contact/', 'https://ibizavipmove.com/ar/services/'),
}


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.hrefs = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            data = dict(attrs)
            if data.get('href'):
                self.hrefs.append(data['href'])


def require(ok, message):
    if not ok:
        raise SystemExit('Phase 135 audit: ' + message)


def run():
    before = (ROOT / 'sitemap.xml').read_bytes()
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [n.text for n in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ns)]
    require(len(urls) == len(set(urls)) == 156, 'sitemap inventory')
    for slug, (local_contact, canonical) in TARGETS.items():
        page = ROOT / slug / 'index.html'
        target = ROOT / local_contact.strip('/') / 'index.html'
        require(page.is_file() and target.is_file(), 'page/contact target ' + slug)
        html = page.read_text(encoding='utf-8')
        hrefs = Links(html).hrefs
        require('/contact/' not in hrefs, 'English contact leakage on ' + slug)
        require(hrefs.count(local_contact) == 4, 'localized contact route cardinality on ' + slug)
        require(html.count(f'<link rel="canonical" href="{canonical}"') == 1, 'canonical ' + slug)
        require(canonical in urls, 'sitemap membership ' + slug)
        require(html.count('<h1') == 1, 'H1 ' + slug)
    require((ROOT / 'sitemap.xml').read_bytes() == before, 'audit mutated sitemap')
    print('PASS: Phase 135 audit — FR/DE/AR Services hubs keep all contact pathways in-language; targets exist; canonical/H1/sitemap unchanged')


if __name__ == '__main__':
    run()
