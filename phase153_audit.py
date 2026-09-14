"""Read-only regression gate for Phase 153 French bespoke-concierge discovery link."""
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path('_site')
SOURCE = 'fr'
DEST = '/fr/conciergerie-sur-mesure-ibiza/'
LABEL = 'demandes sur mesure'
MARKER = 'data-ivm153="bespoke"'


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def require(ok, msg):
    if not ok:
        raise SystemExit('Phase 153 audit: ' + msg)


def run(root: Path = ROOT) -> None:
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls=[e.text for e in ET.parse(root/'sitemap.xml').findall('s:url/s:loc',ns)]
    require(len(urls)==len(set(urls))==156,'canonical inventory changed')
    source=root/SOURCE/'index.html'; target=root/DEST.strip('/')/'index.html'
    require(source.is_file() and target.is_file(),'source/destination missing')
    html=source.read_text(encoding='utf-8'); tags=Tags(html).tags
    require(html.count(MARKER)==1,'exactly one Phase 153 marker')
    require(sum(1 for t,a in tags if t=='a' and a.get('href')==DEST and a.get('data-ivm153')=='bespoke')==1,'exact destination link')
    require(LABEL in html,'existing visible phrase preserved')
    require(sum(t=='h1' for t,a in tags)==1,'French Home H1 preserved')
    require([a.get('href') for t,a in tags if t=='link' and a.get('rel')=='canonical']==['https://ibizavipmove.com/fr/'],'French Home canonical preserved')
    require({a.get('hreflang') for t,a in tags if t=='link' and a.get('rel')=='alternate'}=={'en','es','fr','de','ar','x-default'},'French Home hreflang preserved')
    require('https://ibizavipmove.com/fr/conciergerie-sur-mesure-ibiza/' in urls,'destination remains in sitemap')
    print('PASS: Phase 153 audit — one same-language French Home bespoke link; visible wording, canonical, hreflang and 156-URL sitemap preserved')


if __name__=='__main__':
    run()
